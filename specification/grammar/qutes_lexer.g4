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
RANGE_TYPE : 'range' ;
RETURN : 'return' ;
YIELD : 'yield' ;
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
RANGE_OPERATOR : '..' ;
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

CANON_QUBIT
   : '|0>'
   | '|1>'
   | '|+>'
   | '|->'
   ;

QUANTUM_SUFFIX : 'q' ;

// Helper fragment for escape sequences (newline, tab, quotes, etc.)
fragment ESCAPE_SEQUENCE
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
    : '\'' ( ESCAPE_SEQUENCE | ~['\\\r\n] ) '\''
    ;

FLOAT_LITERAL
   : DIGIT+ '.' DIGIT+
   | '.' DIGIT+
   ;

HEX_LITERAL
   : '0' [x] ([a-f] | DIGIT)+ 
   ;

BIN_LITERAL
   : '0' [b] [01]+ 
   ;

SYMBOL_LITERAL
   : [a-zA-Z_][a-zA-Z0-9_]*
   ;

STRING_LITERAL //this match "something""somethingelse"
   :  '"' ('\\' . | '""' | ~["\\])* '"'
   ;

//STRING_LITERAL //this doesn't match "something""somethingelse"
//   : '"' ( ESCAPE_SEQUENCE | ~["\\\r\n] )* '"'
//   ;


// ----- Whitespace Character Handling -----
WS
   : ([ \r\n\t]+ | COMMENT) -> skip
   ;

NEWLINE
   : '\r'? '\n'
   ;
