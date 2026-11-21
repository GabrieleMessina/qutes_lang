const {spawn} = require("node:child_process");
const fs = require("node:fs/promises");
const path = require("node:path");
const os = require("node:os");
const {createHash} = require("node:crypto");
const {createReadStream} = require("node:fs");

function command(exe, args, options = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(exe, args, {windowsHide:true, stdio:["ignore","pipe","pipe"], ...options});
    const stdout = [], stderr = [];
    let bytes = 0;
    for (const [pipe, list] of [[child.stdout,stdout],[child.stderr,stderr]]) pipe.on("data", chunk => {
      bytes += chunk.length;
      if (bytes <= 32 * 1024 * 1024) list.push(chunk);
      else child.kill();
    });
    let failure;
    child.once("error", error => { failure = error; });
    child.once("close", code => {
      if (failure) return reject(failure);
      if (bytes > 32 * 1024 * 1024) return reject(Error("Compiler response exceeded 32 MiB."));
      resolve({code, stdout:Buffer.concat(stdout).toString("utf8"), stderr:Buffer.concat(stderr).toString("utf8")});
    });
  });
}

async function runtime(extension, storage) {
  const info = JSON.parse(await fs.readFile(path.join(extension,"runtime.json"),"utf8"));
  if (info.target !== process.platform + "-" + process.arch) throw Error("Install the Qutes package for this extension host.");
  // Some native Python modules on Windows still require short installation paths.
  const folder = path.join(storage, info.sha256.slice(0,16));
  const rel = process.platform === "win32" ? "qutes.exe" : "qutes";
  const executable = path.join(folder, rel);
  try { await fs.access(executable); return executable; } catch (error) { if (error.code !== "ENOENT") throw error; }
  await fs.mkdir(storage,{recursive:true});
  const staging = await fs.mkdtemp(path.join(storage,"unpack-"));
  try {
    const archive = path.join(extension,"runtime",info.archive);
    const hash = createHash("sha256");
    for await (const chunk of createReadStream(archive)) hash.update(chunk);
    if (hash.digest("hex") !== info.sha256) throw Error("Bundled Qutes runtime checksum mismatch. Reinstall the extension.");
    const mac = process.platform === "darwin";
    const unpack = mac ? "/usr/bin/ditto" : process.platform === "win32"
      ? path.join(process.env.SystemRoot,"System32","tar.exe") : "/usr/bin/tar";
    const result = await command(unpack, mac ? ["-x","-k",archive,staging] : ["-xf",archive,"-C",staging]);
    if (result.code !== 0) throw Error("Could not unpack Qutes: " + result.stderr);
    const expanded = path.join(staging,info.root);
    await fs.access(path.join(expanded,rel));
    try { await fs.rename(expanded,folder); }
    catch (error) {
      // A second VS Code window may finish the identical extraction first.
      try { await fs.access(executable); } catch { throw error; }
    }
    return executable;
  } finally { await fs.rm(staging,{recursive:true,force:true}); }
}

async function projectConfig(file, workspaceRoot) {
  let dir = path.dirname(file);
  while (true) {
    const config = path.join(dir,"qutes.toml");
    try { await fs.access(config); return config; } catch (error) { if (error.code !== "ENOENT") throw error; }
    if (!workspaceRoot || dir === workspaceRoot || dir === path.dirname(dir)) return undefined;
    dir = path.dirname(dir);
  }
}

async function invoke(executable, mode, text, {config, inputs, shots, signal} = {}) {
  signal?.throwIfAborted();
  const temp = await fs.mkdtemp(path.join(os.tmpdir(),"Qutes editor "));
  try {
    const file = path.join(temp,"document.qut");
    await fs.writeFile(file,text,"utf8");
    const args = [mode,file,"--json"];
    if (config) args.push("--config",config);
    if (mode === "run") {
      args.push("--shots",String(shots ?? 64));
      if (inputs) args.push("--inputs",inputs);
    }
    const result = await command(executable,args,{signal,env:{...process.env,PYTHONIOENCODING:"utf-8"}});
    try { return JSON.parse(result.stdout); }
    catch { throw Error(result.stderr.trim() || "The Qutes compiler exited without a result (" + result.code + ")."); }
  } finally { await fs.rm(temp,{recursive:true,force:true,maxRetries:5,retryDelay:100}); }
}
module.exports = {runtime, projectConfig, invoke};
