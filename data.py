from heapq import merge
from interval import Interval
import decoders

def data_decoder(name, wordlen, linelen):
	def decode_data(ctx, ivl, params):
		if wordlen==1:
			rd = ctx.mem.r8m
		elif wordlen==2:
			rd = ctx.mem.r16m
		else:
			raise IndexError("Illegal operand size.")
		bpl = wordlen*linelen

		for i in ivl.cut_left_iter(merge(ctx.syms.keys_in_range(ivl), ctx.cmts.keys_in_range(ivl))):
			base_val = decoders.base_decoder(ctx, i)
			yield {
					**base_val,
					**{
						"type" : name,
						"address": i.first,
						"bytes": rd(i.first, min(len(i), linelen))
					}
				}
			for addr in range(i.first+bpl, i.last+1, bpl):
				yield {
					"type" : name,
					"address": addr,
					"bytes": rd(addr, min(i.last-addr+1, linelen))
					}

	return decode_data
