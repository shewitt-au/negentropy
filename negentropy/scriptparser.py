from inspect import cleandoc
from textwrap import indent

from lark import Lark, Transformer
from lark.exceptions import LarkError

from .interval import Interval
from . import errors

def parse(ctx, fname):
	with open(fname, "r") as f:
		t = f.read()
	try:
		l = Lark(open(ctx.implfile("script.lark")).read(), parser='lalr', debug=True)
		t = l.parse(t)
		ScriptTransformer(ctx).transform(t)
	except LarkError as e:
		etext = indent(str(e), "   ")
		raise errors.ParserException("Error parsing '{}:\n{}'".format(fname, etext))

class ScriptTransformer(Transformer):
	def __init__(self, ctx):
		self.ctx = ctx

	def datasource(self, t):
		self.ctx.parse_datasource(t[0][1])

	def memmap(self, t):
		def handle(self, range, mmdecoder, properties={}, mmdataaddr=None):
			self.ctx.memtype.parse_add(range, self.ctx.decoders[mmdecoder], properties, mmdataaddr)
		for e in t[0]:
			handle(self, **dict(e))
	def mmbody(self, t):
		return t
	def mmentry(self, t):
		return t
	def mmdecoder(self, t):
		return ("mmdecoder", str(t[0]))
	def mmdataaddr(self, t):
		return ("mmdataaddr", t[0])
	def mmfromreset(selt, t):
		return -1

	def label(self, t):
		def handle(self, range, lname, lflags=""):
			self.ctx.syms.parse_add(self.ctx, range, lname, 'i' in lflags)
		handle(self, **dict(t))
	def lflags(self, t):
		return ("lflags", str(t[0]))
	def lname(self, t):
		return ("lname", str(t[0]))

	def directive(self, t):
		def handle(daddress, dcommand, doaddress=None, dosymbol=None):
			self.ctx.directives.parse_add(daddress, dcommand, doaddress, dosymbol)
		handle(**dict(t))
	def daddress(self, t):
		return ("daddress", t[0])
	def dcommand(self, t):
		return ("dcommand", str(t[0]))
	def doaddress(self, t):
		return ("doaddress", t[0])
	def dosymbol(self, t):
		return ('dosymbol', str(t[0]))

	def comment(self, t):
		def handle(self, caddress, ctext, cpos="^"):
			if not ctext:
				ctext = "\n"
			if cpos=='^':
				self.ctx.cmts.add_before(caddress, ctext)
			elif cpos=='v':
				self.ctx.cmts.add_after(caddress, ctext)
			elif cpos=='>':
				self.ctx.cmts.add_inline(caddress, ctext)
		handle(self, **dict(t))
	def caddress(self, t):
		return ("caddress", t[0])
	def cpos(self, t):
		return ("cpos", str(t[0]))
	def ctext(self, t):
		return ('ctext', str(t[0]))

	def properties(self, t):
		return ("properties", {str(i[0]) : i[1] for i in t})
	def propentry(self, t):
		return t

	def hexnum(self, t):
		return int(t[0][1:], 16)
	def decimal(self, t):
		return int(t[0])
	def boolean(self, t):
		return bool(t[0])
	def list(self, t):
		return list(t)
	def name(self, t):
		return str(t[0])
	def quoted(self, t):
		return t[0][1:-1]
	def tquoted(self, t):
		return cleandoc(t[0][3:-3])

	def range(self, t):
		ivl = Interval(int(t[0]), int(t[1])) if len(t)==2 else Interval(int(t[0]))
		return ("range", ivl)
