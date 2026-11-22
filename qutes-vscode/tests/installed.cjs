const assert = require("node:assert/strict");
const vscode = require("vscode");
const fs = require("node:fs/promises");
const path = require("node:path");
const delay = ms => new Promise(resolve => setTimeout(resolve,ms));
async function until(check) {
  for (let i=0;i<200;i++) { const value=check(); if(value) return value; await delay(250); }
  throw Error("Timed out waiting for the compiler diagnostics");
}
exports.run = async () => {
  const extension = vscode.extensions.getExtension("GabrieleMessina.qutes");
  assert.ok(extension);
  const root = vscode.workspace.workspaceFolders[0].uri.fsPath;
  process.env.PATH = root;
  delete process.env.PYTHONPATH;
  process.env.PYTHONNOUSERSITE = "1";
  await extension.activate();
  await fs.writeFile(path.join(root,"qutes.toml"),"[qutes]\nquint_bits = 3\n");
  const dir = path.join(root,"program with spaces");
  await fs.mkdir(dir);
  const filename = path.join(dir,"Bell pair.qut");
  await fs.writeFile(filename,"qubit a=false; qubit b=false; hadamard(a); if(a){not(b);} return [measure(a),measure(b)];");
  const doc = await vscode.workspace.openTextDocument(filename);
  const editor = await vscode.window.showTextDocument(doc);
  const run = () => vscode.commands.executeCommand("qutes.runQutesFile");
  const bell = await run();
  assert.ok(bell?.outcomes,JSON.stringify(bell));
  assert.deepEqual(bell.outcomes.map(o=>o.value).sort(),[[false,false],[true,true]]);
  assert.equal(bell.execution.shots,64);
  async function edit(text) {
    await editor.edit(builder => builder.replace(new vscode.Range(doc.positionAt(0),doc.positionAt(doc.getText().length)),text));
  }
  await edit("/* 🐈 */ return missing;");
  const errors = await until(() => vscode.languages.getDiagnostics(doc.uri).find(d=>d.code==="Q2002"));
  assert.equal(doc.getText(errors.range),"missing");
  await edit("input int n; return n;");
  const missing = await run(); assert.ok(missing.diagnostics.length);
  await edit("qubit q=false; hada");
  const completion = await vscode.commands.executeCommand("vscode.executeCompletionItemProvider",doc.uri,doc.positionAt(doc.getText().length));
  assert.ok(completion.items.some(c=>c.label==="hadamard"));
  await edit("qubit q=false; phase(q,");
  const help = await vscode.commands.executeCommand("vscode.executeSignatureHelpProvider",doc.uri,doc.positionAt(doc.getText().length),",");
  assert.equal(help.activeParameter,1);
  assert.ok(help.signatures[0].label.includes("float angle"));
  await edit("quint q=3; q+=1; return measure(q);");
  const task = run(); await delay(20); await vscode.commands.executeCommand("qutes.stop"); await task;
  assert.deepEqual((await run()).outcomes.map(o=>o.value),[-4]);
  assert.ok(doc.isDirty);
};
