using System.Data;

using Antlr4.Runtime;

namespace QutesLang.GrammarParsing;

public class QutesErrorListener : BaseErrorListener
{
    public override void SyntaxError(IRecognizer recognizer, IToken offendingSymbol, int line, int charPositionInLine, string msg,
        RecognitionException e)
    {
        base.SyntaxError(recognizer, offendingSymbol, line, charPositionInLine, msg, e);
        if (offendingSymbol != null)
        {
            throw new SyntaxErrorException($"Syntax error at line {line} position {charPositionInLine}, unexpected symbol: {offendingSymbol.Text}. {msg}");
        }
        throw new SyntaxErrorException($"Syntax error at line {line} position {charPositionInLine}: {msg}");
    }
}