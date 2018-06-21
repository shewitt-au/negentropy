from antlr4 import *
from antlrparser.memmapLexer import memmapLexer
from antlrparser.memmapParser import memmapParser
from antlrparser.memmapListener import memmapListener
import memmap

class Listener(memmapListener):
	def __init__(self, ctx, regions):
		self.ctx = ctx
		self.regions = regions

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

				## DOES STUFF
				print("\t"+ent.mmrange().mmfirst().getText()+"-"+ent.mmrange().mmlast().getText(), end="")
				print(" "+ent.mmdecoder().getText(), end="")

				ft = ent.mmrange().mmfirst().getText()
				lt = ent.mmrange().mmlast().getText()
				dt = ent.mmdecoder().getText()

				self.regions.append(memmap.MemRegion(
						self.ctx.decoders[ent.mmdecoder().getText()],
						ft[1:],
						lt[1:],
						{}
						))
				#############


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
