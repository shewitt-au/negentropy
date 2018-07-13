from lark import Lark, Transformer
from lark.exceptions import LarkError
from interval import Interval
import errors
from inspect import cleandoc
from textwrap import indent

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
		self.ctx.parse_datasource(t[0])

	def memmap(self, t):
		data = None
		for e in t[0]:
			if e[3] is not None:
				data = e[3] if e[3]>=0 else None
			self.ctx.memtype.parse_add(e[0], self.ctx.decoders[e[1]], e[2], data)

	# mmentry: range NAME ["<" mmdataaddr] properties?
	def mmentry(self, t):
		length = len(t)
		data = None
		props = {}
		if length==2:
			ivl, dname = t
		elif length==3:
			ivl = t[0]
			dname = t[1]
			if isinstance(t[2], dict):
				props = t[2]
			else:
				data = t[2]
		else: #length==4
			ivl, dname, data, props = t

		# reset data address
		if data is not None and not isinstance(data, int):
			data = -1

		return (ivl, dname, props, data)

	def mmbody(self, t):
		return t

	def label(self, t):
		l = len(t)
		if l==2:
			flags = ""
			pos = 'v'
			ivl, name = t
		else: # i==3
			ivl, flags, name = t
		self.ctx.syms.parse_add(self.ctx, ivl, name, 'i' in flags)

	def lflags(self, t):
		return str(t[0])

	def comment(self, t):
		l = len(t)
		if l==2:
			pos = 'v'
			addr, txt = t
		else: # i==3
			addr, pos, txt = t
		
		cmt = self.ctx.cmts[0].by_address.get(addr, ("", "", ""))
		if pos=='v':
			self.ctx.cmts[0].add((addr, cmt[1], txt))
		elif pos=='^':
			self.ctx.cmts[0].add((addr, txt, cmt[2]))
		elif pos=='>':
			self.ctx.cmts[1].add((addr, txt))
		
	def cpos(self, t):
		return str(t[0])

	def properties(self, t):
		return {str(i[0]) : i[1] for i in t}
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
		return Interval(int(t[0]), int(t[1])) if len(t)==2 else Interval(int(t[0]))
