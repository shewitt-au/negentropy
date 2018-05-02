from heapq import merge
from interval import Interval
import decoders

class BytesDecoder(object):
	def __init__(self, name, linelen):
		self.name = name
		self.linelen = linelen

	def targets(self, ctx, ivl):
		return set()

	def decode(self, ctx, ivl, params):
		for i in ivl.cut_left_iter(merge(ctx.syms.keys_in_range(ivl), ctx.cmts.keys_in_range(ivl))):
			base_val = ctx.prefix(i)
			yield {
					**base_val,
					**{
						"type" : self.name,
						"address": i.first,
						"is_destination" : i.first in ctx.targets,
						"bytes": ctx.mem.r8m(i.first, min(len(i), self.linelen))
					}
				}
			for addr in range(i.first+self.linelen, i.last+1, self.linelen):
				yield {
					"type" : self.name,
					"address": addr,
					"is_destination" : addr in ctx.targets,
					"bytes": ctx.mem.r8m(addr, min(i.last-addr+1, self.linelen))
					}


class PointerDecoder(object):
	def __init__(self, name, linelen):
		self.name = name
		self.linelen = linelen

	def targets(self, ctx, ivl):
		tgts = set()

		addr = ivl.first
		while addr<=ivl.last:
			tgts.add(ctx.mem.r16(addr))
			addr += 2

		return tgts

	def decode(self, ctx, ivl, params):
		def value(addr):
			v = ctx.mem.r16(addr)
			return {"val": ctx.syms.get(v, "{:04x}".format(v)), "is_source": ctx.contains(v), "target": v}

		bpl = 2*self.linelen

		for i in ivl.cut_left_iter(merge(ctx.syms.keys_in_range(ivl), ctx.cmts.keys_in_range(ivl))):
			base_val = ctx.prefix(i)
			yield {
					**base_val,
					**{
						"type" : self.name,
						"address": i.first,
						"is_destination" : i.first in ctx.targets,
						"vals": [value(a) for a in range(i.first, i.first+min(len(i), self.linelen*2), 2)]
					}
				}
			for addr in range(i.first+bpl, i.last+1, bpl):
				yield {
					"type" : self.name,
					"address": addr,
					"is_destination" : addr in ctx.targets,
					"vals": [value(a) for a in range(addr, addr+min(i.last-addr+1, self.linelen*2), 2)]
					}
