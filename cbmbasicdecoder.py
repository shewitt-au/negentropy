import decoders
from cbmbasic import *

class BasicDecoder(decoders.Prefix):
	def preprocess(self, ctx, ivl):
		for livl in line_iterator(ctx.mem, ivl):
			ctx.link_add_reachable(livl.first)

			for token in line_tokens(ctx.mem, livl):
				tp = token['type']
				if tp=='line_num':
					addr = line_to_address(ctx.mem, ivl, token['val'])
					ctx.link_add_referenced(addr)
				elif tp=='address':
					ctx.link_add_referenced(token['val'])
			
	def decode(self, ctx, ivl, params=None):
		def lines():
			def annotated_tokens():
				for token in line_tokens(ctx.mem, livl):
					if token['type'] == 'line_num':
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
				target_already_exits

		return {
			'type': 'basic',
			'lines': lines()
		}
