from heapq import merge
from interval import Interval

def decode(ctx, ivl):
	for i in ivl.cut_left_iter(merge(ctx.syms.keys_in_range(ivl), ctx.cmts.keys_in_range(ivl))):
		c = ctx.cmts.get(i.first)
		yield {
			"type" : "data",
			"address": i.first,
			"label" : ctx.syms.get(i.first),
			"comment_before": None if c is None else c[0],
			"comment_after": None if c is None else c[1],
			"comment_inline": None if c is None else c[2],
			"bytes": ctx.mem.r(ivl.first, min(len(ivl), 16))
			}
		for addr in range(i.first+16, i.last+1, 16):
			yield {
				"type" : "data",
				"address": addr,
				"bytes": ctx.mem.r(addr, min(i.last-addr+1, 16))
				}
