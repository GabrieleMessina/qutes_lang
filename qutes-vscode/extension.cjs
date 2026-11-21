const vscode = require("vscode");
const native = require("./runtime.cjs");

async function activate(context) {
  const service = await import("./language/language.mjs");
  const diagnostics = vscode.languages.createDiagnosticCollection("Qutes");
  const output = vscode.window.createOutputChannel("Qutes");
  const pending = new Map(), inputs = new Map(), indices = new WeakMap();
  let installed, running, shots = 64;
  const exe = () => installed ??= native.runtime(context.extensionPath, context.globalStorageUri.fsPath)
    .catch(error => { installed = undefined; throw error; });
  const config = doc => doc.isUntitled ? undefined : native.projectConfig(doc.fileName,
    vscode.workspace.getWorkspaceFolder(doc.uri)?.uri.fsPath);
  const key = doc => doc.uri.toString();
  function cancel(doc) {
    const job = pending.get(key(doc));
    if (job) { clearTimeout(job.timer); job.controller.abort(); pending.delete(key(doc)); }
  }
  function index(doc) {
    const cached = indices.get(doc);
    if (cached?.version === doc.version) return cached.index;
    const index = service.indexDocument(doc.getText());
    indices.set(doc,{version:doc.version,index});
    return index;
  }
  function display(doc, list) {
    diagnostics.set(doc.uri,list.map(item => {
      const span = new vscode.Range(doc.positionAt(item.from),doc.positionAt(item.to));
      const d = new vscode.Diagnostic(span,[item.message,item.hint].filter(Boolean).join("\n"),
        item.severity === "warning" ? vscode.DiagnosticSeverity.Warning : vscode.DiagnosticSeverity.Error);
      d.source = "Qutes"; d.code = item.code;
      return d;
    }));
  }
  function schedule(doc) {
    if (doc.languageId !== "qutes") return;
    cancel(doc);
    diagnostics.delete(doc.uri);
    const controller = new AbortController(), revision = doc.version;
    const timer = setTimeout(async () => {
      try {
        const text = doc.getText();
        const report = await service.analyzeDocument({text,revision,config:await config(doc)},
          async (source,settings) => native.invoke(await exe(),"analyze",source,{config:settings,signal:controller.signal}));
        if (!controller.signal.aborted && doc.version === report.revision && !doc.isClosed) display(doc,report.diagnostics);
      } catch (error) {
        if (!controller.signal.aborted) {
          output.appendLine(error.message);
          display(doc,[{from:0,to:0,message:error.message,code:"Qutes editor"}]);
        }
      } finally { if (pending.get(key(doc))?.controller === controller) pending.delete(key(doc)); }
    },300);
    pending.set(key(doc),{controller,timer});
  }
  const selector = {language:"qutes"};
  const kinds = {type:"Struct",keyword:"Keyword",constant:"Constant",function:"Function",
    builtin:"Function",variable:"Variable",parameter:"Variable"};
  const add = (...items) => context.subscriptions.push(...items);
  const register = (id,fn) => add(vscode.commands.registerCommand("qutes."+id,fn));
  add(diagnostics,output,vscode.workspace.onDidOpenTextDocument(schedule),
    vscode.workspace.onDidChangeTextDocument(e => schedule(e.document)),
    vscode.workspace.onDidCloseTextDocument(doc => { cancel(doc); inputs.delete(key(doc)); diagnostics.delete(doc.uri); }),
    {dispose() { for (const job of pending.values()) { clearTimeout(job.timer); job.controller.abort(); } running?.abort(); }});
  const watcher = vscode.workspace.createFileSystemWatcher("**/qutes.toml");
  const refresh = () => vscode.workspace.textDocuments.forEach(schedule);
  add(watcher,watcher.onDidCreate(refresh),watcher.onDidChange(refresh),watcher.onDidDelete(refresh));
  add(vscode.languages.registerCompletionItemProvider(selector,{
    provideCompletionItems(doc,pos) {
      const {from,completions} = service.atCursor(index(doc),doc.offsetAt(pos));
      return completions.map(s => {
        const item = new vscode.CompletionItem(s.label,vscode.CompletionItemKind[kinds[s.kind]]);
        item.detail = s.signatures ? s.label+"("+s.signatures[0].join(", ")+")" : s.detail ?? s.kind;
        item.range = new vscode.Range(doc.positionAt(from),pos);
        return item;
      });
    }
  }),vscode.languages.registerSignatureHelpProvider(selector,{
    provideSignatureHelp(doc,pos) {
      const s = service.atCursor(index(doc),doc.offsetAt(pos)).signature;
      if (!s) return;
      const help = new vscode.SignatureHelp();
      help.signatures = s.signatures.map(params => {
        const info = new vscode.SignatureInformation(s.label+"("+params.join(", ")+")");
        info.parameters = params.map(p => new vscode.ParameterInformation(p));
        return info;
      });
      help.activeSignature = Math.max(0,s.signatures.findIndex(p => p.length > s.argument));
      help.activeParameter = s.argument;
      return help;
    }
  },"(",","));
  register("selectInputs",async () => {
    const doc = vscode.window.activeTextEditor?.document;
    if (doc?.languageId !== "qutes") return;
    const choice = await vscode.window.showQuickPick(["Choose a JSON file","Clear input selection"]);
    if (!choice) return;
    if (choice.startsWith("Clear")) { inputs.delete(key(doc)); return; }
    const files = await vscode.window.showOpenDialog({filters:{JSON:["json"]},canSelectMany:false});
    if (files?.length) inputs.set(key(doc),files[0].fsPath);
  });
  register("setShots",async () => {
    const value = await vscode.window.showInputBox({prompt:"Number of simulator shots",value:String(shots),
      validateInput:s => /^[1-9]\d*$/.test(s) && Number.isSafeInteger(Number(s)) ? null : "Enter a positive whole number."});
    if (value) shots = Number(value);
  });
  register("stop",() => running?.abort());
  register("runQutesFile",async () => {
    const doc = vscode.window.activeTextEditor?.document;
    if (!doc || doc.languageId !== "qutes" || running) return;
    const controller = new AbortController(), revision = doc.version, text = doc.getText();
    running = controller;
    output.clear(); output.show(true); output.appendLine("Running " + doc.fileName);
    try {
      await vscode.commands.executeCommand("setContext","qutes.running",true);
      const result = await native.invoke(await exe(),"run",text,{config:await config(doc),inputs:inputs.get(key(doc)),shots,signal:controller.signal});
      if (result.diagnostics) {
        const errors = service.diagnostics(text,result);
        if (!doc.isClosed && doc.version === revision) display(doc,errors);
        errors.forEach(d => output.appendLine(d.code+" "+d.message+(d.hint ? "\n"+d.hint : "")));
      } else {
        output.appendLine(result.execution.shots+" shots · "+result.execution.backend);
        for (const row of result.outcomes) output.appendLine(JSON.stringify(row.value)+"   "+row.count);
      }
      return result;
    } catch (error) { output.appendLine(controller.signal.aborted ? "Stopped." : error.message); }
    finally { running = undefined; await vscode.commands.executeCommand("setContext","qutes.running",false); }
  });
  refresh();
}
module.exports = {activate};
