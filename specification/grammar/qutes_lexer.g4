lexer grammar qutes_lexer;

// ----- Reserved keyword ----- 
BOOL_TYPE : 'bool' ;
INT_TYPE : 'int' ;
CHAR_TYPE : 'char' ;
FLOAT_TYPE : 'float' ;
STRING_TYPE : 'string' ;
QUBIT_TYPE : 'qubit' ;
QUINT_TYPE : 'quint' ;
QUSTRING_TYPE : 'qustring' ;
QUCHAR_TYPE : 'quchar' ;
VOID_TYPE : 'void' ;
RETURN : 'return' ;
BREAK : 'break' ;
EXP : '^' ;
MULTIPLY : '*' ;
DIVIDE : '/' ;
MODULE : '%' ;
ADD : '+' ;
SUB : '-' ;
NOT : 'not' ;
AND : 'and' ;
OR : 'or' ;
BY : 'by' ;
SWAP : 'swap' ;
PAULIY : 'pauliy' ;
PAULIZ : 'pauliz' ;
GROVER : 'grover' ;
MCZ : 'mcz' ;
CNOT : 'cnot' ;
MCX : 'mcx' ;
MCY : 'mcy' ;
MCP : 'mcp' ;
HADAMARD : 'hadamard' ;
MEASURE : 'measure' ;
PRINT : 'print' ;
BARRIER : 'barrier' ;
EQUAL : '==' ;
NOT_EQUAL : '!=' ;
GREATER : '>' ;
GREATEREQUAL : '>=' ;
LOWER : '<' ;
LOWEREQUAL : '<=' ;
LSHIFT : '<<' ;
RSHIFT : '>>' ;
ASSIGN : '=' ;
AUTO_INCREMENT : '++' ;
AUTO_DECREMENT : '--' ;
AUTO_SUM : '+=' ;
AUTO_SUB : '-=' ;
AUTO_MULTIPLY : '*=' ;
AUTO_DIVIDE : '/=' ;
AUTO_MODULE : '%=' ;
END_OF_STATEMENT : ';' ;
VAR_STATEMENT : 'var' ;
FOR_STATEMENT : 'for' ;
FOREACH_STATEMENT : 'foreach' ;
SEARCH_STATEMENT : 'search' ;
IN_STATEMENT : 'in' ;
WHERE_STATEMENT : 'where' ;
IF_STATEMENT : 'if' ;
ELSE_STATEMENT : 'else' ;
WHILE_STATEMENT : 'while' ;
DO_STATEMENT : 'do' ;
CURLY_PARENTHESIS_OPEN : '{' ;
CURLY_PARENTHESIS_CLOSE : '}' ;
ROUND_PARENTHESIS_OPEN : '(' ;
ROUND_PARENTHESIS_CLOSE : ')' ;
SQUARE_PARENTHESIS_OPEN : '[' ;
SQUARE_PARENTHESIS_CLOSE : ']' ;
DOT : '.' ;
STRING_ENCLOSURE : '"';
COMMA : ',';

// ----- Comments -----
fragment
   COMMENT
   : '/*'(.*?)'*/'
   | '//'~('\r' | '\n')*
   ;

// ----- Literals -----
fragment
   TRUE : 'true' ;

fragment
   FALSE : 'false' ;

fragment
   DIGIT
      : [0-9]
      ;

fragment
   CANON_QUBIT
      : '|0>'
      | '|1>'
      | '|+>'
      | '|->'
      ;

// Helper fragment for escape sequences (newline, tab, quotes, etc.)
fragment EscapeSequence
    : '\\' [btnfr"'\\]
    ;

BOOL_LITERAL
   : TRUE
   | FALSE
   ;

INT_LITERAL
   : DIGIT+
   ;

CHAR_LITERAL
    : '\'' ( EscapeSequence | ~['\\\r\n] ) '\''
    ;

FLOAT_LITERAL
   : DIGIT+ '.' DIGIT*
   | '.' DIGIT+
   ;

HEX_LITERAL
   : '0' [x] ([a-f] | DIGIT)+ 
   ;

BIN_LITERAL
   : '0' [b] [01]+ 
   ;

QUBIT_LITERAL
   : SQUARE_PARENTHESIS_OPEN BOOL_LITERAL (COMMA BOOL_LITERAL)? SQUARE_PARENTHESIS_CLOSE [q]
   | SQUARE_PARENTHESIS_OPEN FLOAT_LITERAL COMMA FLOAT_LITERAL SQUARE_PARENTHESIS_OPEN [q]
   | CANON_QUBIT
   | BOOL_LITERAL [q]
   ;

QUINT_LITERAL
   : QUBIT_LITERAL
   | SQUARE_PARENTHESIS_OPEN INT_LITERAL (COMMA INT_LITERAL)* SQUARE_PARENTHESIS_CLOSE [q]
   | INT_LITERAL [q]
   ;

QUCHAR_LITERAL
   : CHAR_LITERAL [q]
   ;

QUSTRING_LITERAL
   : STRING_LITERAL [q]
   ;


SYMBOL_LITERAL
   : [a-z_][a-z0-9_]*
   ;

STRING_LITERAL
   :  '"' ('\\' . | '""' | ~["\\])* '"'
   ;

//STRING_LITERAL
//   : '"' ( EscapeSequence | ~["\\\r\n] )* '"'
//   ;


// ----- Whitespace Character Handling -----
WS
   : ([ \r\n\t]+ | COMMENT) -> skip
   ;

NEWLINE
   : '\r'? '\n'
   ;
