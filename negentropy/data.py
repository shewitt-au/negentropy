from .interval import Interval
from . import decoders

class BytesDecoder(decoders.Prefix):
	def __init__(self, name, linelen):
		self.name = name
		self.linelen = linelen

	def preprocess(self, ctx, ivl):
		for addr in range(ivl.first, ivl.last+1, self.linelen):
			ctx.link_add_reachable(addr)
		# return the non-processed part of the interval
		return Interval()

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

	def cutting_policy(self):
		return decoders.CuttingPolicy.Guided

	def preprocess(self, ctx, ivl, cutter):
		mem = ctx.mem.view(ivl)

		bpl = 2*self.linelen
		for addr in range(ivl.first, ivl.last+1, bpl):
			ctx.link_add_reachable(addr)
		for addr in range(ivl.first, ivl.last+1, 2):
			cutter.atomic(ivl)
			ctx.link_add_referenced(mem.r16(addr))
		cutter.done()

		# return the non-processed part of the interval
		return Interval(addr+2, ivl.last)

	def decode(self, ctx, ivl, params):
		mem = ctx.mem.view(ivl)

		def value(addr):
			v = mem.r16(addr)
			e = ctx.syms.lookup(v)
			return {"val": e, "is_source": ctx.is_destination(e.addr)}

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
