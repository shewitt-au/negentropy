from interval import Interval
import decoders

class BytesDecoder(decoders.Prefix):
	def __init__(self, name, linelen):
		self.name = name
		self.linelen = linelen

	def links(self, ctx, ivl):
		for addr in range(ivl.first, ivl.last+1, self.linelen):
			ctx.link_destinations.add(addr)

	def decode(self, ctx, ivl, params):
		def lines(self):
			target_already_exits = params['target_already_exits']
			for addr in range(ivl.first, ivl.last+1, self.linelen):
				yield {
					'address': addr,
					'is_destination' : not target_already_exits and addr in ctx.link_sources,
					'bytes': ctx.mem.r8m(addr, min(ivl.last-addr+1, self.linelen))
					}
				target_already_exits = False

		return {
			'type': self.name,
			'lines': lines(self)
			}

class PointerDecoder(decoders.Prefix):
	def __init__(self, name, linelen):
		self.name = name
		self.linelen = linelen

	def links(self, ctx, ivl):
		bpl = 2*self.linelen
		for addr in range(ivl.first, ivl.last+1, bpl):
			ctx.link_destinations.add(addr)
		for addr in range(ivl.first, ivl.last+1, 2):
			ctx.link_sources.add(ctx.mem.r16(addr))

	def decode(self, ctx, ivl, params):
		def value(addr):
			v = ctx.mem.r16(addr)
			s = ctx.syms.get(v)
			val = "{:04x}".format(v) if s is None else s[1]
			return {"val": val, "is_source": v in ctx.link_destinations, "target": v}

		def lines(self):
			bpl = 2*self.linelen
			target_already_exits = params['target_already_exits']
			for addr in range(ivl.first, ivl.last+1, bpl):
				yield {
					'address': addr,
					'is_destination' : not target_already_exits and addr in ctx.link_sources,
					'vals': [value(a) for a in range(addr, addr+min(ivl.last-addr+1, self.linelen*2), 2)]
					}
				target_already_exits = False

		return {
			'type': self.name,
			'lines': lines(self)
			}
