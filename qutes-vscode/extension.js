const vscode = require('vscode');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
	let runQutesFileCommand = vscode.commands.registerCommand('qutes.runQutesFile', function () {
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

    let runQutesFile100Command = vscode.commands.registerCommand('qutes.runQutesFile100', function () {
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
            args: ["-image","-circuit","-iter","100",filePath],
            justMyCode: true
            
        };

        // Start debugging with the defined configuration
        vscode.debug.startDebugging(undefined, debugConfiguration);
    });

    context.subscriptions.push(runQutesFileCommand);
    context.subscriptions.push(runQutesFile100Command);
}

function deactivate() {}

// eslint-disable-next-line no-undef
module.exports = {
	activate,
	deactivate
}