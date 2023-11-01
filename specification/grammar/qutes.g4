grammar qutes;

// ----- Reserved keyword ----- 
ADD : '+' ;
SUB : '-' ;
EQUAL : '==' ;
GREATER : '>' ;
GREATEREQUAL : '>=' ;
LOWER : '<' ;
LOWEREQUAL : '<=' ;
ASSIGN : '=' ;
END_OF_STATEMENT : ';' ;
IF_STATEMENT : 'if' ;
ELSE_STATEMENT : 'else' ;
WHILE_STATEMENT : 'while' ;
DO_STATEMENT : 'do' ;
BLOCK_STATEMENT_START : '{' ;
BLOCK_STATEMENT_END : '}' ;
STRING_ENCLOSURE : '"' ;
END_OF_PROGRAM : EOF ;

fragment
COMMENT
: '/*'(.*?)'*/' /*single comment*/
| '//'~('\r' | '\n')* /* multiple comment*/
;

// ----- Entrypoint ----- 
program
   : statement+
   ;

statement
   : IF_STATEMENT paren_expr statement #IfStatement
   | IF_STATEMENT paren_expr statement ELSE_STATEMENT statement #IfElseStatement
   | WHILE_STATEMENT paren_expr statement #WhileStatement
   | DO_STATEMENT statement WHILE_STATEMENT paren_expr #DoWhileStatement
   | BLOCK_STATEMENT_START statement* BLOCK_STATEMENT_END #BlockStatement
   | variableName ASSIGN (expr|paren_expr) END_OF_STATEMENT #AssignmentStatement
   | expr END_OF_STATEMENT #ExpressionStatement
   | END_OF_STATEMENT #EmptyStatement
   ;

paren_expr
   : '(' expr ')'
   ;

expr
   : term
   | test
   | paren_expr
   ;

test
   : term
   | term op=(GREATER | LOWER | EQUAL | GREATEREQUAL | LOWEREQUAL) term
   ;

term
   : string
   | term op=(ADD | SUB) term
   | integer
   | variableName
   ;

variableName
   : STRING
   ;

string
   : STRING_ENCLOSURE STRING STRING_ENCLOSURE
   ;

integer
   : INT
   ;


INT // INT bust me before STRING so that numbers doesn't get parsed as variable names
   : [0-9]+
   ;


STRING
   : [a-zA-Z]+
   ;


WS
: ( [ \r\n\t]+ | COMMENT) -> skip
;

NEWLINE
   : '\r'? '\n'
   ;