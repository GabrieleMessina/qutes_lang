grammar Qutes;

program: (function | statement | inputDeclaration)* EOF;
inputDeclaration: 'input' type IDENT ';';
function: type IDENT '(' parameters? ')' block;
parameters: parameter (',' parameter)*;
parameter: type IDENT;
type: typeName ('[' ']')?;
typeName: 'bool' | 'int' | 'char' | 'string' | 'void'
        | 'qubit' | 'quint' | 'quchar' | 'qustring';
block: '{' statement* '}';
statement: block
         | declaration ';'
         | simple ';'
         | ifStatement
         | 'while' '(' expression ')' block
         | 'for' '(' initializer? ';' condition=expression? ';' update=simple? ')' block
         | 'foreach' '(' type IDENT 'in' expression ')' block
         | 'return' expression? ';';
initializer: declaration | simple;
declaration: type IDENT '=' expression;
simple: expression (('=' | '+=' | '-=') expression | '++' | '--')?;
ifStatement: 'if' '(' expression ')' block ('else' (block | ifStatement))?;
expression: logicalOr;
logicalOr: logicalAnd ('||' logicalAnd)*;
logicalAnd: equality ('&&' equality)*;
equality: comparison (('==' | '!=') comparison)*;
comparison: addition (('<' | '<=' | '>' | '>=' | 'in') addition)*;
addition: multiplication (('+' | '-') multiplication)*;
multiplication: unary (('*' | '/' | '%') unary)*;
unary: ('!' | '-' | '+')* postfix;
postfix: primary suffix*;
suffix: '(' arguments? ')' | '[' expression ']' | '.' IDENT;
arguments: expression (',' expression)*;
primary: INT | STRING | CHAR | 'true' | 'false' | IDENT
       | '(' expression ')' | '[' arguments? ']'
       | 'new' typeName '[' expression ']';
IDENT: [A-Za-z_] [A-Za-z_0-9]*;
INT: [0-9]+;
// Decode/validate escapes in the AST adapter, including Unicode scalar checks.
STRING: '"' ('\\' ~[\r\n] | ~["\\\r\n])* '"';
CHAR: '\'' ('\\' ~[\r\n] | ~['\\\r\n])* '\'';
LINE_COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
UNTERMINATED_COMMENT: '/*' (~[*] | '*'+ ~[*/])* '*'* EOF;
UNTERMINATED_STRING: '"' ('\\' ~[\r\n] | ~["\\\r\n])*;
UNTERMINATED_CHAR: '\'' ('\\' ~[\r\n] | ~['\\\r\n])*;
WS: [ \t\r\n]+ -> skip;
INVALID: .;
