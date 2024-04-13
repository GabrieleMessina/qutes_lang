lexer grammar qutes_lexer;

options {
   caseInsensitive = true; //TODO: we should remove this for better variable declaration?
}

// ----- Reserved keyword ----- 
INT_TYPE : 'int' ;
BOOL_TYPE : 'bool' ;
STRING_TYPE : 'string' ;
QUBIT_TYPE : 'qubit' ;
QUINT_TYPE : 'quint' ;
QUSTRING_TYPE : 'qustring' ;
FLOAT_TYPE : 'float' ;
VOID_TYPE : 'void' ;
RETURN : 'return' ;
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
   MATH_SIGN
      : [+-]
      ;

fragment
   QUBIT_STANDARD
      : '|0>'
      | '|1>'
      | '|+>'
      | '|->'
      ;

BOOL_LITERAL
   : TRUE
   | FALSE
   | '1'
   | '0'
   ;

INT_LITERAL
   : MATH_SIGN? DIGIT+
   ;

FLOAT_LITERAL
   : MATH_SIGN? DIGIT+ '.' DIGIT*
   | MATH_SIGN? '.' DIGIT+
   ;

HEX_LITERAL
   : '0' [x] ([a-f] | DIGIT)+ 
   ;

BIN_LITERAL
   : '0' [b] [01]+ 
   ;

QUBIT_LITERAL
   : SQUARE_PARENTHESIS_OPEN (BOOL_LITERAL | '0' | '1') (COMMA (' ')* (BOOL_LITERAL | '0' | '1'))? SQUARE_PARENTHESIS_CLOSE [q]
   | FLOAT_LITERAL COMMA FLOAT_LITERAL [q]
   | QUBIT_STANDARD
   | MATH_SIGN? (BOOL_LITERAL | '0' | '1') [q]
   ;

QUINT_LITERAL
   : QUBIT_LITERAL
   | SQUARE_PARENTHESIS_OPEN QUBIT_LITERAL (COMMA (' ')* QUBIT_LITERAL)* SQUARE_PARENTHESIS_CLOSE
   | SQUARE_PARENTHESIS_OPEN INT_LITERAL (COMMA (' ')* INT_LITERAL)* SQUARE_PARENTHESIS_CLOSE [q]
   | MATH_SIGN? DIGIT+ [q]
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


// ----- Whitespace Character Handling -----
WS
   : ([ \r\n\t]+ | COMMENT) -> skip
   ;

NEWLINE
   : '\r'? '\n'
   ;
