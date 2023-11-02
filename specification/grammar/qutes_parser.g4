parser grammar qutes_parser;

options {
   tokenVocab = qutes_lexer;
   language = Python3;
}

// ----- Entrypoint -----
program
   : statement* EOF
   ;

statement
   : IF_STATEMENT parenExpr statement #IfStatement
   | IF_STATEMENT parenExpr statement ELSE_STATEMENT statement #IfElseStatement
   | WHILE_STATEMENT parenExpr statement #WhileStatement
   | DO_STATEMENT statement WHILE_STATEMENT parenExpr #DoWhileStatement
   | CURLY_PARENTHESIS_OPEN statement* CURLY_PARENTHESIS_CLOSE #BlockStatement
   | variableType variableName ASSIGN (expr|parenExpr) END_OF_STATEMENT #DeclarationStatement
   | qualifiedName ASSIGN (expr|parenExpr) END_OF_STATEMENT #AssignmentStatement
   | expr END_OF_STATEMENT #ExpressionStatement
   | END_OF_STATEMENT #EmptyStatement
   ;

parenExpr
   : ROUND_PARENTHESIS_OPEN expr ROUND_PARENTHESIS_CLOSE
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
   : term op=(ADD | SUB) term
   | qualifiedName
   | string
   | integer
   ;


type
   : INT_TYPE
   | STRING_TYPE
   | QUBIT_TYPE
   ;

variableType
   : type
   | qualifiedName
   ;

qualifiedName 
   : STRING (DOT STRING)*
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