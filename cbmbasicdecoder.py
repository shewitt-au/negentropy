import decoders
from cbmbasic import *
from interval import Interval

class BasicDecoder(decoders.Prefix):
	def __init__(self, name):
		self.name = name

	def cutting_policy(self):
		return decoders.CuttingPolicy.Guided

	def preprocess(self, ctx, ivl, cutter):
		token = None
		p = Parser(ctx.mem, ivl)
		for token in p.tokens():
			if token.type == TokenType.LineLink:
				line_first = token.ivl.first
				ctx.link_add_reachable(line_first)
			elif token.type == TokenType.LineEnd:
				cutter.atomic(Interval(line_first, token.ivl.last))
			elif token.type == TokenType.LineNumberReference:
				addr = line_to_address(ctx.mem, ivl, token.value(ctx.mem))
				ctx.link_add_referenced(addr)
		cutter.done()

		# return the non-processed part of the interval
		unproc = Interval(token.ivl.last+1, ivl.last) if token else ivl
		return unproc
			
	def decode(self, ctx, ivl, params=None):
		def lines():
			def annotated_tokens():
				# TODO: We should use 'params' to pass data in
				for token in line_tokens(ctx.mem, livl, "c64font" in ctx.flags):
					if token['type'] == 'line_ref':
						target = line_to_address(ctx.mem, ivl, token['val'])
						token['is_source'] = ctx.is_destination(target)
						token['target'] = target
					elif token['type'] == 'address':
						target = token['val']
						token['is_source'] = ctx.is_destination(target)
						token['target'] = target
					yield token

			target_already_exits = params['target_already_exits']
			for livl in line_iterator(ctx.mem, ivl):
				yield {
					'type': 'line',
					'address': livl.first,
					'tokens': annotated_tokens(),
					'is_destination': (not target_already_exits) and (ctx.is_destination(livl.first)),
					'address': livl.first
				}
				target_already_exits = False

		return {
			'type': self.name,
			'lines': lines()
		}
