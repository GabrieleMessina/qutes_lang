const assert = require("node:assert/strict");
const path = require("node:path");
const vscode = require("vscode");

async function panelRun(command, stop = false, onStop) {
  let text = "", exitCode, timer;
  let finish, fail;
  const ended = new Promise((resolve, reject) => { finish = resolve; fail = reject; });
  const tracker = vscode.debug.registerDebugAdapterTrackerFactory("qutes", {
    createDebugAdapterTracker(session) {
      return {
        onDidSendMessage(message) {
          if (message.event === "stopped" && onStop) {
            setImmediate(() => onStop(session, message.body).catch(fail));
          }
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

  const callLine = new vscode.SourceBreakpoint(new vscode.Location(doc.uri, new vscode.Position(6, 0)));
  vscode.debug.addBreakpoints([callLine]);
  const lines = [];
  async function inspect(session, event) {
    const thread = {threadId:event.threadId};
    const {stackFrames} = await session.customRequest("stackTrace", thread);
    const top = stackFrames[0];
    lines.push(top.line);
    assert.equal(top.source.path.toLowerCase(), file.toLowerCase());
    const {scopes} = await session.customRequest("scopes", {frameId:top.id});
    const {variables} = await session.customRequest("variables", {variablesReference:scopes[0].variablesReference});
    if (lines.length === 1) {
      assert.equal(event.reason, "breakpoint");
      assert.equal(top.line, 7);
      await session.customRequest("stepIn",thread);
    } else if (lines.length === 2) {
      assert.deepEqual(stackFrames.map(f => f.name), ["entangle","Script"]);
      assert.equal(top.line, 2);
      await session.customRequest("next", thread);
    } else if (lines.length === 3) {
      assert.equal(top.line, 3);
      assert.deepEqual(variables.map(v => v.name).sort(), ["|00⟩","|01⟩"]);
      assert.ok(variables.every(v => v.value.startsWith("50.0000%")));
      await session.customRequest("stepOut",thread);
    } else {
      assert.equal(top.line, 8);
      assert.deepEqual(variables.map(v => v.name).sort(), ["|00⟩","|11⟩"]);
      await session.customRequest("continue",thread);
    }
  }
  try {
    const interactive = await panelRun(run, false, inspect);
    assert.equal(interactive.exitCode, 0, interactive.text);
    assert.deepEqual(lines, [7,2,3,8]);
    assert.match(interactive.text, /\[(false,false|true,true)\]\s+1/);
    const over = [];
    const stopped = await panelRun(run, false, async (session, event) => {
      const thread = {threadId:event.threadId};
      const {stackFrames} = await session.customRequest("stackTrace", thread);
      over.push(stackFrames[0].line);
      if (over.length === 1) await session.customRequest("next", thread);
      else await vscode.debug.stopDebugging(session);
    });
    assert.deepEqual(over, [7,8]);
    assert.match(stopped.text, /Stopped\./);
    const bypass = await panelRun(runWithoutDebugging);
    assert.match(bypass.text, /64 shots/);
  } finally { vscode.debug.removeBreakpoints([callLine]); }

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
