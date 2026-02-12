parser grammar qutes_parser;

options {
   tokenVocab = qutes_lexer;
}

// ----- Entrypoint -----
program
   : statement* EOF
   ;

statement
   : IF_STATEMENT expr statement #IfStatement
   | IF_STATEMENT expr statement ELSE_STATEMENT statement #IfElseStatement
   | WHILE_STATEMENT expr statement #WhileStatement
   | FOR_STATEMENT qualifiedName (COMMA qualifiedName)? IN_STATEMENT expr (PARALLEL)? statement #ForeachStatement
   | DO_STATEMENT statement WHILE_STATEMENT expr #DoWhileStatement
   | CURLY_PARENTHESIS_OPEN statement* CURLY_PARENTHESIS_CLOSE #BlockStatement
   | variableType qualifiedName ROUND_PARENTHESIS_OPEN functionDeclarationParams? ROUND_PARENTHESIS_CLOSE statement #FunctionDeclarationStatement
   | variableDeclaration #DeclarationStatement
   //TODO: now that this return a statement we can have something that return null.
   // plus we should understand (for uniformity) if we want to move AssignmentStatement to expre
   // or if we want to handle statement instead of expr even in other statements.
   | expr ASSIGN statement #AssignmentStatement
   | RETURN expr? END_OF_STATEMENT #ReturnStatement
   | YIELD expr END_OF_STATEMENT #YieldStatement
   | BREAK END_OF_STATEMENT #BreakStatement
   | expr END_OF_STATEMENT #ExpressionStatement
   | (MEASURE | BARRIER | PRINT) #FactStatement
   | END_OF_STATEMENT #EmptyStatement
   ;

functionDeclarationParams
   : variableDeclaration (COMMA variableDeclaration)*
   ;

variableDeclaration
   : variableType qualifiedName (ASSIGN statement)?
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
   // Unary and Multiple quantum operators
   | op=(PRINT | PAULIY | PAULIZ | HADAMARD | MEASURE) expr #UnaryOperator
   | op=(SWAP | CNOT) expr COMMA expr #DoubleUnaryOperator
   | op=(MCX | MCZ | MCY | HADAMARD | MEASURE | BARRIER | SWAP) termList #MultipleUnaryOperator
   | op=MCP termList BY expr #MultipleUnaryPhaseOperator
   // Range operator (start..end, start.., ..end, ..)
   | expr RANGE_OPERATOR expr (COLON expr)? #RangeFullExpression
   | expr RANGE_OPERATOR (COLON expr)? #RangeFromExpression
   | RANGE_OPERATOR expr (COLON expr)? #RangeToExpression
   | RANGE_OPERATOR (COLON expr)? #RangeExpression
   // Search and Grover operators
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
   | RANGE_TYPE
   | FUNCTION_TYPE
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
   : CANON_QUBIT
   | boolean QUANTUM_SUFFIX
   | CURLY_PARENTHESIS_OPEN boolean (COMMA boolean)? CURLY_PARENTHESIS_CLOSE QUANTUM_SUFFIX
   | CURLY_PARENTHESIS_OPEN float (COMMA float)? CURLY_PARENTHESIS_CLOSE QUANTUM_SUFFIX
   ;

quint
   : integer QUANTUM_SUFFIX
   | CURLY_PARENTHESIS_OPEN integer (COMMA integer)* CURLY_PARENTHESIS_CLOSE QUANTUM_SUFFIX
   | CURLY_PARENTHESIS_OPEN integer RANGE_OPERATOR integer (COLON integer)? CURLY_PARENTHESIS_CLOSE QUANTUM_SUFFIX
   ;

quchar
   : char QUANTUM_SUFFIX
   ;

qustring
   : string QUANTUM_SUFFIX
   ;