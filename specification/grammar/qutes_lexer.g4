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
SQUARE_PARENTHESIS_OPEN : '[' ;
SQUARE_PARENTHESIS_CLOSE : ']' ;
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


BOOl_LITERAL
   : TRUE
   | FALSE
   | [01]
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
   : SQUARE_PARENTHESIS_OPEN INT_LITERAL (COMMA (' ')* INT_LITERAL)? SQUARE_PARENTHESIS_CLOSE QUBIT_LITERAL_POSTFIX
   | FLOAT_LITERAL COMMA FLOAT_LITERAL QUBIT_LITERAL_POSTFIX
   | MATH_SIGN? BOOl_LITERAL QUBIT_LITERAL_POSTFIX
   | MATH_SIGN QUBIT_LITERAL_POSTFIX
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
