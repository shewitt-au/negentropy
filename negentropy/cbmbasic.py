from enum import Enum, unique, auto
import functools

from .interval import Interval

# $80 - $ca
_commands = (
	"END",		# $80
	"FOR",		# $81
	"NEXT",		# $82
	"DATA",		# $83
	"INPUT#",	# $84
	"INPUT",	# $85
	"DIM",		# $86
	"READ",		# $87
	"LET",		# $88
	"GOTO",		# $89
	"RUN",		# $8a
	"IF",		# $8b
	"RESTORE",	# $8c
	"GOSUB",	# $8d
	"RETURN",	# $8e
	"REM",		# $8f
	"STOP",		# $90
	"ON",		# $91
	"WAIT",		# $92
	"LOAD",		# $93
	"SAVE",		# $94
	"VERIFY",	# $95
	"DEF",		# $96
	"POKE",		# $97
	"PRINT#",	# $98
	"PRINT",	# $99
	"CONT",		# $9a
	"LIST",		# $9b
	"CLR",		# $9c
	"CMD",		# $9d
	"SYS",		# $9e
	"OPEN",		# $9f
	"CLOSE",	# $a0
	"GET",		# $a1
	"NEW",		# $a2
	"TAB(",		# $a3
	"TO",		# $a4
	"FN",		# $a5
	"SPC(",		# $a6
	"THEN",		# $a7
	"NOT",		# $a8
	"STEP",		# $a9
	"+",		# $aa
	"-",		# $ab
	"*",		# $ac
	"/",		# $ad
	"↑",		# $ae
	"AND",		# $af
	"OR",		# $b0
	">",		# $b1
	"=",		# $b2
	"<",		# $b3
	"SGN",		# $b4
	"INT",		# $b5
	"ABS",		# $b6
	"USR",		# $b7
	"FRE",		# $b7
	"POS",		# $b9
	"SQR",		# $ba
	"RND",		# $bb
	"LOG",		# $bc
	"EXP",		# $bd
	"COS",		# $be
	"SIN",		# $bf
	"TAN",		# $c0
	"ATN",		# $c1
	"PEEK",		# $c2
	"LEN",		# $c3
	"STR$",		# $c4
	"VAL",		# $c5
	"ASC",		# $c6
	"CHR$",		# $c7
	"LEFT$",	# $c8
	"RIGHT$",	# $c9
	"MID$",		# $ca
	#
	#"\u03C0"   # $ff PI symmol
)

def command(token):
	if token>=0x80 and token<=0xca:
		return _commands[token-0x80]
	elif token==0xff:
		return "\u03C0"
	else:
		return "?"

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

@functools.lru_cache()
def line_to_address(mem, ivl, line):
	mem = mem.view(ivl)
	for livl in line_iterator(mem, ivl):
		num = mem.r16(livl.first+2)
		if num==line:
			return livl.first
		if num>line: # no point looking any further
			break
	return None

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
	Address = auto()
	LineEnd = auto()


class Token(object):
	def __init__(self, type, ivl):
		self.type = type
		self.ivl = ivl

	def value(self, **kwargs):
		return None

	def __str__(self):
		return "{}: {}".format(self.type, self.ivl)

class U16Token(Token):
	def __init__(self, type, ivl, val):
		super().__init__(type, ivl)
		self._value = val

	def value(self, **kwargs):
		return self._value

	def hexstr(self):
		return "${:04x}".format(self._value)

	def __str__(self):
		return str(self._value)

class NumberToken(Token):
	def __init__(self, type, ivl):
		super().__init__(type, ivl)

	def value(self, **kwargs):
		n = 0
		mem = kwargs['mem']
		for a in self.ivl:
			n = n*10+(mem.r8(a)-0x30)
		return n

class CommandToken(Token):
	def __init__(self, ivl, val):
		super().__init__(TokenType.Command, ivl)
		self._value = val

	def value(self, **kwargs):
		return command(self._value)

	def __str__(self):
		return command(self._value)

class CharToken(Token):
	def __init__(self, type, ivl, val):
		super().__init__(type, ivl)
		self._value = val

	def value(self, **kwargs):
		return chr(self._value)

	def __str__(self):
		return chr(self._value)

class TextToken(Token):
	def __init__(self, type, ivl):
		super().__init__(type, ivl)

	def value(self, **kwargs):
		return kwargs['mem'].string(self.ivl, kwargs['codec'])

	def __str__(self):
		return "{string: {}}", self.ivl

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
					yield TextToken(TokenType.Quoted, ivl)
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
					yield TextToken(TokenType.Spaces, ivl)
				elif not self.remark and v>=ord('0') and v<=ord('9'):
					ivl, addr = self._number(addr)
					yield NumberToken(TokenType.Number, ivl)
				else:
					ivl, addr = self._text(addr)
					yield TextToken(TokenType.Text, ivl)

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
				yield NumberToken(TokenType.LineNumberReference, tok.ivl)

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
					yield NumberToken(TokenType.LineNumberReference, tok.ivl)
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
				yield NumberToken(TokenType.LineNumberReference, tok.ivl)
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
				yield NumberToken(TokenType.LineNumberReference, tok.ivl)

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
				yield NumberToken(TokenType.LineNumberReference, tok.ivl)
			else:
				yield tok # pass it on if it's a number or not
		except StopIteration:
			pass

	def _sys(self):
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
				# rewrite the type, it's an address
				yield NumberToken(TokenType.Address, tok.ivl)
		except StopIteration:
			pass

	def tokens(self):
		for tok in self.gen:
			if tok.type==TokenType.Command:
				c = tok._value
				if c==0x89 or c==0x8d: # GOTO or GOSUB
					yield tok
					yield from self._goto_or_gosub()
				elif c==0xa7: # THEN
					yield tok
					yield from self._then()
				elif c==0x9b: # LIST
					yield tok
					yield from self._list()
				elif c==0x9e: # SYS
					yield tok
					yield from self._sys()
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

class Line(object):
	def __init__(self, gen):
		self.gen = gen

	def tokens(self):
		for token in self.gen:
			yield token
			if token.type==TokenType.LineEnd:
				break
