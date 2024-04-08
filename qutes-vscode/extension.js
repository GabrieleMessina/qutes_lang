const vscode = require('vscode');

function runQutes(runs, params = []){
    let activeEditor = vscode.window.activeTextEditor;
    if (!activeEditor || activeEditor.document.languageId !== 'qutes') {
        return; // no active editor or the active file is not a Qutes file
    }

    let filePath = activeEditor.document.uri.fsPath;

    // Define a debug configuration
    let debugConfiguration = {
        name: "Run Qutes File",
        type: "debugpy",
        request: "launch",
        program: "src/qutes.py",
        console: "integratedTerminal",
        args: [params,"-image","-circuit","-iter",runs,filePath],
        justMyCode: true
    };

    // Start debugging with the defined configuration
    vscode.debug.startDebugging(undefined, debugConfiguration);
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
	let runQutesFileCommand = vscode.commands.registerCommand('qutes.runQutesFile', function () {
        runQutes("1");
    });

    let runQutesFile100Command = vscode.commands.registerCommand('qutes.runQutesFile100', function () {
        runQutes("100");
    });

    let runQutesFileVerboseCommand = vscode.commands.registerCommand('qutes.runQutesFileVerbose', function () {
        runQutes("1", ["--verbose"]);
    });

    let runQutesFile100VerboseCommand = vscode.commands.registerCommand('qutes.runQutesFileVerbose100', function () {
        runQutes("100", ["--verbose"]);
    });

    context.subscriptions.push(runQutesFileCommand);
    context.subscriptions.push(runQutesFile100Command);
    context.subscriptions.push(runQutesFileVerboseCommand);
    context.subscriptions.push(runQutesFile100VerboseCommand);
}

function deactivate() {}

// eslint-disable-next-line no-undef
module.exports = {
	activate,
	deactivate
}