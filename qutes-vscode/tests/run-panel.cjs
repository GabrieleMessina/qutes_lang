const assert = require("node:assert/strict");
const path = require("node:path");
const vscode = require("vscode");

async function panelRun(command, stop = false) {
  let text = "", exitCode, timer;
  let finish, fail;
  const ended = new Promise((resolve, reject) => { finish = resolve; fail = reject; });
  const tracker = vscode.debug.registerDebugAdapterTrackerFactory("qutes", {
    createDebugAdapterTracker(session) {
      return {
        onDidSendMessage(message) {
          if (message.event === "output") {
            text += message.body.output;
            if (stop && message.body.output.startsWith("Running ")) {
              vscode.debug.stopDebugging(session).then(undefined, fail);
            }
          }
          if (message.event === "exited") exitCode = message.body.exitCode;
        }
      };
    }
  });
  const listener = vscode.debug.onDidTerminateDebugSession(session => {
    if (session.type === "qutes") finish({text,exitCode});
  });
  try {
    timer = setTimeout(() => fail(Error("Run panel timeout: " + command + "\n" + text)), 60000);
    vscode.commands.executeCommand(command).then(undefined, fail);
    return await ended;
  } finally {
    clearTimeout(timer);
    listener.dispose();
    tracker.dispose();
  }
}

exports.run = async () => {
  assert.equal(vscode.workspace.workspaceFolders?.length || 0, 0);
  const file = process.env.QUTES_TEST_BELL;
  process.env.PATH = path.dirname(file);
  delete process.env.PYTHONPATH;
  const doc = await vscode.workspace.openTextDocument(file);
  const editor = await vscode.window.showTextDocument(doc);
  const bell = doc.getText();
  const run = "workbench.action.debug.start", runWithoutDebugging = "workbench.action.debug.run";
  async function edit(text) {
    await editor.edit(edit => edit.replace(new vscode.Range(doc.positionAt(0), doc.positionAt(doc.getText().length)), text));
    await doc.save();
    await vscode.window.showTextDocument(doc);
  }
  const result = await panelRun(run);
  assert.equal(result.exitCode, 0, result.text);
  assert.match(result.text, /64 shots/);
  assert.match(result.text, /\[false,false\]/);
  assert.match(result.text, /\[true,true\]/);
  assert.doesNotMatch(result.text, /\[(false,true|true,false)\]/);

  await edit("return missing;");
  const invalid = await panelRun(runWithoutDebugging);
  assert.equal(invalid.exitCode, 1, invalid.text);
  assert.match(invalid.text, /Q2002/);
  await edit(bell);
  const cancelled = await panelRun(run, true);
  assert.match(cancelled.text, /Stopped\./);
  const retry = await panelRun(runWithoutDebugging);
  assert.equal(retry.exitCode, 0, retry.text);
};
