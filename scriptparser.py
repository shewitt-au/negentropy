from lark import Lark, Transformer

class ScriptTransformer(Transformer):
	def datasource(self, t):
		print(t)
		length = len(t)
		assert length==1 or length==2, "Syntax error"
		if length==1:
			p = (None, t[0])
		else:
			p = (str(t[0]), t[1])
		print("datasource: ", p)
		return p

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

	l = Lark(open("script.lark").read(), parser='lalr')

	t = l.parse(t)
	#print(t.pretty())
	ScriptTransformer().transform(t)
