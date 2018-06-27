grammar memmap ;

r : (datasource|memmap|annotate)* EOF ;

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
variant : NAME | number | string_ | boolean_ ;
number : DECIMAL | HEXNUM ;
string_ : QUOTED ;
boolean_ : BOOLEAN_ ;
list_ : variant (',' variant)*  ;

annotate : ANNOTATE '{' (label | comment)* '}' ;
label :  aaddress ('(' lflags+ ')')? lname lflags* ;
lflags : 'i' ;
laddress : HEXNUM ;
lname : NAME ;
comment : aaddress cpos? ctext;
cpos : '^' | 'v' | '>' ;
ctext : QUOTED | TQUOTED;

// ------- LEXER ------- //

LINECOMMENT : '//' ~[\r\n]* -> skip ;
BLOCKCOMMENT : '/*' .*? '*/' -> skip ;

DATASOURCE : 'datasource' ;
FILE : 'file' ;
MEMMAP : 'memmap' ;
ANNOTATE : 'annotate' ;

BOOLEAN_ : 'True' | 'False' ;
DECIMAL : [0-9]+ ;
HEXNUM : '$' [0-9a-fA-F]+ ;

fragment NAMEFIRST : [a-zA-Z\-_] ;
fragment NAMEREST : [0-9a-zA-Z\-_] ;
NAME : NAMEFIRST NAMEREST* ;

fragment SQUOTED : '\'' (~['\r\n])* '\'' ;
fragment DQUOTED : '"' (~["\r\n])* '"' ;
QUOTED : SQUOTED | DQUOTED ;
TQUOTED : '\'\'\'' .*? '\'\'\'' ;

WS : [ \t\r\n]+ -> skip ;
