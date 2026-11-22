const {downloadAndUnzipVSCode,resolveCliArgsFromVSCodeExecutablePath,runTests} = require("@vscode/test-electron");
const {spawnSync} = require("node:child_process");
const fs = require("node:fs/promises");
const os = require("node:os");
const path = require("node:path");

async function main() {
  const archive = path.resolve(process.argv[2]);
  const exe = process.env.QUTES_VSCODE || await downloadAndUnzipVSCode("stable");
  const root = await fs.mkdtemp(path.join(os.tmpdir(),"Qutes offline review "));
  console.log("Testing in",root);
  const data = path.join(root,"profile"), extensions = path.join(root,"extensions"), workspace = path.join(root,"course");
  await fs.mkdir(workspace);
  const flags = ["--user-data-dir="+data,"--extensions-dir="+extensions,"--disable-updates",
    "--disable-telemetry","--disable-workspace-trust","--host-resolver-rules=MAP * ~NOTFOUND"];
  const [cli,...cliArgs] = resolveCliArgsFromVSCodeExecutablePath(exe,{reuseMachineInstall:true});
  let cliScript = path.resolve(path.dirname(exe),"resources/app/out/cli.js");
  if (process.platform === "win32") {
    const candidates = await fs.readdir(path.dirname(exe));
    for (const entry of candidates.filter(n => /^[a-f0-9]{8,40}$/.test(n))) {
      const versioned = path.join(path.dirname(exe),entry,"resources/app/out/cli.js");
      try { await fs.access(versioned); cliScript=versioned; break; } catch { /* other version */ }
    }
  }
  const install = process.platform === "win32"
    ? spawnSync(exe,[cliScript,...flags,"--install-extension",archive],
      {stdio:"inherit",env:{...process.env,ELECTRON_RUN_AS_NODE:"1"}})
    : spawnSync(cli,[...cliArgs,...flags,"--install-extension",archive],{stdio:"inherit"});
  if (install.status !== 0) throw Error("VSIX installation failed");
  await runTests({vscodeExecutablePath:exe,extensionDevelopmentPath:path.join(__dirname,"harness"),
    extensionTestsPath:path.join(__dirname,"installed.cjs"),launchArgs:[workspace,...flags],
    reuseMachineInstall:true});
  const bell = path.join(root,"Bell pair.qut");
  await fs.copyFile(path.resolve(__dirname,"../../examples/language/41_bell_gates.qut"),bell);
  await runTests({vscodeExecutablePath:exe,extensionDevelopmentPath:path.join(__dirname,"harness"),
    extensionTestsPath:path.join(__dirname,"run-panel.cjs"),launchArgs:[bell,...flags,"--new-window"],
    extensionTestsEnv:{QUTES_TEST_BELL:bell},reuseMachineInstall:true});
  if (path.dirname(path.resolve(root)) !== path.resolve(os.tmpdir())) throw Error("Unexpected test directory");
  await fs.rm(root,{recursive:true,force:true,maxRetries:5,retryDelay:200});
}
main().catch(error=>{ console.error(error); process.exitCode=1; });
