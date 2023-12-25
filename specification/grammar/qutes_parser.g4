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
   : IF_STATEMENT expr statement #IfStatement
   | IF_STATEMENT expr statement ELSE_STATEMENT statement #IfElseStatement
   | WHILE_STATEMENT expr statement #WhileStatement
   | DO_STATEMENT statement WHILE_STATEMENT expr #DoWhileStatement
   | CURLY_PARENTHESIS_OPEN statement* CURLY_PARENTHESIS_CLOSE #BlockStatement
   | variableType variableName (ASSIGN expr)? END_OF_STATEMENT #DeclarationStatement //TODO: rename variableName to variableDeclarationName
   | qualifiedName ASSIGN expr END_OF_STATEMENT #AssignmentStatement
   | expr END_OF_STATEMENT #ExpressionStatement
   | END_OF_STATEMENT #EmptyStatement
   ;

expr
   : term
   | test
   | parenExpr
   ;

parenExpr
   : ROUND_PARENTHESIS_OPEN expr ROUND_PARENTHESIS_CLOSE
   ;

test
   : term
   | term op=(GREATER | LOWER | EQUAL | GREATEREQUAL | LOWEREQUAL) term
   ;

term
   : term op=(ADD | SUB) term #BinaryOperator
   | op=(NOT | PAULIY | PAULIZ | HADAMARD | MEASURE | ADD | SUB) term #UnaryOperator
   | (boolean
   | integer
   | float
   | qubit
   | quint
   | qualifiedName
   | string) #IdentityOperator
   ;

type
   : INT_TYPE
   | BOOL_TYPE
   | FLOAT_TYPE
   | STRING_TYPE
   | QUBIT_TYPE
   | QUINT_TYPE
   ;

variableType
   : type
   | qualifiedName
   ;

qualifiedName 
   : SYMBOL_LITERAL (DOT SYMBOL_LITERAL)*
   ;

variableName
   : SYMBOL_LITERAL
   ;

string
   : STRING_LITERAL
   ;

qubit
   : QUBIT_LITERAL
   ;

quint
   : QUINT_LITERAL
   ;

float
   : FLOAT_LITERAL
   ;

integer
   : INT_LITERAL
   | BIN_LITERAL
   | HEX_LITERAL
   ;

boolean
   : BOOl_LITERAL
   ;