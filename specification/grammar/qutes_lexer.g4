lexer grammar qutes_lexer;

options {
   caseInsensitive = true;
}

// ----- Reserved keyword ----- 
INT_TYPE : 'int' ;
STRING_TYPE : 'string' ;
QUBIT_TYPE : 'qubit' ;
ADD : '+' ;
SUB : '-' ;
EQUAL : '==' ;
GREATER : '>' ;
GREATEREQUAL : '>=' ;
LOWER : '<' ;
LOWEREQUAL : '<=' ;
ASSIGN : '=' ;
END_OF_STATEMENT : ';' ;
VAR_STATEMENT : 'var' ;
IF_STATEMENT : 'if' ;
ELSE_STATEMENT : 'else' ;
WHILE_STATEMENT : 'while' ;
DO_STATEMENT : 'do' ;
CURLY_PARENTHESIS_OPEN : '{' ;
CURLY_PARENTHESIS_CLOSE : '}' ;
ROUND_PARENTHESIS_OPEN : '(' ;
ROUND_PARENTHESIS_CLOSE : ')' ;
DOT : '.' ;
STRING_ENCLOSURE : '"' ;
END_OF_PROGRAM : EOF ;

fragment
   COMMENT
   : '/*'(.*?)'*/' /*single comment*/
   | '//'~('\r' | '\n')* /* multiple comment*/
   ;

INT // INT bust me before STRING so that numbers doesn't get parsed as variable names
   : [0-9]+
   ;


STRING
   : [a-z]+
   ;


WS
   : ( [ \r\n\t]+ | COMMENT) -> skip
   ;

NEWLINE
   : '\r'? '\n'
   ;