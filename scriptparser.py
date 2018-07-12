from lark import Lark, Transformer
from interval import Interval

class ScriptTransformer(Transformer):
	def datasource(self, t):
		length = len(t)
		assert length==1 or length==2, "Syntax error"
		if length==1:
			p = (None, t[0])
		else:
			p = (str(t[0]), t[1])
		return p

	def memmap(self, t):
		length = len(t)
		if length==1:
			p = (None)
		elif length==2:
			p = (str(t[0]))
		elif length==3:
			p = (str(t[0]), str(t[1]))
		#print(t)

	def mmentry(self, t):
		pass

	def range(self, t):
		print(Interval(int(t[0]), int(t[1])) if len(t)==2 else Interval(int(t[0])))
		return Interval(int(t[0]), int(t[1])) if len(t)==2 else Interval(int(t[0]))

	def properties(self, t):
		return {str(i[0]) : i[1] for i in t}
	def propentry(self, t):
		return t
	def hexnum(self, t):
		return int(t[0][1:], 16)
	def decimal(self, t):
		return int(t[0])
	def string(self, t):
		return str(t[0])
	def boolean(self, t):
		return bool(t[0])
	def list(self, t):
		return list(t)
	
if __name__=='__main__':
	with open("MemType.txt", "r") as f:
		t = f.read()

	l = Lark(open("script.lark").read(), parser='lalr', debug=True)

	t = l.parse(t)
	#print(t.pretty())
	ScriptTransformer().transform(t)
