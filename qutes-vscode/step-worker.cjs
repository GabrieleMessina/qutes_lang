const {parentPort, workerData} = require("node:worker_threads");
const fs = require("node:fs/promises");
const path = require("node:path");
const {loadPyodide} = require("./step-runtime/pyodide.js");

async function start() {
  const root = path.join(__dirname, "step-runtime");
  const py = await loadPyodide({indexURL:root + path.sep});
  py.FS.writeFile("/compiler.zip", await fs.readFile(path.join(root, "compiler.zip")));
  if (workerData.config) py.FS.writeFile("/qutes.toml", await fs.readFile(workerData.config));
  py.globals.set("source", workerData.text);
  py.globals.set("filename", workerData.filename);
  py.globals.set("input_text", workerData.inputs ? await fs.readFile(workerData.inputs, "utf8") : "{}");
  const ready = JSON.parse(py.runPython(`
import sys
sys.path.insert(0, "/compiler.zip")
from pathlib import Path
from qutes.source_debug import DebugShot
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError
from qutes.serialization import json_text, load_json
try:
    cfg = Path("/qutes.toml")
    shot = DebugShot(source, filename, load_json(input_text), CompilerConfig.load(cfg) if cfg.exists() else None)
    status = {"lines": sorted({point.span.start.line for point in shot.points})}
except DiagnosticError as error:
    status = {"diagnostics": [d.to_dict() for d in error.diagnostics]}
json_text(status)
`));
  parentPort.postMessage(ready);
  if (!ready.lines) return;
  let mode, depth = 0, breakpoints = [], scheduled = false;
  function advance() {
    scheduled = false;
    try {
      py.globals.set("action", mode);
      py.globals.set("depth", depth);
      py.globals.set("lines_json", JSON.stringify(breakpoints));
      const result = JSON.parse(py.runPython("json_text(shot.advance(action, set(load_json(lines_json)), depth))"));
      if (!result.frames && !result.done) return schedule();
      if (result.frames) depth = result.frames.length - 1;
      parentPort.postMessage(result);
    } catch (error) {
      parentPort.postMessage({error:error.message});
    }
  }
  function schedule() {
    if (!scheduled) { scheduled = true; setImmediate(advance); }
  }
  parentPort.on("message", message => {
    if (message.breakpoints) breakpoints = message.breakpoints;
    if (message.mode) { mode = message.mode; schedule(); }
  });
}
start().catch(error => parentPort.postMessage({error:error.message}));
