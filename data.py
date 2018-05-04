from interval import Interval
import decoders

class BytesDecoder(decoders.Prefix):
	def __init__(self, name, linelen):
		self.name = name
		self.linelen = linelen

	def targets(self, ctx, ivl):
		return set()

	def decode(self, ctx, ivl, first_target, params):
		def lines(self):
			ft = first_target
			for addr in range(ivl.first, ivl.last+1, self.linelen):
				yield {
					"address": addr,
					"is_destination" : ft and addr in ctx.targets,
					"bytes": ctx.mem.r8m(addr, min(ivl.last-addr+1, self.linelen))
					}
				ft = True

		return {
			"type": self.name,
			"lines": lines(self)
			}

class PointerDecoder(decoders.Prefix):
	def __init__(self, name, linelen):
		self.name = name
		self.linelen = linelen

	def targets(self, ctx, ivl):
		tgts = set()
		for addr in ivl:
			tgts.add(ctx.mem.r16(addr))

		return tgts

	def decode(self, ctx, ivl, first_target, params):
		def value(addr):
			v = ctx.mem.r16(addr)
			return {"val": ctx.syms.get(v, "{:04x}".format(v)), "is_source": ctx.contains(v), "target": v}

		def lines(self):
			bpl = 2*self.linelen
			for addr in range(ivl.first, ivl.last+1, bpl):
				ft = first_target
				yield {
					"address": addr,
					"is_destination" : ft and addr in ctx.targets,
					"vals": [value(a) for a in range(addr, addr+min(ivl.last-addr+1, self.linelen*2), 2)]
					}
				ft = True

		return {
			"type": self.name,
			"lines": lines(self)
			}
