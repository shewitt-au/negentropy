from heapq import merge
from interval import Interval

def data_decoder(name, wordlen, linelen):
	def decode_data(ctx, ivl, params):
		if wordlen==1:
			b = ctx.mem.r8m
		elif wordlen==2:
			b = ctx.mem.r16m
		else:
			raise IndexError("Illegal operand size.")
		bpl = wordlen*linelen

		for i in ivl.cut_left_iter(merge(ctx.syms.keys_in_range(ivl), ctx.cmts.keys_in_range(ivl))):
			c = ctx.cmts.get(i.first)
			yield {
				"type" : name,
				"address": i.first,
				"label" : ctx.syms.get(i.first),
				"comment_before": None if c is None else c[0],
				"comment_after": None if c is None else c[1],
				"comment_inline": None if c is None else c[2],
				"bytes": b(i.first, min(len(i), linelen))
				}
			for addr in range(i.first+bpl, i.last+1, bpl):
				yield {
					"type" : name,
					"address": addr,
					"bytes": b(addr, min(i.last-addr+1, linelen))
					}

	return decode_data
