from interval import Interval
from enum import Enum, unique, auto
from collections import namedtuple

# $80 - $ca
CommandInfo = namedtuple("CommandInfo", "name, num_lines, syscall")
_commands = (
	CommandInfo("END",		0,  False),		# $80
	CommandInfo("FOR",		0,  False),		# $81
	CommandInfo("NEXT",		0,  False),		# $82
	CommandInfo("DATA",		0,  False),		# $83
	CommandInfo("INPUT#",	0,  False),		# $84
	CommandInfo("INPUT",	0,  False),		# $85
	CommandInfo("DIM",		0,  False),		# $86
	CommandInfo("READ",		0,  False),		# $87
	CommandInfo("LET",		0,  False),		# $88
	CommandInfo("GOTO",		-1, False),		# $89
	CommandInfo("RUN",		1,  False),		# $8a
	CommandInfo("IF",		0,  False),		# $8b
	CommandInfo("RESTORE",	0,  False),		# $8c
	CommandInfo("GOSUB",	-1, False),		# $8d
	CommandInfo("RETURN",	0,  False),		# $8e
	CommandInfo("REM",		0,  False),		# $8f
	CommandInfo("STOP",		0,  False),		# $90
	CommandInfo("ON",		0,  False),		# $91
	CommandInfo("WAIT",		0,  False),		# $92
	CommandInfo("LOAD",		0,  False),		# $93
	CommandInfo("SAVE",		0,  False),		# $94
	CommandInfo("VERIFY",	0,  False),		# $95
	CommandInfo("DEF",		0,  False),		# $96
	CommandInfo("POKE",		0,  False),		# $97
	CommandInfo("PRINT#",	0,  False),		# $98
	CommandInfo("PRINT",	0,  False),		# $99
	CommandInfo("CONT",		0,  False),		# $9a
	CommandInfo("LIST",		-1, False),		# $9b
	CommandInfo("CLR",		0,  False),		# $9c
	CommandInfo("CMD",		0,  False),		# $9d
	CommandInfo("SYS",		0,  True),		# $9e
	CommandInfo("OPEN",		0,  False),		# $9f
	CommandInfo("CLOSE",	0,  False),		# $a0
	CommandInfo("GET",		0,  False),		# $a1
	CommandInfo("NEW",		0,  False),		# $a2
	CommandInfo("TAB(",		0,  False),		# $a3
	CommandInfo("TO",		0,  False),		# $a4
	CommandInfo("FN",		0,  False),		# $a5
	CommandInfo("SPC(",		0,  False),		# $a6
	CommandInfo("THEN",		1,  False),		# $a7
	CommandInfo("NOT",		0,  False),		# $a8
	CommandInfo("STEP",		0,  False),		# $a9
	CommandInfo("+",		0,  False),		# $aa
	CommandInfo("-",		0,  False),		# $ab
	CommandInfo("*",		0,  False),		# $ac
	CommandInfo("/",		0,  False),		# $ad
	CommandInfo("↑",		0,  False),		# $ae
	CommandInfo("AND",		0,  False),		# $af
	CommandInfo("OR",		0,  False),		# $b0
	CommandInfo(">",		0,  False),		# $b1
	CommandInfo("=",		0,  False),		# $b2
	CommandInfo("<",		0,  False),		# $b3
	CommandInfo("SGN",		0,  False),		# $b4
	CommandInfo("INT",		0,  False),		# $b5
	CommandInfo("ABS",		0,  False),		# $b6
	CommandInfo("USR",		0,  False),		# $b7
	CommandInfo("FRE",		0,  False),		# $b7
	CommandInfo("POS",		0,  False),		# $b9
	CommandInfo("SQR",		0,  False),		# $ba
	CommandInfo("RND",		0,  False),		# $bb
	CommandInfo("LOG",		0,  False),		# $bc
	CommandInfo("EXP",		0,  False),		# $bd
	CommandInfo("COS",		0,  False),		# $be
	CommandInfo("SIN",		0,  False),		# $bf
	CommandInfo("TAN",		0,  False),		# $c0
	CommandInfo("ATN",		0,  False),		# $c1
	CommandInfo("PEEK",		0,  False),		# $c2
	CommandInfo("LEN",		0,  False),		# $c3
	CommandInfo("STR$",		0,  False),		# $c4
	CommandInfo("VAL",		0,  False),		# $c5
	CommandInfo("ASC",		0,  False),		# $c6
	CommandInfo("CHR$",		0,  False),		# $c7
	CommandInfo("LEFT$",	0,  False),		# $c8
	CommandInfo("RIGHT$",	0,  False),		# $c9
	CommandInfo("MID$",		0,  False)		# $ca
	#
	#CommandInfo("\u03C0)",		0,  False)		# $ff PI symmol
)

def command(token):
	if token>=0x80 and token<=0xca:
		return _commands[token-0x80]
	elif token==0xff:
		return CommandInfo("\u03C0", 0,  False)		# $ff PI symmol
	else:
		return CommandInfo("?", 0, False)

# From cbmcodecs: https://pypi.org/project/cbmcodecs/
_decoding_table = (
	'\ufffe'    #  0x00 -> UNDEFINED
	'\ufffe'    #  0x01 -> UNDEFINED
	'\ufffe'    #  0x02 -> UNDEFINED
	'\ufffe'    #  0x03 -> UNDEFINED
	'\ufffe'    #  0x04 -> UNDEFINED
	'\uf100'    #  0x05 -> WHITE COLOR SWITCH (CUS)
	'\ufffe'    #  0x06 -> UNDEFINED
	'\ufffe'    #  0x07 -> UNDEFINED
	'\uf118'    #  0x08 -> DISABLE CHARACTER SET SWITCHING (CUS)
	'\uf119'    #  0x09 -> ENABLE CHARACTER SET SWITCHING (CUS)
	'\ufffe'    #  0x0A -> UNDEFINED
	'\ufffe'    #  0x0B -> UNDEFINED
	'\ufffe'    #  0x0C -> UNDEFINED
	'\r'        #  0x0D -> CARRIAGE RETURN
	'\x0e'      #  0x0E -> SHIFT OUT
	'\ufffe'    #  0x0F -> UNDEFINED
	'\ufffe'    #  0x10 -> UNDEFINED
	'\uf11c'    #  0x11 -> CURSOR DOWN (CUS)
	'\uf11a'    #  0x12 -> REVERSE VIDEO ON (CUS)
	'\uf120'    #  0x13 -> HOME (CUS)
	'\x7f'      #  0x14 -> DELETE
	'\ufffe'    #  0x15 -> UNDEFINED
	'\ufffe'    #  0x16 -> UNDEFINED
	'\ufffe'    #  0x17 -> UNDEFINED
	'\ufffe'    #  0x18 -> UNDEFINED
	'\ufffe'    #  0x19 -> UNDEFINED
	'\ufffe'    #  0x1A -> UNDEFINED
	'\ufffe'    #  0x1B -> UNDEFINED
	'\uf101'    #  0x1C -> RED COLOR SWITCH (CUS)
	'\uf11d'    #  0x1D -> CURSOR RIGHT (CUS)
	'\uf102'    #  0x1E -> GREEN COLOR SWITCH (CUS)
	'\uf103'    #  0x1F -> BLUE COLOR SWITCH (CUS)
	' '         #  0x20 -> SPACE
	'!'         #  0x21 -> EXCLAMATION MARK
	'"'         #  0x22 -> QUOTATION MARK
	'#'         #  0x23 -> NUMBER SIGN
	'$'         #  0x24 -> DOLLAR SIGN
	'%'         #  0x25 -> PERCENT SIGN
	'&'         #  0x26 -> AMPERSAND
	"'"         #  0x27 -> APOSTROPHE
	'('         #  0x28 -> LEFT PARENTHESIS
	')'         #  0x29 -> RIGHT PARENTHESIS
	'*'         #  0x2A -> ASTERISK
	'+'         #  0x2B -> PLUS SIGN
	','         #  0x2C -> COMMA
	'-'         #  0x2D -> HYPHEN-MINUS
	'.'         #  0x2E -> FULL STOP
	'/'         #  0x2F -> SOLIDUS
	'0'         #  0x30 -> DIGIT ZERO
	'1'         #  0x31 -> DIGIT ONE
	'2'         #  0x32 -> DIGIT TWO
	'3'         #  0x33 -> DIGIT THREE
	'4'         #  0x34 -> DIGIT FOUR
	'5'         #  0x35 -> DIGIT FIVE
	'6'         #  0x36 -> DIGIT SIX
	'7'         #  0x37 -> DIGIT SEVEN
	'8'         #  0x38 -> DIGIT EIGHT
	'9'         #  0x39 -> DIGIT NINE
	':'         #  0x3A -> COLON
	';'         #  0x3B -> SEMICOLON
	'<'         #  0x3C -> LESS-THAN SIGN
	'='         #  0x3D -> EQUALS SIGN
	'>'         #  0x3E -> GREATER-THAN SIGN
	'?'         #  0x3F -> QUESTION MARK
	'@'         #  0x40 -> COMMERCIAL AT
	'A'         #  0x41 -> LATIN CAPITAL LETTER A
	'B'         #  0x42 -> LATIN CAPITAL LETTER B
	'C'         #  0x43 -> LATIN CAPITAL LETTER C
	'D'         #  0x44 -> LATIN CAPITAL LETTER D
	'E'         #  0x45 -> LATIN CAPITAL LETTER E
	'F'         #  0x46 -> LATIN CAPITAL LETTER F
	'G'         #  0x47 -> LATIN CAPITAL LETTER G
	'H'         #  0x48 -> LATIN CAPITAL LETTER H
	'I'         #  0x49 -> LATIN CAPITAL LETTER I
	'J'         #  0x4A -> LATIN CAPITAL LETTER J
	'K'         #  0x4B -> LATIN CAPITAL LETTER K
	'L'         #  0x4C -> LATIN CAPITAL LETTER L
	'M'         #  0x4D -> LATIN CAPITAL LETTER M
	'N'         #  0x4E -> LATIN CAPITAL LETTER N
	'O'         #  0x4F -> LATIN CAPITAL LETTER O
	'P'         #  0x50 -> LATIN CAPITAL LETTER P
	'Q'         #  0x51 -> LATIN CAPITAL LETTER Q
	'R'         #  0x52 -> LATIN CAPITAL LETTER R
	'S'         #  0x53 -> LATIN CAPITAL LETTER S
	'T'         #  0x54 -> LATIN CAPITAL LETTER T
	'U'         #  0x55 -> LATIN CAPITAL LETTER U
	'V'         #  0x56 -> LATIN CAPITAL LETTER V
	'W'         #  0x57 -> LATIN CAPITAL LETTER W
	'X'         #  0x58 -> LATIN CAPITAL LETTER X
	'Y'         #  0x59 -> LATIN CAPITAL LETTER Y
	'Z'         #  0x5A -> LATIN CAPITAL LETTER Z
	'['         #  0x5B -> LEFT SQUARE BRACKET
	'\xa3'      #  0x5C -> POUND SIGN
	']'         #  0x5D -> RIGHT SQUARE BRACKET
	'\u2191'    #  0x5E -> UPWARDS ARROW
	'\u2190'    #  0x5F -> LEFTWARDS ARROW
	'\u2500'    #  0x60 -> BOX DRAWINGS LIGHT HORIZONTAL
	'\u2660'    #  0x61 -> BLACK SPADE SUIT
	'\u2502'    #  0x62 -> BOX DRAWINGS LIGHT VERTICAL
	'\u2500'    #  0x63 -> BOX DRAWINGS LIGHT HORIZONTAL
	'\uf122'    #  0x64 -> BOX DRAWINGS LIGHT HORIZONTAL ONE QUARTER UP (CUS)
	'\uf123'    #  0x65 -> BOX DRAWINGS LIGHT HORIZONTAL TWO QUARTERS UP (CUS)
	'\uf124'    #  0x66 -> BOX DRAWINGS LIGHT HORIZONTAL ONE QUARTER DOWN (CUS)
	'\uf126'    #  0x67 -> BOX DRAWINGS LIGHT VERTICAL ONE QUARTER LEFT (CUS)
	'\uf128'    #  0x68 -> BOX DRAWINGS LIGHT VERTICAL ONE QUARTER RIGHT (CUS)
	'\u256e'    #  0x69 -> BOX DRAWINGS LIGHT ARC DOWN AND LEFT
	'\u2570'    #  0x6A -> BOX DRAWINGS LIGHT ARC UP AND RIGHT
	'\u256f'    #  0x6B -> BOX DRAWINGS LIGHT ARC UP AND LEFT
	'\uf12a'    #  0x6C -> ONE EIGHTH BLOCK UP AND RIGHT (CUS)
	'\u2572'    #  0x6D -> BOX DRAWINGS LIGHT DIAGONAL UPPER LEFT TO LOWER RIGHT
	'\u2571'    #  0x6E -> BOX DRAWINGS LIGHT DIAGONAL UPPER RIGHT TO LOWER LEFT
	'\uf12b'    #  0x6F -> ONE EIGHTH BLOCK DOWN AND RIGHT (CUS)
	'\uf12c'    #  0x70 -> ONE EIGHTH BLOCK DOWN AND LEFT (CUS)
	'\u25cf'    #  0x71 -> BLACK CIRCLE
	'\uf125'    #  0x72 -> BOX DRAWINGS LIGHT HORIZONTAL TWO QUARTERS DOWN (CUS)
	'\u2665'    #  0x73 -> BLACK HEART SUIT
	'\uf127'    #  0x74 -> BOX DRAWINGS LIGHT VERTICAL TWO QUARTERS LEFT (CUS)
	'\u256d'    #  0x75 -> BOX DRAWINGS LIGHT ARC DOWN AND RIGHT
	'\u2573'    #  0x76 -> BOX DRAWINGS LIGHT DIAGONAL CROSS
	'\u25cb'    #  0x77 -> WHITE CIRCLE
	'\u2663'    #  0x78 -> BLACK CLUB SUIT
	'\uf129'    #  0x79 -> BOX DRAWINGS LIGHT VERTICAL TWO QUARTERS RIGHT (CUS)
	'\u2666'    #  0x7A -> BLACK DIAMOND SUIT
	'\u253c'    #  0x7B -> BOX DRAWINGS LIGHT VERTICAL AND HORIZONTAL
	'\uf12e'    #  0x7C -> LEFT HALF BLOCK MEDIUM SHADE (CUS)
	'\u2502'    #  0x7D -> BOX DRAWINGS LIGHT VERTICAL
	'\u03c0'    #  0x7E -> GREEK SMALL LETTER PI
	'\u25e5'    #  0x7F -> BLACK UPPER RIGHT TRIANGLE
	'\ufffe'    #  0x80 -> UNDEFINED
	'\uf104'    #  0x81 -> ORANGE COLOR SWITCH (CUS)
	'\ufffe'    #  0x82 -> UNDEFINED
	'\ufffe'    #  0x83 -> UNDEFINED
	'\ufffe'    #  0x84 -> UNDEFINED
	'\uf110'    #  0x85 -> FUNCTION KEY 1 (CUS)
	'\uf112'    #  0x86 -> FUNCTION KEY 3 (CUS)
	'\uf114'    #  0x87 -> FUNCTION KEY 5 (CUS)
	'\uf116'    #  0x88 -> FUNCTION KEY 7 (CUS)
	'\uf111'    #  0x89 -> FUNCTION KEY 2 (CUS)
	'\uf113'    #  0x8A -> FUNCTION KEY 4 (CUS)
	'\uf115'    #  0x8B -> FUNCTION KEY 6 (CUS)
	'\uf117'    #  0x8C -> FUNCTION KEY 8 (CUS)
	'\n'        #  0x8D -> LINE FEED
	'\x0f'      #  0x8E -> SHIFT IN
	'\ufffe'    #  0x8F -> UNDEFINED
	'\uf105'    #  0x90 -> BLACK COLOR SWITCH (CUS)
	'\uf11e'    #  0x91 -> CURSOR UP (CUS)
	'\uf11b'    #  0x92 -> REVERSE VIDEO OFF (CUS)
	'\x0c'      #  0x93 -> FORM FEED
	'\uf121'    #  0x94 -> INSERT (CUS)
	'\uf106'    #  0x95 -> BROWN COLOR SWITCH (CUS)
	'\uf107'    #  0x96 -> LIGHT RED COLOR SWITCH (CUS)
	'\uf108'    #  0x97 -> GRAY 1 COLOR SWITCH (CUS)
	'\uf109'    #  0x98 -> GRAY 2 COLOR SWITCH (CUS)
	'\uf10a'    #  0x99 -> LIGHT GREEN COLOR SWITCH (CUS)
	'\uf10b'    #  0x9A -> LIGHT BLUE COLOR SWITCH (CUS)
	'\uf10c'    #  0x9B -> GRAY 3 COLOR SWITCH (CUS)
	'\uf10d'    #  0x9C -> PURPLE COLOR SWITCH (CUS)
	'\uf11d'    #  0x9D -> CURSOR LEFT (CUS)
	'\uf10e'    #  0x9E -> YELLOW COLOR SWITCH (CUS)
	'\uf10f'    #  0x9F -> CYAN COLOR SWITCH (CUS)
	'\xa0'      #  0xA0 -> NO-BREAK SPACE
	'\u258c'    #  0xA1 -> LEFT HALF BLOCK
	'\u2584'    #  0xA2 -> LOWER HALF BLOCK
	'\u2594'    #  0xA3 -> UPPER ONE EIGHTH BLOCK
	'\u2581'    #  0xA4 -> LOWER ONE EIGHTH BLOCK
	'\u258f'    #  0xA5 -> LEFT ONE EIGHTH BLOCK
	'\u2592'    #  0xA6 -> MEDIUM SHADE
	'\u2595'    #  0xA7 -> RIGHT ONE EIGHTH BLOCK
	'\uf12f'    #  0xA8 -> LOWER HALF BLOCK MEDIUM SHADE (CUS)
	'\u25e4'    #  0xA9 -> BLACK UPPER LEFT TRIANGLE
	'\uf130'    #  0xAA -> RIGHT ONE QUARTER BLOCK (CUS)
	'\u251c'    #  0xAB -> BOX DRAWINGS LIGHT VERTICAL AND RIGHT
	'\u2597'    #  0xAC -> QUADRANT LOWER RIGHT
	'\u2514'    #  0xAD -> BOX DRAWINGS LIGHT UP AND RIGHT
	'\u2510'    #  0xAE -> BOX DRAWINGS LIGHT DOWN AND LEFT
	'\u2582'    #  0xAF -> LOWER ONE QUARTER BLOCK
	'\u250c'    #  0xB0 -> BOX DRAWINGS LIGHT DOWN AND RIGHT
	'\u2534'    #  0xB1 -> BOX DRAWINGS LIGHT UP AND HORIZONTAL
	'\u252c'    #  0xB2 -> BOX DRAWINGS LIGHT DOWN AND HORIZONTAL
	'\u2524'    #  0xB3 -> BOX DRAWINGS LIGHT VERTICAL AND LEFT
	'\u258e'    #  0xB4 -> LEFT ONE QUARTER BLOCK
	'\u258d'    #  0xB5 -> LEFT THREE EIGTHS BLOCK
	'\uf131'    #  0xB6 -> RIGHT THREE EIGHTHS BLOCK (CUS)
	'\uf132'    #  0xB7 -> UPPER ONE QUARTER BLOCK (CUS)
	'\uf133'    #  0xB8 -> UPPER THREE EIGHTS BLOCK (CUS)
	'\u2583'    #  0xB9 -> LOWER THREE EIGHTHS BLOCK
	'\uf12d'    #  0xBA -> ONE EIGHTH BLOCK UP AND LEFT (CUS)
	'\u2596'    #  0xBB -> QUADRANT LOWER LEFT
	'\u259d'    #  0xBC -> QUADRANT UPPER RIGHT
	'\u2518'    #  0xBD -> BOX DRAWINGS LIGHT UP AND LEFT
	'\u2598'    #  0xBE -> QUADRANT UPPER LEFT
	'\u259a'    #  0xBF -> QUADRANT UPPER LEFT AND LOWER RIGHT
	'\u2500'    #  0xC0 -> BOX DRAWINGS LIGHT HORIZONTAL
	'\u2660'    #  0xC1 -> BLACK SPADE SUIT
	'\u2502'    #  0xC2 -> BOX DRAWINGS LIGHT VERTICAL
	'\u2500'    #  0xC3 -> BOX DRAWINGS LIGHT HORIZONTAL
	'\uf122'    #  0xC4 -> BOX DRAWINGS LIGHT HORIZONTAL ONE QUARTER UP (CUS)
	'\uf123'    #  0xC5 -> BOX DRAWINGS LIGHT HORIZONTAL TWO QUARTERS UP (CUS)
	'\uf124'    #  0xC6 -> BOX DRAWINGS LIGHT HORIZONTAL ONE QUARTER DOWN (CUS)
	'\uf126'    #  0xC7 -> BOX DRAWINGS LIGHT VERTICAL ONE QUARTER LEFT (CUS)
	'\uf128'    #  0xC8 -> BOX DRAWINGS LIGHT VERTICAL ONE QUARTER RIGHT (CUS)
	'\u256e'    #  0xC9 -> BOX DRAWINGS LIGHT ARC DOWN AND LEFT
	'\u2570'    #  0xCA -> BOX DRAWINGS LIGHT ARC UP AND RIGHT
	'\u256f'    #  0xCB -> BOX DRAWINGS LIGHT ARC UP AND LEFT
	'\uf12a'    #  0xCC -> ONE EIGHTH BLOCK UP AND RIGHT (CUS)
	'\u2572'    #  0xCD -> BOX DRAWINGS LIGHT DIAGONAL UPPER LEFT TO LOWER RIGHT
	'\u2571'    #  0xCE -> BOX DRAWINGS LIGHT DIAGONAL UPPER RIGHT TO LOWER LEFT
	'\uf12b'    #  0xCF -> ONE EIGHTH BLOCK DOWN AND RIGHT (CUS)
	'\uf12c'    #  0xD0 -> ONE EIGHTH BLOCK DOWN AND LEFT (CUS)
	'\u25cf'    #  0xD1 -> BLACK CIRCLE
	'\uf125'    #  0xD2 -> BOX DRAWINGS LIGHT HORIZONTAL TWO QUARTERS DOWN (CUS)
	'\u2665'    #  0xD3 -> BLACK HEART SUIT
	'\uf127'    #  0xD4 -> BOX DRAWINGS LIGHT VERTICAL TWO QUARTERS LEFT (CUS)
	'\u256d'    #  0xD5 -> BOX DRAWINGS LIGHT ARC DOWN AND LEFT
	'\u2573'    #  0xD6 -> BOX DRAWINGS LIGHT DIAGONAL CROSS
	'\u25cb'    #  0xD7 -> WHITE CIRCLE
	'\u2663'    #  0xD8 -> BLACK CLUB SUIT
	'\uf129'    #  0xD9 -> BOX DRAWINGS LIGHT VERTICAL TWO QUARTERS RIGHT (CUS)
	'\u2666'    #  0xDA -> BLACK DIAMOND SUIT
	'\u253c'    #  0xDB -> BOX DRAWINGS LIGHT VERTICAL AND HORIZONTAL
	'\uf12e'    #  0xDC -> LEFT HALF BLOCK MEDIUM SHADE (CUS)
	'\u2502'    #  0xDD -> BOX DRAWINGS LIGHT VERTICAL
	'\u03c0'    #  0xDE -> GREEK SMALL LETTER PI
	'\u25e5'    #  0xDF -> BLACK UPPER RIGHT TRIANGLE
	'\xa0'      #  0xE0 -> NO-BREAK SPACE
	'\u258c'    #  0xE1 -> LEFT HALF BLOCK
	'\u2584'    #  0xE2 -> LOWER HALF BLOCK
	'\u2594'    #  0xE3 -> UPPER ONE EIGHTH BLOCK
	'\u2581'    #  0xE4 -> LOWER ONE EIGHTH BLOCK
	'\u258f'    #  0xE5 -> LEFT ONE EIGHTH BLOCK
	'\u2592'    #  0xE6 -> MEDIUM SHADE
	'\u2595'    #  0xE7 -> RIGHT ONE EIGHTH BLOCK
	'\uf12f'    #  0xE8 -> LOWER HALF BLOCK MEDIUM SHADE (CUS)
	'\u25e4'    #  0xE9 -> BLACK UPPER LEFT TRIANGLE
	'\uf130'    #  0xEA -> RIGHT ONE QUARTER BLOCK (CUS)
	'\u251c'    #  0xEB -> BOX DRAWINGS LIGHT VERTICAL AND RIGHT
	'\u2597'    #  0xEC -> QUADRANT LOWER RIGHT
	'\u2514'    #  0xED -> BOX DRAWINGS LIGHT UP AND RIGHT
	'\u2510'    #  0xEE -> BOX DRAWINGS LIGHT DOWN AND LEFT
	'\u2582'    #  0xEF -> LOWER ONE QUARTER BLOCK
	'\u250c'    #  0xF0 -> BOX DRAWINGS LIGHT DOWN AND RIGHT
	'\u2534'    #  0xF1 -> BOX DRAWINGS LIGHT UP AND HORIZONTAL
	'\u252c'    #  0xF2 -> BOX DRAWINGS LIGHT DOWN AND HORIZONTAL
	'\u2524'    #  0xF3 -> BOX DRAWINGS LIGHT VERTICAL AND LEFT
	'\u258e'    #  0xF4 -> LEFT ONE QUARTER BLOCK
	'\u258d'    #  0xF5 -> LEFT THREE EIGTHS BLOCK
	'\uf131'    #  0xF6 -> RIGHT THREE EIGHTHS BLOCK (CUS)
	'\uf132'    #  0xF7 -> UPPER ONE QUARTER BLOCK (CUS)
	'\uf133'    #  0xF8 -> UPPER THREE EIGHTS BLOCK (CUS)
	'\u2583'    #  0xF9 -> LOWER THREE EIGHTHS BLOCK
	'\uf12d'    #  0xFA -> ONE EIGHTH BLOCK UP AND LEFT (CUS)
	'\u2596'    #  0xFB -> QUADRANT LOWER LEFT
	'\u259d'    #  0xFC -> QUADRANT UPPER RIGHT
	'\u2518'    #  0xFD -> BOX DRAWINGS LIGHT UP AND LEFT
	'\u2598'    #  0xFE -> QUADRANT UPPER LEFT
	'\u03c0'    #  0xFF -> GREEK SMALL LETTER PI
)

_p2sadjust = [0x80, 0x00, -0X40, 0X40, 0X40, -0X40, -0X80, 0X00]

_control_char_names = {
	0x03:	"{run/stop}",
	0x05:	"{white}",
	0X08:	"{ctrl+h}",
	0X09:	"{ctrl+i}",
	0X0E:	"{ctrl+n}",
	0X11:	"{crsr down}",
	0x12:	"{rvs on}",
	0x13:	"{home}",
	0x14:	"{del}",
	0x1c:	"{red}",
	0x1d:	"{crsr right}",
	0x1e:	"{green}",
	0x1f:	"{blue}",
	0x81:	"{orange}",
	0x85:	"{f1}",
	0X86:	"{f3}",
	0x87:	"{f5}",
	0x88:	"{f7}",
	0x89:	"{f2}",
	0x8a:	"{f4}",
	0X8b:	"{f6}",
	0x8c:	"{f8}",
	0x8d:	"{shift return}",
	0x8e:	"{ctrl+/}",
	0x90:	"{black}",
	0x91:	"{crsr up}",
	0x92:	"{rvs off}",
	0x93:	"{clear}",
	0x94:	"{inst}",
	0x95:	"{brown}",
	0x96:	"{light-red}",
	0x97:	"{darkgrey}",
	0X98:	"{grey}",
	0X99:	"{lightgreen}",
	0X9a:	"{lightblue}",
	0x9b:	"{lightgrey}",
	0x9c:	"{purple}",
	0x9d:	"{crsr left}",
	0x9e:	"{yellow}",
	0x9f:	"{cyan}"
}

def pettoscreen(c):
	return c+_p2sadjust[c>>5]

def pettoascii(c):
	return _control_char_names.get(c, _decoding_table[c])

def c64fontmapper(c):
	if c>=0x01 and c<=0x1f:
		c += 0x80
	elif c>=0x80 and c<=0x9f:
		c += 0x40
	else:
		c = pettoscreen(c)

	return chr(0xee00+c)

def line_iterator(mem, ivl):
	mem = mem.view(ivl)

	addr = ivl.first
	while addr<=ivl.last:
		link = mem.r16(addr)
		if (link&0xff00)==0:
			# Code from LIST command:
			# .,A6CD B1 5F    LDA ($5F),Y     HIGH BYTE OF LINK
			# .,A6CF F0 43    BEQ $A714       END OF PROGRAM
			break # end of the program
		yield Interval(addr, link-1)
		addr = link

@unique
class TokenType(Enum):
	LineLink = auto()
	LineNumber = auto()
	Command = auto()
	Quoted = auto()
	Colon = auto()
	Semicolon = auto()
	Comma = auto()
	OpenBracket = auto()
	CloseBracket = auto()
	Spaces = auto()
	Number = auto()
	Text = auto()
	LineNumberReference = auto()
	LineEnd = auto()


class Token(object):
	def __init__(self, type, ivl):
		self.type = type
		self.ivl = ivl

	def value(self):
		return None

	def __str__(self):
		return "{}: {}".format(self.type, self.ivl)

class U16Token(Token):
	def __init__(self, type, ivl, val):
		super().__init__(type, ivl)
		self.value = val

	def value(self):
		return self.value

	def hexstr(self):
		return "${:04x}".format(self.value)

	def __str__(self):
		return str(self.value)

class NumberToken(Token):
	def __init__(self, type, ivl):
		super().__init__(type, ivl)

	def value(self, mem):
		n = 0
		for a in self.ivl:
			n = n*10+(mem.r8(a)-0x30)
		return n

class CommandToken(Token):
	def __init__(self, ivl, val):
		super().__init__(TokenType.Command, ivl)
		self.value = val

	def value(self):
		return self.value

	def __str__(self):
		return command(self.value).name

class CharToken(Token):
	def __init__(self, type, ivl, val):
		super().__init__(type, ivl)
		self.value = val

	def value(self):
		return self.value

	def __str__(self):
		return chr(self.value)

class Lexer(object):
	def __init__(self, mem, ivl):
		self.mem = mem
		self.ivl = ivl
		self.remark = False

	def _spaces(self, addr):
		if addr>=self.ivl.last:
			return (Interval(addr, addr), addr+1)
		for a in range(addr+1, self.ivl.last+1):
			v = self.mem.r8(a)
			if v!=ord(' '):
				return (Interval(addr, a-1), a)
		return (Interval(addr, self.ivl.last), self.ivl.last+1)

	# IMPORTANT: numbers should not stop a text run or variables such
	#            as 'X2$' will be spit.
	_endstext = {ord(' '), ord('"'), ord(':'), ord(';'), ord(','), ord('('), ord(')'), 0}
	_endtextremark = {ord('"'), 0}

	def _textshouldend(self, ch):
		if self.remark:
			return ch in self._endtextremark
		else:
			return ch in self._endstext

	def _text(self, addr):
		if addr>=self.ivl.last:
			return (Interval(addr, addr), addr+1)
		for a in range(addr+1, self.ivl.last+1):
			v = self.mem.r8(a)
			if v&0x80 or self._textshouldend(v):
				return (Interval(addr, a-1), a)
		return (Interval(addr, self.ivl.last), self.ivl.last+1)

	def _quoted(self, addr):
		if addr>=self.ivl.last:
			return (Interval(addr, addr), addr+1)
		for a in range(addr+1, self.ivl.last+1):
			v = self.mem.r8(a)
			if v==ord('"'):
				return (Interval(addr, a), a+1)
			elif v==0:
				return (Interval(addr, a-1), a)
		return (Interval(addr, self.ivl.last), self.ivl.last+1)

	def _number(self, addr):
		if addr>=self.ivl.last:
			return (Interval(addr, addr), addr+1)
		for a in range(addr+1, self.ivl.last+1):
			v = self.mem.r8(a)
			if v<ord('0') or v>ord('9'):
				return (Interval(addr, a-1), a)
		return (Interval(addr, self.ivl.last), self.ivl.last+1)

	def tokens(self):
		addr = self.ivl.first

		while addr<=self.ivl.last:
			# the line link
			link = self.mem.r16(addr)
			yield U16Token(TokenType.LineLink, Interval(addr, addr+1), link)
			if link&0xff00 == 0:
				break
			addr += 2

			# the line number
			yield U16Token(TokenType.LineNumber, Interval(addr, addr+1), self.mem.r16(addr))
			addr += 2

			while addr<=self.ivl.last:
				v = self.mem.r8(addr)
				if v==0:
					yield Token(TokenType.LineEnd, Interval(addr))
					addr += 1
					self.remark = False
					break
				elif v&0x80: # command
					addr += 1
					yield CommandToken(Interval(addr), v)
					if v==0x8f: # REM
						self.remark = True
				elif v==ord('"'):
					ivl, addr = self._quoted(addr)
					yield Token(TokenType.Quoted, ivl)
				elif not self.remark and v==ord(':'):
					yield CharToken(TokenType.Colon, Interval(addr), v)
					addr += 1
				elif not self.remark and v==ord(';'):
					yield CharToken(TokenType.Semicolon, Interval(addr), v)
					addr += 1
				elif not self.remark and v==ord(','):
					yield CharToken(TokenType.Comma, Interval(addr), v)
					addr += 1
				elif not self.remark and v==ord('('):
					yield CharToken(TokenType.OpenBracket, Interval(addr), v)
					addr += 1
				elif not self.remark and v==ord(')'):
					yield CharToken(TokenType.CloseBracket, Interval(addr), v)
					addr += 1
				elif not self.remark and v==ord(' '):
					ivl, addr = self._spaces(addr)
					yield Token(TokenType.Spaces, ivl)
				elif not self.remark and v>=ord('0') and v<=ord('9'):
					ivl, addr = self._number(addr)
					yield NumberToken(TokenType.Number, ivl)
				else:
					ivl, addr = self._text(addr)
					yield Token(TokenType.Text, ivl)

class Parser(object):
	def __init__(self, mem, ivl):
		self.lexer = Lexer(mem, ivl)
		self.gen = self.lexer.tokens()

	def _goto_or_gosub(self):
		try:
			tok = next(self.gen)
			if tok.type==TokenType.LineEnd:
				yield tok
				return
			# pass on spaces before the first line number
			if tok.type==TokenType.Spaces:
				yield tok
				tok = next(self.gen)
				if tok.type==TokenType.LineEnd:
					yield tok
					return

			if tok.type!=TokenType.Number:
				# we we're expecting a line number. Pass it on and bail.
				yield tok
			else:
				# rewrite the type, it's a line number reference.
				tok.type = TokenType.LineNumberReference
				yield tok

				# additional line numbers are separated by commas. There may
				# also be whitespace on either side of the comma.
				while True:
					# space before the comma
					tok = next(self.gen)
					if tok.type==TokenType.LineEnd:
						yield tok
						return
					if tok.type==TokenType.Spaces:
						yield tok
						tok = next(self.gen)
						if tok.type==TokenType.LineEnd:
							yield tok
							return

					# a comma
					if tok.type!=TokenType.Comma:
						# if more line numbers were coming this should have been a comma
						# so pass it on and bail.
						yield tok
						return
					yield tok
					tok = next(self.gen)
					if tok.type==TokenType.LineEnd:
						yield tok
						return

					# there could be more space after the comma
					if tok.type==TokenType.Spaces:
						yield tok
						tok = next(self.gen)
						if tok.type==TokenType.LineEnd:
							yield tok
							return

					# the line number
					if tok.type!=TokenType.Number:
						yield tok
						return

					# rewrite the type, it's a line number reference.
					tok.type = TokenType.LineNumberReference
					yield tok
		except StopIteration:
			pass

	def _then(self):
		try:
			tok = next(self.gen)
			if tok.type==TokenType.LineEnd:
				yield tok
				return
			# pass on spaces before the line number
			if tok.type==TokenType.Spaces:
				yield tok
				tok = next(self.gen)
				if tok.type==TokenType.LineEnd:
					yield tok
					return

			if tok.type!=TokenType.Number:
				# we we're expecting a line number. Pass it on and bail.
				yield tok
			else:
				# rewrite the type, it's a line number reference.
				tok.type = TokenType.LineNumberReference
				yield tok
		except StopIteration:
			pass

	def _list(self):
		try:
			tok = next(self.gen)
			if tok.type==TokenType.LineEnd:
				yield tok
				return
			# pass on spaces before the line numbers
			if tok.type==TokenType.Spaces:
				yield tok
				tok = next(self.gen)
				if tok.type==TokenType.LineEnd:
					yield tok
					return

			if tok.type==TokenType.Number:
				# rewrite the type, it's a line number reference.
				tok.type = TokenType.LineNumberReference
				yield tok

				tok = next(self.gen)
				if tok.type==TokenType.LineEnd:
					yield tok
					return
				# pass on spaces after the number
				if tok.type==TokenType.Spaces:
					yield tok
					tok = next(self.gen)
					if tok.type==TokenType.LineEnd:
						yield tok
						return

				if tok.type!=TokenType.Command or tok.value!=0xab: # $ab is MINUS
					# we didn't get a minus sign here so we're done
					yield tok
					return
				yield tok # pass on the MINUS sign
			elif tok.type==TokenType.Command and tok.value==0xab: # $ab is MINUS
				# it's a minus sign
				yield tok
			else:
				# we were expecting a number or a minus sign. Pass token
				# on and bail.
				yield tok
				return

			# spaces after the minus sign
			tok = next(self.gen)
			if tok.type==TokenType.LineEnd:
				yield tok
				return
			if tok.type==TokenType.Spaces:
				yield tok
				tok = next(self.gen)
				if tok.type==TokenType.LineEnd:
					yield tok
					return

			if tok.type==TokenType.Number:
				# rewrite the type, it's a line number reference.
				tok.type = TokenType.LineNumberReference

			yield tok # pass it on if it's a number or not
		except StopIteration:
			pass

	def tokens(self):
		for tok in self.gen:
			if tok.type==TokenType.Command:
				c = tok.value
				if c==0x89 or c==0x8d: # GOTO or GOSUB
					yield from self._goto_or_gosub()
				elif c==0xa7: # THEN
					yield from self._then()
				elif c==0x9b: # LIST
					yield from self._list()
				else:
					yield tok
			else:
				yield tok

def line_tokens(mem, ivl, c64font=False):
	mem = mem.view(ivl)
	mapper = c64fontmapper if c64font else pettoascii

	yield {
		'type': 'line_num',
		'ivl': Interval(ivl.first+2, ivl.first+3),
		'val': mem.r16(ivl.first+2)}

	# parsing state
	@unique
	class PS(Enum):
		ExpectingAnything = auto()
		ProcessCommand = auto()
		ProcessColon = auto()
		GetLineNumber = auto()
		GetRestOfLineNumber = auto()
		OpenQuote = auto()
		ProcessQuote = auto()
		GetText = auto()
		GetRestOfText = auto()
		GetAddress = auto()
		GetRestOfAddress = auto()
		ProcessComma = auto()
		Done = auto()
	ps = PS.ExpectingAnything

	line_num_quota = 0
	
	for addr in range(ivl.first+4, ivl.last+1): # +4 skips line link and number
		token = mem.r8(addr)

		recycle_token = True
		while recycle_token:
			recycle_token = False
			# *************************************************************#
			if ps==PS.ExpectingAnything:
				# command
				if token&0x80:
					recycle_token = True
					ps = PS.ProcessCommand
				# colon
				elif token==0x3a:
					recycle_token = True
					ps = PS.ProcessColon
				# quotes
				elif token==0x22:
					recycle_token = True
					ps = PS.OpenQuote
				elif token==0:
					ps = PS.Done
				# text
				else:
					if line_num_quota and (token>=ord('0') and token<=ord('9')):
						recycle_token = True
						ps = PS.GetLineNumber
					else:
						recycle_token = True
						ps = PS.GetText
			# *************************************************************#
			elif ps==PS.ProcessCommand:
				cmd = command(token)
				yield {
					'type': 'command',
					'ivl': Interval(addr, addr),
					'val': cmd.name}

				if cmd.syscall:
					ps = PS.GetAddress
				else:
					line_num_quota = cmd.num_lines
					if line_num_quota:
						numval = 0
					ps = PS.ExpectingAnything
			# *************************************************************#
			elif ps==PS.GetText:
					token_start = addr
					strval = mapper(token)
					ps = PS.GetRestOfText
			# *************************************************************#
			elif ps==PS.GetRestOfText:
				# command
				if token&0x80:
					recycle_token = True
					ps = PS.ProcessCommand
				# colon
				elif token==0x3a:
					recycle_token = True
					ps = PS.ProcessColon
				# quotes
				elif token==0x22:
					recycle_token = True
					ps = PS.OpenQuote
				# comma
				elif token==ord(','):
					recycle_token = True
					ps = PS.ProcessComma
				elif line_num_quota and (token>=ord('0') and token<=ord('9')):
					recycle_token = True
					ps = PS.GetLineNumber
				elif token==0:
					ps = PS.Done
				else:
					strval += mapper(token)

				# we generate an output token when we leave this state
				if ps!=PS.GetRestOfText:
					yield {
						'type': 'text',
						'ivl': Interval(token_start, addr-1),
						'val': strval}
			# *************************************************************#
			elif ps==PS.ProcessComma:
				yield {
						'type': 'text',
						'ivl': Interval(addr, addr),
						'val': chr(token)}
				ps = PS.ExpectingAnything
			# *************************************************************#
			elif ps==PS.ProcessColon:
				line_num_quota = 0
				# in this context a colon is a statement separator so we
				# return it in its own text token
				yield {
					'type': 'text',
					'ivl': Interval(addr, addr),
					'val': ':'}
				ps = PS.ExpectingAnything
			# *************************************************************#
			elif ps==PS.OpenQuote:
				token_start = addr
				strval = '"'
				ps = PS.ProcessQuote
			# *************************************************************#
			elif ps==PS.ProcessQuote:
				if token==0x22: # quote
					yield {
						'type': 'quoted',
						'ivl': Interval(token_start, addr),
						'val': strval+'"'}
					ps = PS.ExpectingAnything
				elif token==0:
					yield {
						'type': 'quoted',
						'ivl': Interval(token_start, addr-1),
						'val': strval}
					ps = PS.Done
				else:
					strval += mapper(token)
			# *************************************************************#
			elif ps==PS.GetLineNumber:
					token_start = addr
					numval = token-ord('0')
					ps = PS.GetRestOfLineNumber
			# *************************************************************#
			elif ps==PS.GetRestOfLineNumber:
				if token>=ord('0') and token<=ord('9'):
					numval = numval*10 + int(token-ord('0'))
				else:
					yield {
						'type': 'line_ref',
						'ivl': Interval(token_start, addr-1),
						'val':	numval
					}
					if line_num_quota>0:
						line_num_quota -= 1
					recycle_token = True
					ps = PS.ExpectingAnything
			# *************************************************************#
			elif ps==PS.GetAddress:
				if token>=ord('0') and token<=ord('9'):
					token_start = addr
					numval = token-ord('0')
					ps = PS.GetRestOfAddress
				else:
					recycle_token = True
					ps = PS.ExpectingAnything
			# *************************************************************#
			elif ps==PS.GetRestOfAddress:
				if token>=ord('0') and token<=ord('9'):
					numval = numval*10 + int(token-ord('0'))
				else:
					yield {
						'type': 'address',
						'ivl': Interval(token_start, addr-1),
						'val':	numval
					}
					recycle_token = True
					ps = PS.ExpectingAnything
			# *************************************************************#
			else:
				assert False, "Unexpected state!"

def line_to_address(mem, ivl, line):
	mem = mem.view(ivl)
	for livl in line_iterator(mem, ivl):
		num = mem.r16(livl.first+2)
		if num==line:
			return livl.first
		if num>line: # no point looking any further
			break
	return None
 
if __name__=='__main__':
	from memory import *

	with open("list.prg", "rb") as f:
		contents = f.read()
		mem = Memory(contents)

	p = Parser(mem, mem.range())
	for token in p.tokens():
		if token.type == TokenType.LineNumber:
			print(token.type," ", token)
		if token.type == TokenType.Command:
			print(token)
		elif token.type == TokenType.LineNumberReference:
			print(" : ", token)
	print()
