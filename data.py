from heapq import merge
from interval import Interval

def data_decoder(name, size=8):
	def decode_data(ctx, ivl):
		if size==8:
			b = ctx.mem.r8m
			n = 16
		elif size==16:
			b = ctx.mem.r16m
			n = 32
		else:
			raise IndexError("Illegal operand size.")

		for i in ivl.cut_left_iter(merge(ctx.syms.keys_in_range(ivl), ctx.cmts.keys_in_range(ivl))):
			c = ctx.cmts.get(i.first)
			yield {
				"type" : name,
				"address": i.first,
				"label" : ctx.syms.get(i.first),
				"comment_before": None if c is None else c[0],
				"comment_after": None if c is None else c[1],
				"comment_inline": None if c is None else c[2],
				"bytes": b(ivl.first, min(len(ivl), n))
				}
			for addr in range(i.first+n, i.last+1, n):
				yield {
					"type" : name,
					"address": addr,
					"bytes": b(addr, min(i.last-addr+1, n))
					}

	return decode_data
