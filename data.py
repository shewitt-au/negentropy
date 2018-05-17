import decoders

class BytesDecoder(decoders.Prefix):
	def __init__(self, name, linelen):
		self.name = name
		self.linelen = linelen

	def preprocess(self, ctx, ivl):
		for addr in range(ivl.first, ivl.last+1, self.linelen):
			ctx.add_link_destination(addr)

	def decode(self, ctx, ivl, params):
		def lines(self):
			target_already_exits = params['target_already_exits']
			for addr in range(ivl.first, ivl.last+1, self.linelen):
				yield {
					'address': addr,
					'is_destination' : not target_already_exits and ctx.is_destination(addr),
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

	def preprocess(self, ctx, ivl):
		bpl = 2*self.linelen
		for addr in range(ivl.first, ivl.last+1, bpl):
			ctx.add_link_destination(addr)
		for addr in range(ivl.first, ivl.last+1, 2):
			ctx.add_link_source(ctx.mem.r16(addr))

	def decode(self, ctx, ivl, params):
		def value(addr):
			v = ctx.mem.r16(addr)
			s = ctx.syms.by_address.get(v)
			val = "{:04x}".format(v) if s is None else s[1]
			return {"val": val, "is_source": ctx.is_destination(v), "target": v}

		def lines(self):
			bpl = 2*self.linelen
			target_already_exits = params['target_already_exits']
			for addr in range(ivl.first, ivl.last+1, bpl):
				yield {
					'address': addr,
					'is_destination' : not target_already_exits and ctx.is_destination(addr),
					'vals': [value(a) for a in range(addr, addr+min(ivl.last-addr+1, self.linelen*2), 2)]
					}
				target_already_exits = False

		return {
			'type': self.name,
			'lines': lines(self)
			}
