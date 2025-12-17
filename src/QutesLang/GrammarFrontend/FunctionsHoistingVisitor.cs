using Qutes.Grammar;
using QutesLang.Symbols.Types;

namespace QutesLang.GrammarFrontend;

public class FunctionsHoistingVisitor : qutes_parserBaseVisitor<object>
{
    public override object VisitFunctionDeclarationParams(qutes_parser.FunctionDeclarationParamsContext context)
    {
        return base.VisitFunctionDeclarationParams(context);
    }
    
    // ogni volta che apro un nuovo scope, mando a questo visitor il context
    // in modo che lui possa fare l'hoisting delle funzioni dichiarate in quello scope
    // invece di fare l'hoisting globale all'inizio della compilazione
    // l'approccio globale richiede infatti di scandire il codice per 
    // aprire e chiudere gli scope esattamente come avverrà in fase di esecuzione
    // cosa che invece con questo approccio non è necessaria.
}