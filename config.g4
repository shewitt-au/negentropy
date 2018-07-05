grammar config ;

r : WS* (toplevel (WS+ toplevel)*)? WS* EOF ;
toplevel : datasource|memmap|annotate ;

datasource : DATASOURCE WS+ dsname? WS* properties? ;
dsname : NAME ;

memmap : MEMMAP WS+ mmname WS* ('(' WS* mmdatasource WS* ')')? WS* mmbody? ;
mmname : NAME ;
mmdatasource : NAME ;
mmbody : '{' WS* (mmentry (WS+ mmentry)*)? WS* '}' ;
mmentry : range_ WS+ mmdecoder (WS* '<' mmdataaddr)? WS* properties? ;
mmdataaddr : mmfromaddr | mmfromreset;
mmfromaddr : number ;
mmfromreset : '*' ;
mmdecoder : NAME ;
mmfirst : number ;
mmlast : number ;

properties : '{' WS* (propentry (WS+ propentry)*)? WS* '}' ;
propentry : propname WS* '=' WS* propval ;
propname : NAME ;
propval : (variant | list_) ;
variant : NAME | number | string_ | boolean_ ;
number : DECIMAL | HEXNUM ;
string_ : QUOTED ;
boolean_ : BOOLEAN_ ;
list_ : variant WS* (',' WS* variant)*  ;

annotate : ANNOTATE WS* '{' WS* (atoplevel (WS+ atoplevel)*)? WS* '}' ;
atoplevel : label | comment ;
label :  range_ WS* ('(' lflags+ ')')? WS+ lname WS* ;
lflags : 'i' ;
lname : NAME ;
comment : aaddress WS* cpos? WS* ctext;
aaddress : range_ ;
cpos : '^' | 'v' | '>' ;
ctext : QUOTED | TQUOTED ;

range_ :
	(range_single) | 
	(range_first WS* '-' WS* range_last)
	;
range_single : number ;
range_first : number ;
range_last : number ;

// ------- LEXER ------- //

LINECOMMENT : '//' ~[\r\n]* -> skip ;
BLOCKCOMMENT : '/*' .*? '*/' -> skip ;

DATASOURCE : 'datasource' ;
MEMMAP : 'memmap' ;
ANNOTATE : 'annotate' ;

BOOLEAN_ : 'True' | 'False' ;
DECIMAL : [0-9]+ ;
HEXNUM : '$' [0-9a-fA-F]+ ;

fragment NAMEFIRST : [a-zA-Z_] ;
fragment NAMEREST : [0-9a-zA-Z\-_] ;
NAME : NAMEFIRST NAMEREST* ;

fragment SQUOTED : '\'' (~['\r\n])* '\'' ;
fragment DQUOTED : '"' (~["\r\n])* '"' ;
QUOTED : SQUOTED | DQUOTED ;
TQUOTED : '\'\'\'' .*? '\'\'\'' ;

WS : [ \t\r\n] ;
