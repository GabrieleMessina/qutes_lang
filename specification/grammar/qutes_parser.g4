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
   | variableType functionName ROUND_PARENTHESIS_OPEN functionDeclarationParams? ROUND_PARENTHESIS_CLOSE statement #FunctionStatement
   | variableDeclaration END_OF_STATEMENT #DeclarationStatement
   | qualifiedName ASSIGN expr END_OF_STATEMENT #AssignmentStatement
   | RETURN expr END_OF_STATEMENT #ReturnStatement
   | expr END_OF_STATEMENT #ExpressionStatement
   | (MEASURE | BARRIER) #FactStatement
   | END_OF_STATEMENT #EmptyStatement
   ;

functionDeclarationParams
   : variableDeclaration (COMMA functionDeclarationParams)?
   ;

variableDeclaration
   : variableType variableName (ASSIGN expr)?
   ;

expr // Order: https://en.wikipedia.org/wiki/Order_of_operations#Programming_languages
   : ROUND_PARENTHESIS_OPEN expr ROUND_PARENTHESIS_CLOSE #ParentesizeExpression
   | literal #LiteralExpression
   | qualifiedName #QualifiedNameExpression
   // Array access
   | functionName ROUND_PARENTHESIS_OPEN functionCallParams? ROUND_PARENTHESIS_CLOSE #FunctionCallExpression
   | expr op=(AUTO_INCREMENT | AUTO_DECREMENT) #PostfixOperator
   | op=(NOT | ADD | SUB | AUTO_INCREMENT | AUTO_DECREMENT) expr #PrefixOperator
   // cast operation
   | expr op=(MULTIPLY | DIVIDE | MODULE) expr #MultiplicativeOperator
   | expr op=(ADD | SUB) expr #SumOperator
   | expr op=(LSHIFT | RSHIFT) expr #ShiftOperator
   | expr op=(GREATEREQUAL | LOWEREQUAL | GREATER | LOWER ) expr #RelationalOperator
   | expr op=(EQUAL | NOT_EQUAL) expr #EqualityOperator
   | expr op=AND expr #LogicAndOperator
   | expr op=OR expr #LogicOrOperator
   // | <assoc = right> expr op=(AUTO_SUM | AUTO_DECREMENT | AUTO_MODULE | AUTO_DIVIDE | AUTO_MODULE) expr #AutoAssignmentOperator
   | op=(MCX | MCZ | MCY | SWAP) termList #MultipleUnaryOperator
   | op=(PRINT | PAULIY | PAULIZ | HADAMARD | MEASURE) expr #UnaryOperator
   | op=MCP termList BY expr #MultipleUnaryPhaseOperator
   | termList op=IN_STATEMENT qualifiedName #GroverOperator
   ;

functionCallParams
   : (literal | qualifiedName) (COMMA functionCallParams)?
   ;

termList
   : (literal | qualifiedName) (COMMA termList)?
   ;

variableType
   : type
   | qualifiedName
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

qualifiedName 
   : SYMBOL_LITERAL (DOT SYMBOL_LITERAL)*
   | variableName
   | functionName
   ;

variableName
   : SYMBOL_LITERAL
   ;

functionName
   : SYMBOL_LITERAL
   ;

literal
   : boolean
   | integer
   | float
   | qubit
   | quint
   | qustring
   | string
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