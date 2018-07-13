from lark import Lark, Transformer
from interval import Interval
from inspect import cleandoc

class ScriptTransformer(Transformer):
	def datasource(self, t):
		# t[0] is a dict containing the properties
		#print(t[0])
		return t

	def memmap(self, t):
		#print(t[0])
		return t[0]

	# mmentry: range NAME ["<" mmdataaddr] properties?
	def mmentry(self, t):
		length = len(t)
		data = None
		props = None
		if length==2:
			ivl, name = t
		elif length==3:
			ivl = t[0]
			name = t[1]
			if isinstance(t[2], int):
				data = t[2]
			else:
				props = t[2]
		else: #length==4
			ivl, name, data, props = t

		return ivl, name, data, props

	def mmbody(self, t):
		return t

	def range(self, t):
		return Interval(int(t[0]), int(t[1])) if len(t)==2 else Interval(int(t[0]))

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
	def quoted(self, t):
		return t[0][1:-1]
	def tquoted(self, t):
		return cleandoc(t[0][2:-2])
	def name(self, t):
		return str(t[0])

	def comment(self, t):
		l = len(t)
		if l==2:
			pos = 'v'
			ivl, txt = t
		else: # i==3
			ivl, pos, txt = t
		#print(ivl, pos, txt)
		return t
	def cpos(self, t):
		return str(t[0])

	def label(self, t):
		l = len(t)
		if l==2:
			flags = ""
			pos = 'v'
			ivl, name = t
		else: # i==3
			ivl, flags, name = t
		#print(ivl, flags, name)
		return t
	def lflags(self, t):
		return str(t[0])

if __name__=='__main__':
	with open("MemType.txt", "r") as f:
		t = f.read()

	l = Lark(open("script.lark").read(), parser='lalr', debug=True)

	t = l.parse(t)
	#print(t.pretty())
	ScriptTransformer().transform(t)
