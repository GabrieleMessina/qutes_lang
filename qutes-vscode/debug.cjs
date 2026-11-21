const path = require("node:path");
const vscode = require("vscode");

// The simulator returns a finished circuit run. There are no suspended threads.
class SimulatorSession {
  constructor(run) {
    this.run = run;
    this.messages = new vscode.EventEmitter();
    this.onDidSendMessage = this.messages.event;
    this.controller = new AbortController();
    this.sequence = 1;
  }

  send(message) {
    this.messages.fire({seq:this.sequence++, ...message});
  }

  async launch() {
    let exitCode = 1;
    const write = line => this.send({type:"event", event:"output", body:{category:"console", output:line + "\n"}});
    try {
      const result = await this.run(this.controller, write);
      if (result?.outcomes) exitCode = 0;
    } catch (error) {
      write(error.message);
    } finally {
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
        return reply({supportsTerminateRequest:true});
      case "launch":
        reply();
        this.send({type:"event", event:"initialized"});
        void this.launch();
        return;
      case "threads":
        return reply({threads:[]});
      case "setBreakpoints":
        return reply({breakpoints:(request.arguments.breakpoints || []).map(() => ({
          verified:false, message:"Qutes runs the circuit to completion."
        }))});
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
      return new vscode.DebugAdapterInlineImplementation(new SimulatorSession(async (controller, write) => {
        const doc = await vscode.workspace.openTextDocument(uri);
        if (doc.languageId !== "qutes") throw Error("Choose a Qutes file to run.");
        return run(doc, controller, write);
      }));
    }
  }));
};
