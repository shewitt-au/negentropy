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
		for livl in line_iterator(ctx.mem, ivl):
			cutter.atomic(livl)
			ctx.link_add_reachable(livl.first)

			for token in line_tokens(ctx.mem, livl):
				tp = token['type']
				if tp=='line_ref':
					addr = line_to_address(ctx.mem, ivl, token['val'])
					ctx.link_add_referenced(addr)
				elif tp=='address':
					ctx.link_add_referenced(token['val'])
		cutter.done()

		# return the non-processed part of the interval
		unproc = Interval(token['ivl'].last+4, ivl.last) if token else ivl # +1 to NULL line term, +1 to skip it, +2 over link
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
