// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
	let disposable = vscode.commands.registerCommand('qutes.runQutesFile', function () {
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
            args: ["-image","-circuit","-iter","1",filePath],
            justMyCode: true
            
        };

        // Start debugging with the defined configuration
        vscode.debug.startDebugging(undefined, debugConfiguration);
    });
    context.subscriptions.push(disposable);
}

// this method is called when your extension is deactivated
function deactivate() {}

// eslint-disable-next-line no-undef
module.exports = {
	activate,
	deactivate
}