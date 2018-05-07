from interval import Interval
import decoders

class BytesDecoder(decoders.Prefix):
	def __init__(self, name, linelen):
		self.name = name
		self.linelen = linelen

	def targets(self, ctx, ivl):
		pass

	def decode(self, ctx, ivl, params):
		def lines(self):
			target_already_exits = params['target_already_exits']
			for addr in range(ivl.first, ivl.last+1, self.linelen):
				yield {
					'address': addr,
					'is_destination' : not target_already_exits and addr in ctx.targets,
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

	def targets(self, ctx, ivl):
		for addr in ivl:
			ctx.targets.add(ctx.mem.r16(addr))

	def decode(self, ctx, ivl, params):
		def value(addr):
			v = ctx.mem.r16(addr)
			return {"val": ctx.syms.get(v, "{:04x}".format(v)), "is_source": ctx.contains(v), "target": v}

		def lines(self):
			bpl = 2*self.linelen
			target_already_exits = params['target_already_exits']
			for addr in range(ivl.first, ivl.last+1, bpl):
				yield {
					'address': addr,
					'is_destination' : not target_already_exits and addr in ctx.targets,
					'vals': [value(a) for a in range(addr, addr+min(ivl.last-addr+1, self.linelen*2), 2)]
					}
				target_already_exits = False

		return {
			'type': self.name,
			'lines': lines(self)
			}
