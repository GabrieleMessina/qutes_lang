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
   | FOREACH_STATEMENT qualifiedName (COMMA qualifiedName)? IN_STATEMENT expr statement #ForeachStatement
   | DO_STATEMENT statement WHILE_STATEMENT expr #DoWhileStatement
   | CURLY_PARENTHESIS_OPEN statement* CURLY_PARENTHESIS_CLOSE #BlockStatement
   | variableType qualifiedName ROUND_PARENTHESIS_OPEN functionDeclarationParams? ROUND_PARENTHESIS_CLOSE statement #FunctionDeclarationStatement
   | variableDeclaration END_OF_STATEMENT #DeclarationStatement
   | expr ASSIGN expr END_OF_STATEMENT #AssignmentStatement
   | RETURN expr? END_OF_STATEMENT #ReturnStatement
   | BREAK END_OF_STATEMENT #BreakStatement
   | expr END_OF_STATEMENT #ExpressionStatement
   | (MEASURE | BARRIER | PRINT) #FactStatement
   | END_OF_STATEMENT #EmptyStatement
   ;

functionDeclarationParams
   : variableDeclaration (COMMA variableDeclaration)*
   ;

variableDeclaration
   : variableType qualifiedName (ASSIGN expr)?
   ;

expr // Order: https://en.wikipedia.org/wiki/Order_of_operations#Programming_languages
   : ROUND_PARENTHESIS_OPEN expr ROUND_PARENTHESIS_CLOSE #ParentesizeExpression
   | literal #LiteralExpression
   | qualifiedName #QualifiedNameExpression
   | SQUARE_PARENTHESIS_OPEN termList SQUARE_PARENTHESIS_CLOSE #ArrayExpression
   // Function call, scope, array/member access
   | qualifiedName ROUND_PARENTHESIS_OPEN termList? ROUND_PARENTHESIS_CLOSE #FunctionCallExpression
   | expr SQUARE_PARENTHESIS_OPEN expr SQUARE_PARENTHESIS_CLOSE #ArrayAccessExpression
   // Unary operators, sizeof and type casts
   | expr op=(AUTO_INCREMENT | AUTO_DECREMENT) #PostfixOperator
   | expr op=EXP expr #ExpOperator
   | op=(NOT | ADD | SUB | AUTO_INCREMENT | AUTO_DECREMENT) expr #PrefixOperator
   // Multiplication, division, modulo
   | expr op=(MULTIPLY | DIVIDE | MODULE) expr #MultiplicativeOperator
   // Addition and subtraction
   | expr op=(ADD | SUB) expr #SumOperator
   // Bitwise shift left and right
   | expr op=(LSHIFT | RSHIFT) expr #ShiftOperator
   // Comparisons less-greater, then, equallity, inequality
   | expr op=(GREATEREQUAL | LOWEREQUAL | GREATER | LOWER ) expr #RelationalOperator
   | expr op=(EQUAL | NOT_EQUAL) expr #EqualityOperator
   // Logical AND then OR
   | expr op=AND expr #LogicAndOperator
   | expr op=OR expr #LogicOrOperator
   // Assignment and auto assignment operators | <assoc = right> expr op=(AUTO_SUM | AUTO_DECREMENT | AUTO_MODULE | AUTO_DIVIDE | AUTO_MODULE) expr #AutoAssignmentOperator
   | op=(PRINT | PAULIY | PAULIZ | HADAMARD | MEASURE) expr #UnaryOperator
   | op=(SWAP | CNOT) expr COMMA expr #DoubleUnaryOperator
   | op=(MCX | MCZ | MCY | HADAMARD | MEASURE | BARRIER | SWAP) termList #MultipleUnaryOperator
   | op=MCP termList BY expr #MultipleUnaryPhaseOperator
   | expr op=IN_STATEMENT expr #GroverOperator
   | op=GROVER expr ROUND_PARENTHESIS_OPEN termList? ROUND_PARENTHESIS_CLOSE #FreeGroverOperator
   ;
   
termList
   : expr (COMMA expr)*
   ;

variableType
   : type (SQUARE_PARENTHESIS_OPEN SQUARE_PARENTHESIS_CLOSE)?
   ;

type
   : BOOL_TYPE
   | INT_TYPE
   | CHAR_TYPE
   | FLOAT_TYPE
   | STRING_TYPE
   | QUBIT_TYPE
   | QUINT_TYPE
   | QUCHAR_TYPE
   | QUSTRING_TYPE
   | VOID_TYPE
   ;

qualifiedName 
   : SYMBOL_LITERAL (DOT SYMBOL_LITERAL)*
   ;

literal
   : boolean
   | integer
   | char
   | float
   | qubit
   | quint
   | quchar
   | qustring
   | string
   ;

boolean
   : BOOL_LITERAL
   ;

integer
   : INT_LITERAL
   | BIN_LITERAL
   | HEX_LITERAL
   ;

char
   : CHAR_LITERAL
   ;

float
   : FLOAT_LITERAL
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

quchar
   : QUCHAR_LITERAL
   ;

qustring
   : QUSTRING_LITERAL
   ;