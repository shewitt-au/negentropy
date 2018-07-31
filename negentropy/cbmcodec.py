import codecs

# Codec example here: https://github.com/dj51d/cbmcodecs/blob/develop/cbmcodecs/petscii_c64en_uc.py
# More stuff here: https://pymotw.com/3/codecs/

_petscii_decoding_table = (
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

# 'charmap_build' is undocumented and somewhat contentious.
# TODO: PERHAPS WE SHOULD NOT BE USING THIS?!?!
_petscii_encoding_table = codecs.charmap_build(_petscii_decoding_table)

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

def pettoascii(c):
	return _control_char_names.get(c, _petscii_decoding_table[c])

_c64promonostyle_decoding_table = (
	'\uee80'
	'\uee81'
	'\uee82'
	'\uee83'
	'\uee84'
	'\uee85'
	'\uee86'
	'\uee87'
	'\uee88'
	'\uee89'
	'\uee8a'
	'\uee8b'
	'\uee8c'
	'\uee8d'
	'\uee8e'
	'\uee8f'
	'\uee90'
	'\uee91'
	'\uee92'
	'\uee93'
	'\uee94'
	'\uee95'
	'\uee96'
	'\uee97'
	'\uee98'
	'\uee99'
	'\uee9a'
	'\uee9b'
	'\uee9c'
	'\uee9d'
	'\uee9e'
	'\uee9f'
	'\uee20'
	'\uee21'
	'\uee22'
	'\uee23'
	'\uee24'
	'\uee25'
	'\uee26'
	'\uee27'
	'\uee28'
	'\uee29'
	'\uee2a'
	'\uee2b'
	'\uee2c'
	'\uee2d'
	'\uee2e'
	'\uee2f'
	'\uee30'
	'\uee31'
	'\uee32'
	'\uee33'
	'\uee34'
	'\uee35'
	'\uee36'
	'\uee37'
	'\uee38'
	'\uee39'
	'\uee3a'
	'\uee3b'
	'\uee3c'
	'\uee3d'
	'\uee3e'
	'\uee3f'
	'\uee00'
	'\uee01'
	'\uee02'
	'\uee03'
	'\uee04'
	'\uee05'
	'\uee06'
	'\uee07'
	'\uee08'
	'\uee09'
	'\uee0a'
	'\uee0b'
	'\uee0c'
	'\uee0d'
	'\uee0e'
	'\uee0f'
	'\uee10'
	'\uee11'
	'\uee12'
	'\uee13'
	'\uee14'
	'\uee15'
	'\uee16'
	'\uee17'
	'\uee18'
	'\uee19'
	'\uee1a'
	'\uee1b'
	'\uee1c'
	'\uee1d'
	'\uee1e'
	'\uee1f'
	'\ueea0'
	'\ueea1'
	'\ueea2'
	'\ueea3'
	'\ueea4'
	'\ueea5'
	'\ueea6'
	'\ueea7'
	'\ueea8'
	'\ueea9'
	'\ueeaa'
	'\ueeab'
	'\ueeac'
	'\ueead'
	'\ueeae'
	'\ueeaf'
	'\ueeb0'
	'\ueeb1'
	'\ueeb2'
	'\ueeb3'
	'\ueeb4'
	'\ueeb5'
	'\ueeb6'
	'\ueeb7'
	'\ueeb8'
	'\ueeb9'
	'\ueeba'
	'\ueebb'
	'\ueebc'
	'\ueebd'
	'\ueebe'
	'\ueebf'
	'\ueec0'
	'\ueec1'
	'\ueec2'
	'\ueec3'
	'\ueec4'
	'\ueec5'
	'\ueec6'
	'\ueec7'
	'\ueec8'
	'\ueec9'
	'\ueeca'
	'\ueecb'
	'\ueecc'
	'\ueecd'
	'\ueece'
	'\ueecf'
	'\ueed0'
	'\ueed1'
	'\ueed2'
	'\ueed3'
	'\ueed4'
	'\ueed5'
	'\ueed6'
	'\ueed7'
	'\ueed8'
	'\ueed9'
	'\ueeda'
	'\ueedb'
	'\ueedc'
	'\ueedd'
	'\ueede'
	'\ueedf'
	'\uee60'
	'\uee61'
	'\uee62'
	'\uee63'
	'\uee64'
	'\uee65'
	'\uee66'
	'\uee67'
	'\uee68'
	'\uee69'
	'\uee6a'
	'\uee6b'
	'\uee6c'
	'\uee6d'
	'\uee6e'
	'\uee6f'
	'\uee70'
	'\uee71'
	'\uee72'
	'\uee73'
	'\uee74'
	'\uee75'
	'\uee76'
	'\uee77'
	'\uee78'
	'\uee79'
	'\uee7a'
	'\uee7b'
	'\uee7c'
	'\uee7d'
	'\uee7e'
	'\uee7f'
	'\uee40'
	'\uee41'
	'\uee42'
	'\uee43'
	'\uee44'
	'\uee45'
	'\uee46'
	'\uee47'
	'\uee48'
	'\uee49'
	'\uee4a'
	'\uee4b'
	'\uee4c'
	'\uee4d'
	'\uee4e'
	'\uee4f'
	'\uee50'
	'\uee51'
	'\uee52'
	'\uee53'
	'\uee54'
	'\uee55'
	'\uee56'
	'\uee57'
	'\uee58'
	'\uee59'
	'\uee5a'
	'\uee5b'
	'\uee5c'
	'\uee5d'
	'\uee5e'
	'\uee5f'
	'\ueee0'
	'\ueee1'
	'\ueee2'
	'\ueee3'
	'\ueee4'
	'\ueee5'
	'\ueee6'
	'\ueee7'
	'\ueee8'
	'\ueee9'
	'\ueeea'
	'\ueeeb'
	'\ueeec'
	'\ueeed'
	'\ueeee'
	'\ueeef'
	'\ueef0'
	'\ueef1'
	'\ueef2'
	'\ueef3'
	'\ueef4'
	'\ueef5'
	'\ueef6'
	'\ueef7'
	'\ueef8'
	'\ueef9'
	'\ueefa'
	'\ueefb'
	'\ueefc'
	'\ueefd'
	'\ueefe'
	'\ueeff'
	)

# 'charmap_build' is undocumented and somewhat contentious.
# TODO: PERHAPS WE SHOULD NOT BE USING THIS?!?!
_c64promonostyle_encoding_table = codecs.charmap_build(_c64promonostyle_decoding_table)

###############################################################################

class PetsciiCodec(codecs.Codec):
	def encode(self, input, errors='strict'):
		return codecs.charmap_encode(input, errors, _petscii_encoding_table)

	def decode(self, input, errors='strict'):
		return codecs.charmap_decode(input, errors, _petscii_decoding_table)

class PetsciiIncrementalEncoder(codecs.IncrementalEncoder):
	def encode(self, input, final=False):
		return codecs.charmap_encode(input, self.errors, _petscii_encoding_table)[0]

class PetsciiIncrementalDecoder(codecs.IncrementalDecoder):
	def decode(self, input, final=False):
		return codecs.charmap_decode(input, self.errors, _petscii_decoding_table)[0]

class PetsciiStreamWriter(PetsciiCodec, codecs.StreamWriter):
	pass

class PetsciiStreamReader(PetsciiCodec, codecs.StreamReader):
	pass

def petscii_getregentry():
	return codecs.CodecInfo(
		name='petscii',
		encode=PetsciiCodec().encode,
		decode=PetsciiCodec().decode,
		incrementalencoder=PetsciiIncrementalEncoder,
		incrementaldecoder=PetsciiIncrementalDecoder,
		streamreader=PetsciiStreamWriter,
		streamwriter=PetsciiStreamReader,
	)

###############################################################################

class PetsciiCtrlCodec(codecs.Codec):
	encode = None

	def decode(self, input, errors='strict'):
		return ("".join(map(pettoascii, input)), len(input))

class PetsciiCtrlIncrementalDecoder(codecs.IncrementalDecoder):
	def decode(self, input, final=False):
		return pettoascii(input)

class PetsciiCtrlStreamWriter(PetsciiCtrlCodec, codecs.StreamWriter):
	pass

class PetsciiCtrlStreamReader(PetsciiCtrlCodec, codecs.StreamReader):
	pass

def petsciisctrl_getregentry():
	return codecs.CodecInfo(
		name='petscii-ctrl',
		encode=PetsciiCtrlCodec().encode,
		decode=PetsciiCtrlCodec().decode,
		incrementalencoder=None,
		incrementaldecoder=PetsciiCtrlIncrementalDecoder,
		streamreader=PetsciiCtrlStreamWriter,
		streamwriter=PetsciiCtrlStreamReader,
	)

###############################################################################

class C64FontCodec(codecs.Codec):
	def encode(self, input, errors='strict'):
		return codecs.charmap_encode(input, errors, _c64promonostyle_encoding_table)

	def decode(self, input, errors='strict'):
		return codecs.charmap_decode(input, errors, _c64promonostyle_decoding_table)

class C64FontIncrementalEncoder(codecs.IncrementalEncoder):
	def encode(self, input, final=False):
		return codecs.charmap_encode(input, self.errors, _c64promonostyle_encoding_table)[0]

class C64FontIncrementalDecoder(codecs.IncrementalDecoder):
	def decode(self, input, final=False):
		return codecs.charmap_decode(input, self.errors, _c64promonostyle_decoding_table)[0]

class C64FontStreamWriter(C64FontCodec, codecs.StreamWriter):
	pass

class C64FontStreamReader(C64FontCodec, codecs.StreamReader):
	pass

def c64font_getregentry():
	return codecs.CodecInfo(
		name='c64font',
		encode=C64FontCodec().encode,
		decode=C64FontCodec().decode,
		incrementalencoder=C64FontIncrementalEncoder,
		incrementaldecoder=C64FontIncrementalDecoder,
		streamreader=C64FontStreamReader,
		streamwriter=C64FontStreamWriter,
	)

###############################################################################

_codecs = {
	'c64font': c64font_getregentry(),
	'petscii': petscii_getregentry(),
	'petscii-ctrl': petsciisctrl_getregentry()
	}

def _search_fn(encoding):
	return _codecs.get(encoding, None)

codecs.register(_search_fn)

###############################################################################

if __name__=='__main__':
	b = b'abc'
	print(b.decode('c64font'))

#	_p2sadjust = [0x80, 0x00, -0X40, 0X40, 0X40, -0X40, -0X80, 0X00]
#
#	def pettoscreen(c):
#		return c+_p2sadjust[c>>5]
#
#	def c64fontmapper(c):
#		if c>=0x01 and c<=0x1f:
#			c += 0x80
#		elif c>=0x80 and c<=0x9f:
#			c += 0x40
#		else:
#			c = pettoscreen(c)
#
#		return chr(0xee00+c)
#
#	print ("_c64promonostyle_decoding_table = (")
#	for c in range(0, 256):
#		print("\t'\\u{:04x}'".format(ord(c64fontmapper(c))))
#	print("\t)")
