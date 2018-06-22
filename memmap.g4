grammar memmap ;

r : (datasource|memmap)+ EOF ;

datasource : DATASOURCE dsname '{' dsentry '}' ;
dsname : NAME ;
dsentry : FILE '=' dsfile ;
dsfile : QUOTED ;

memmap : MEMMAP mmname ('(' mmdatasource ')')? mmbody? ;
mmname : NAME ;
mmdatasource : NAME ;
mmbody : '{' mmentry* '}' ;
mmentry : mmrange mmdecoder ('<' mmdataaddr)? properties? ;
mmrange : mmfirst '-' mmlast ;
mmdataaddr : mmfromaddr | mmfromreset;
mmfromaddr : number ;
mmfromreset : '*' ;
mmdecoder : NAME ;
mmfirst : number ;
mmlast : number ;

properties : '{' propentry* '}' ;
propentry : propname '=' propval ;
propname : NAME ;
propval : (variant | list_) ;
number : DECIMAL | HEXNUM ;
variant : NAME | number | QUOTED ;
list_ : variant (',' variant)*  ;

// ------- LEXER ------- //

DATASOURCE : 'datasource' ;
FILE : 'file' ;
MEMMAP: 'memmap' ;

DECIMAL : [0-9]+ ;
HEXNUM : '$' [0-9a-fA-F]+ ;

fragment NAMEFIRST : [a-zA-Z\-_] ;
fragment NAMEREST : [0-9a-zA-Z\-_] ;
NAME : NAMEFIRST NAMEREST* ;

fragment SQUOTED : '\'' (~['\r\n])* '\'' ;
fragment DQUOTED : '"' (~["\r\n])* '"' ;
QUOTED: SQUOTED | DQUOTED ;

WS : [ \t\r\n]+ -> skip ;
