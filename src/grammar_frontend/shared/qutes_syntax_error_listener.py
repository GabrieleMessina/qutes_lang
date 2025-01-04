from antlr4.error.ErrorListener import ConsoleErrorListener as ErrorListenerToExtend

class QutesErrorListener(ErrorListenerToExtend):
    def __init__(self):
        super().__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxError("Syntax error at" + " line: " + str(line) + ", column: " + str(column) + ((", unexpected symbol: " + offendingSymbol.text) if offendingSymbol is not None else "") + ". " + msg) from e

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        pass #Not an error, just a trace

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        pass #Not an error, just a trace

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        pass #Not an error, just a trace