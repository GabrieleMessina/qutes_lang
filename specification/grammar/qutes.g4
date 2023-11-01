grammar qutes;

options {
   language = Python3;
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
BLOCK_STATEMENT_START : '{' ;
BLOCK_STATEMENT_END : '}' ;
STRING_ENCLOSURE : '"' ;
END_OF_PROGRAM : EOF ;

type
   : INT_TYPE
   | STRING_TYPE
   | QUBIT_TYPE
   ;

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
   : IF_STATEMENT parenExpr statement #IfStatement
   | IF_STATEMENT parenExpr statement ELSE_STATEMENT statement #IfElseStatement
   | WHILE_STATEMENT parenExpr statement #WhileStatement
   | DO_STATEMENT statement WHILE_STATEMENT parenExpr #DoWhileStatement
   | BLOCK_STATEMENT_START statement* BLOCK_STATEMENT_END #BlockStatement
   | variableType variableName ASSIGN (expr|parenExpr) END_OF_STATEMENT #DeclarationStatement
   | qualifiedName ASSIGN (expr|parenExpr) END_OF_STATEMENT #AssignmentStatement
   | expr END_OF_STATEMENT #ExpressionStatement
   | END_OF_STATEMENT #EmptyStatement
   ;

parenExpr
   : '(' expr ')'
   ;

expr
   : term
   | test
   | parenExpr
   ;

test
   : term
   | term op=(GREATER | LOWER | EQUAL | GREATEREQUAL | LOWEREQUAL) term
   ;

term
   : string
   | term op=(ADD | SUB) term
   | integer
   | qualifiedName
   ;

variableType
   : type
   | qualifiedName
   ;

qualifiedName 
   : STRING ('.' STRING)*
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