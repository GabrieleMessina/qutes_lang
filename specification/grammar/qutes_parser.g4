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
   | block #BlockStatement
   | variableType functionName ROUND_PARENTHESIS_OPEN functionDeclarationParams? ROUND_PARENTHESIS_CLOSE statement #FunctionStatement
   | variableDeclaration END_OF_STATEMENT #DeclarationStatement
   | qualifiedName ASSIGN expr END_OF_STATEMENT #AssignmentStatement
   | RETURN expr END_OF_STATEMENT #ReturnStatement
   | expr END_OF_STATEMENT #ExpressionStatement
   | END_OF_STATEMENT #EmptyStatement
   ;

block
   : CURLY_PARENTHESIS_OPEN statement* CURLY_PARENTHESIS_CLOSE
   ;

functionDeclarationParams
   : variableDeclaration (COMMA functionDeclarationParams)?
   ;

//TODO: rename variableName to variableDeclarationName
variableDeclaration
   : variableType variableName (ASSIGN expr)?
   ;

functionCallParams
   : qualifiedName (COMMA functionCallParams)?
   ;

expr
   : term
   | functionCall
   | test
   | parenExpr
   | groverExpr
   ;

groverExpr
   : termList op=IN_STATEMENT qualifiedName
   ;

functionCall //Function name should be a qualifiedName here.
   : functionName ROUND_PARENTHESIS_OPEN functionCallParams? ROUND_PARENTHESIS_CLOSE
   ;

parenExpr
   : ROUND_PARENTHESIS_OPEN expr ROUND_PARENTHESIS_CLOSE
   ;

test
   : term
   | term op=(GREATER | LOWER | EQUAL | GREATEREQUAL | LOWEREQUAL) term
   ;

term
   : term op=(MULTIPLY | DIVIDE) term #BinaryPriorityOperator
   | term op=(ADD | SUB) term #BinaryOperator
   | op=(PRINT | NOT | PAULIY | PAULIZ | HADAMARD | MEASURE | ADD | SUB) term #UnaryOperator
   | op=(MCX | MCZ | MCY | SWAP) termList #MultipleUnaryOperator
   | op=MCP termList BY expr #MultipleUnaryPhaseOperator
   | (boolean
   | integer
   | float
   | qubit
   | quint
   | qustring
   | qualifiedName
   | MEASURE
   | BARRIER
   | string) #IdentityOperator
   ;

termList
   : term (COMMA termList)?
   ;

type
   : INT_TYPE
   | BOOL_TYPE
   | FLOAT_TYPE
   | STRING_TYPE
   | QUBIT_TYPE
   | QUINT_TYPE
   | QUSTRING_TYPE
   | VOID_TYPE
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

functionName
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

qustring
   : QUSTRING_LITERAL
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
   : BOOL_LITERAL
   ;