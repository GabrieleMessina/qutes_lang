lexer grammar qutes_lexer;

options {
   caseInsensitive = true;
}

// ----- Reserved keyword ----- 
INT_TYPE : 'int' ;
BOOL_TYPE : 'bool' ;
STRING_TYPE : 'string' ;
QUBIT_TYPE : 'qubit' ;
FLOAT_TYPE : 'float' ;
TRUE : 'true' ;
FALSE : 'false' ;
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
STRING_ENCLOSURE : '"';
QUBIT_LITERAL_POSTFIX : 'q';
COMMA : ',';

// ----- Comments -----
fragment
   COMMENT
   : '/*'(.*?)'*/'
   | '//'~('\r' | '\n')*
   ;

// ----- Literals -----
fragment
   DIGIT
      : [0-9]
      ;

INT_LITERAL
   : DIGIT+
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
   : FLOAT_LITERAL COMMA FLOAT_LITERAL QUBIT_LITERAL_POSTFIX
   ;

SYMBOL_LITERAL
   : [a-z0-9]+
   ;

STRING_LITERAL
   :  '"' ('\\' . | '""' | ~["\\])* '"';


// ----- Whitespace Character Handling -----
WS
   : ([ \r\n\t]+ | COMMENT) -> skip
   ;

NEWLINE
   : '\r'? '\n'
   ;
