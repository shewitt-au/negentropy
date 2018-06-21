from antlr4 import *
from antlrparser.memmapLexer import memmapLexer
from antlrparser.memmapParser import memmapParser
from antlrparser.memmapListener import memmapListener

class Listener(memmapListener):
	def enterDatasource(self, ctx:memmapParser.DatasourceContext):
		print("datasource ", end="")
		print(ctx.dsname().getText())
		print("{")
		print("\tfile = "+ctx.dsentry().dsfile().getText())
		print("}")

	def enterMemmap(self, ctx:memmapParser.MemmapContext):
		print("\nmemmap ", end="")
		print(ctx.mmname().getText(), end="")
		src = ctx.mmdatasource()
		if src:
			print("("+src.getText()+")")

		body = ctx.mmbody()
		if body:
			print("{")
			for ent in body.mmentry():
				print("\t"+ent.mmrange().mmfirst().getText()+"-"+ent.mmrange().mmlast().getText(), end="")
				print(" "+ent.mmdecoder().getText(), end="")
				if not ent.mmfrom() is None:
					print(" < "+ent.mmfrom().getText(), end="")
				print()
				props = ent.properties()
				if props:
					print("\t{")
					for pe in props.propentry():
						print("\t\t"+pe.propname().getText()+" = ", end="")
						pval = pe.propval()
						v = pval.variant()
						if v:
							print(v.getText())
						else:
							l = pval.list_()
							if l:
								print(",".join([v.getText() for v in l.variant()]))
					print("\t}")
			print("}")

if __name__=='__main__':
	input = FileStream('in.txt')
	lexer = memmapLexer(input)
	stream = CommonTokenStream(lexer)
	parser = memmapParser(stream)
	#parser._errHandler = BailErrorStrategy()
	tree = parser.r()

	if not parser.getNumberOfSyntaxErrors():
		l = Listener()
		walker = ParseTreeWalker()
		walker.walk(l, tree)

	print()
