from antlr4 import *
from antlrparser.memmapLexer import memmapLexer
from antlrparser.memmapParser import memmapParser
from antlrparser.memmapListener import memmapListener
import memmap
from interval import Interval

class Listener(memmapListener):
	def __init__(self, ctx, map, fname):
		self._ok = False
		if not fname:
			return
		self.ctx = ctx
		self.mem = map
		self.data_address = None

		input = FileStream(fname)
		lexer = memmapLexer(input)
		stream = CommonTokenStream(lexer)
		parser = memmapParser(stream)
		tree = parser.r()

		if not parser.getNumberOfSyntaxErrors():
			walker = ParseTreeWalker()
			walker.walk(self, tree)

	def got_data(self):
		return self._ok

	def enterDatasource(self, ctx:memmapParser.DatasourceContext):
		#print("datasource ", end="")
		#print(ctx.dsname().getText())
		#print("{")
		#print("\tfile = "+ctx.dsentry().dsfile().getText())
		#print("}")
		pass

	def enterMemmap(self, ctx:memmapParser.MemmapContext):
		#print("\nmemmap ", end="")
		#print(ctx.mmname().getText(), end="")
		#src = ctx.mmdatasource()
		#if src:
		#	print("("+src.getText()+")")

		def getValue(n):
			def var2Type(v):
				if v.number():
					ns = v.number().getText()
					return int(ns[1:], 16) if ns[0]=='$' else int(ns)
				elif v.string_():
					return v.string_().getText()[1:-1]
				elif v.boolean_():
					return v.boolean_().getText()=='True'

			pval = pe.propval()
			v = pval.variant()
			if v:
				return var2Type(v)
			else:
				l = pval.list_()
				if l:
					return [var2Type(e) for e in l.variant()]

		body = ctx.mmbody()
		if body:
			for ent in body.mmentry():
				self._ok = True

				ft = ent.mmrange().mmfirst().getText()
				lt = ent.mmrange().mmlast().getText()
				dt = ent.mmdecoder().getText()
				dataaddr = ent.mmdataaddr()
				if not dataaddr is None:
					dataaddrt = dataaddr.getText()
					if dataaddrt=='*':
						self.data_address = None
					else:
						self.data_address = int(dataaddrt[1:], 16)

				props = {}
				props_node = ent.properties()
				if props_node:
					for pe in props_node.propentry():
						name = pe.propname().getText()
						props[name] = getValue(pe.propval())

				self.mem.map.append(memmap.MemRegion(
						self.ctx.decoders[ent.mmdecoder().getText()],
						ft[1:],
						lt[1:],
						props,
						self.data_address
						))

				if not self.data_address is None:
					self.data_address += len(Interval(ft[1:], lt[1:]))
