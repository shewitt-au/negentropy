from heapq import merge
from interval import Interval
import decoders

class DataDecoder(object):
	def __init__(self, name, wordlen, linelen):
		self.name = name
		self.wordlen = wordlen
		self.linelen = linelen

	def targets(self, ctx, ivl):
		tgts = set()

		if self.wordlen == 1:
			rd = ctx.mem.r8
		else:
			rd = ctx.mem.r16

		addr = ivl.first
		while addr<=ivl.last:
			tgts.add(rd(addr))
			addr += self.wordlen

		return tgts

	def decode(self, ctx, ivl, params):
		def value(addr):
			if self.wordlen==1:
				v = ctx.mem.r8(addr)
				return {"val": "{:02x}".format(v), "is_source": ctx.contains(v), "target": v}
			else:
				v = ctx.mem.r16(addr)
				return {"val": ctx.syms.get(v, "{:04x}".format(v)), "is_source": ctx.contains(v), "target": v}


		bpl = self.wordlen*self.linelen

		for i in ivl.cut_left_iter(merge(ctx.syms.keys_in_range(ivl), ctx.cmts.keys_in_range(ivl))):
			base_val = ctx.prefix(i)
			yield {
					**base_val,
					**{
						"type" : self.name,
						"address": i.first,
						"is_destination" : i.first in ctx.targets,
						"vals": [value(a) for a in range(i.first, i.first+min(len(i), self.linelen), self.wordlen)]
					}
				}
			for addr in range(i.first+bpl, i.last+1, bpl):
				yield {
					"type" : self.name,
					"address": addr,
					"is_destination" : addr in ctx.targets,
					"vals": [value(a) for a in range(addr, addr+min(i.last-addr+1, self.linelen), self.wordlen)]
					}
