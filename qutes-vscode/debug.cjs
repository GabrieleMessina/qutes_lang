const path = require("node:path");
const {Worker} = require("node:worker_threads");
const vscode = require("vscode");

class SimulatorSession {
  constructor(uri, run) {
    this.uri = uri;
    this.run = run;
    this.messages = new vscode.EventEmitter();
    this.onDidSendMessage = this.messages.event;
    this.controller = new AbortController();
    this.sequence = 1;
    this.breakpoints = new Map();
    this.nextId = 1;
  }

  send(message) {
    this.messages.fire({seq:this.sequence++, ...message});
  }

  event(event, body) {
    this.send({type:"event", event, body});
  }

  breakpoint(line, id) {
    const verified = this.lines?.has(line) ?? false;
    const message = this.lines ? "No executable statement on this line for these inputs." : "Waiting for the compiled circuit.";
    return {line, id, verified, ...(verified ? {} : {message})};
  }

  setBreakpoints(args) {
    const requested = args.breakpoints || [];
    if (!args.source.path || ![this.uri.fsPath, this.uri.toString()].includes(args.source.path)
        && vscode.Uri.file(args.source.path).toString() !== this.uri.toString()) {
      return requested.map(({line}) => ({line, verified:false, message:"Outside the active Qutes program."}));
    }
    const previous = this.breakpoints;
    this.breakpoints = new Map();
    const points = requested.map(({line, condition, hitCondition, logMessage}) => {
      if (condition || hitCondition || logMessage) return {line, verified:false, message:"Choose a plain line breakpoint."};
      const id = previous.get(line) ?? this.nextId++;
      this.breakpoints.set(line, id);
      return this.breakpoint(line, id);
    });
    this.worker?.postMessage({breakpoints:[...this.breakpoints.keys()]});
    return points;
  }

  stepShot(data) {
    const signal = this.controller.signal;
    signal.throwIfAborted();
    return new Promise((resolve, reject) => {
      const worker = new Worker(path.join(__dirname, "step-worker.cjs"), {workerData:data});
      this.worker = worker;
      const abort = () => reject(Error("Stopped."));
      signal.addEventListener("abort", abort, {once:true});
      this.clearWorker = () => {
        signal.removeEventListener("abort", abort);
        this.worker = undefined;
        void worker.terminate();
      };
      worker.on("error", reject);
      worker.on("exit", () => reject(Error("The Qutes stepping worker exited.")));
      worker.on("message", message => {
        if (signal.aborted) return;
        if (message.lines) {
          this.lines = new Set(message.lines);
          for (const [line, id] of this.breakpoints) {
            this.event("breakpoint", {reason:"changed", breakpoint:this.breakpoint(line, id)});
          }
          worker.postMessage({mode:this.args.stopOnEntry ? "entry" : "continue", breakpoints:[...this.breakpoints.keys()]});
        } else if (message.frames) {
          this.stopped = message;
          this.event("stopped", {reason:message.reason, threadId:1, allThreadsStopped:true,
            ...(message.reason === "breakpoint" ? {hitBreakpointIds:[this.breakpoints.get(message.frames[0].line)]} : {})});
        } else if (message.done) {
          resolve({execution:{shots:1, backend:"Qutes interactive statevector"}, outcomes:[{value:message.result,count:1}]});
        } else if (message.diagnostics) resolve(message);
        else reject(Error(message.error));
      });
    });
  }

  async launch() {
    let exitCode = 1;
    const write = line => this.send({type:"event", event:"output", body:{category:"console", output:line + "\n"}});
    try {
      const interactive = !this.args.noDebug && (this.args.stopOnEntry || this.breakpoints.size > 0);
      const result = await this.run(this.controller, write, interactive ? data => this.stepShot(data) : undefined);
      if (result?.outcomes) exitCode = 0;
    } catch (error) {
      write(error.message);
    } finally {
      this.clearWorker?.();
      this.send({type:"event", event:"exited", body:{exitCode}});
      this.send({type:"event", event:"terminated"});
    }
  }

  handleMessage(request) {
    if (request.type !== "request") return;
    const reply = (body, success = true, message) => this.send({
      type:"response", request_seq:request.seq, command:request.command, success, body, message
    });
    switch (request.command) {
      case "initialize":
        return reply({supportsTerminateRequest:true, supportsConfigurationDoneRequest:true});
      case "launch":
        this.args = request.arguments;
        reply();
        this.send({type:"event", event:"initialized"});
        return;
      case "configurationDone":
        reply();
        void this.launch();
        return;
      case "threads":
        return reply({threads:this.worker ? [{id:1, name:"Qutes simulation · one shot"}] : []});
      case "setBreakpoints":
        return reply({breakpoints:this.setBreakpoints(request.arguments)});
      case "stackTrace":
        return reply({stackFrames:(this.stopped?.frames || []).map((frame, i) => ({
          ...frame, id:i + 1, source:{name:path.basename(this.uri.fsPath), path:this.uri.fsPath}
        }))});
      case "scopes": {
        const frameId = request.arguments.frameId;
        const frame = this.stopped?.sourceScopes[frameId - 1];
        if (!frame) return reply({scopes:[]});
        const order = frame.wireOrder.join(" ");
        return reply({scopes:[
          {name:"Qutes variables", variablesReference:frameId + 1, presentationHint:"locals", expensive:false},
          {name:order ? "Quantum state · |" + order + "⟩" : "Quantum state", variablesReference:1, expensive:false}
        ]});
      }
      case "variables": {
        const ref = request.arguments.variablesReference;
        if (!this.stopped) return reply({variables:[]});
        const {sourceScopes, distributions} = this.stopped;
        const firstDistribution = sourceScopes.length + 2;
        const {filter, start = 0, count} = request.arguments;
        const indexed = ref >= firstDistribution;
        if (filter && filter !== (indexed ? "indexed" : "named")) return reply({variables:[]});
        let values;
        if (ref === 1) values = this.stopped.variables;
        else if (ref < firstDistribution) values = sourceScopes[ref - 2]?.variables;
        else values = distributions[ref - firstDistribution];
        const variables = (values || []).slice(start, count > 0 ? start + count : undefined);
        return reply({variables:variables.map(({name, value, distribution}) => (
          distribution === undefined ? {name, value, variablesReference:0} :
            {name, value, variablesReference:firstDistribution + distribution,
             indexedVariables:distributions[distribution].length}
        ))});
      }
      case "next":
      case "stepIn":
      case "stepOut":
      case "continue":
        if (!this.stopped) return reply(undefined, false, "The circuit is not paused.");
        this.stopped = undefined;
        reply(request.command === "continue" ? {allThreadsContinued:true} : undefined);
        this.event("continued", {threadId:1, allThreadsContinued:true});
        this.worker.postMessage({mode:request.command});
        return;
      case "pause":
        if (!this.worker) return reply(undefined, false, "Start a stepping session with a breakpoint.");
        this.worker.postMessage({mode:"pause"});
        return reply();
      case "terminate":
      case "disconnect":
        this.controller.abort();
        return reply();
      default:
        return reply(undefined, false, "Unsupported Qutes request: " + request.command);
    }
  }

  dispose() {
    this.controller.abort();
    this.messages.dispose();
  }
}

exports.register = function (context, run) {
  context.subscriptions.push(vscode.debug.registerDebugConfigurationProvider("qutes", {
    resolveDebugConfiguration(folder, config) {
      if (config.request && config.request !== "launch") return undefined;
      const doc = vscode.window.activeTextEditor?.document;
      if (!config.program && doc?.languageId !== "qutes") {
        vscode.window.showErrorMessage("Open a Qutes file to run it.");
        return null;
      }
      return {name:"Run Qutes File", internalConsoleOptions:"openOnSessionStart", ...config,
        type:"qutes", request:"launch", documentUri:config.program ? undefined : doc.uri.toString()};
    }
  }), vscode.debug.registerDebugAdapterDescriptorFactory("qutes", {
    createDebugAdapterDescriptor(session) {
      const config = session.configuration;
      const uri = config.program
        ? vscode.Uri.file(path.resolve(session.workspaceFolder?.uri.fsPath || "", config.program))
        : vscode.Uri.parse(config.documentUri);
      return new vscode.DebugAdapterInlineImplementation(new SimulatorSession(uri, async (controller, write, stepShot) => {
        const doc = await vscode.workspace.openTextDocument(uri);
        if (doc.languageId !== "qutes") throw Error("Choose a Qutes file to run.");
        const listener = stepShot && vscode.workspace.onDidChangeTextDocument(change => {
          if (change.document === doc && change.contentChanges.length) {
            write("Source changed. Restart debugging to use your edits.");
            controller.abort();
          }
        });
        try { return await run(doc, controller, write, stepShot); }
        finally { listener?.dispose(); }
      }));
    }
  }));
};
