import memory as memmod
import symbols as symmod

class Context(object):
	def __init__(self, decoders, address, memory, memtype, symbols, comments):
		self.decoders = decoders
		self.memtype = memmod.MemType(memtype, decoders)
		with open("5000-8fff.bin", "rb") as f:
			self.mem = memmod.Memory(f.read(), address)
		self.syms = symmod.read_symbols(*symbols)
		self.cmts = symmod.read_comments(comments)

	def contains(self, addr):
		return self.memtype.contains(addr)

	def targets(self, ivl):
		self.targets = self.memtype.targets(self, ivl)

	def decode(self, ivl):
		self.targets(ivl)
		return self.memtype.decode(self, ivl)

class Prefix(object):
	def prefix(self, ctx, ivl):
		c = ctx.cmts.get(ivl.first)
		return {
			"type": "prefix",
			"address": ivl.first,
			"is_destination" : ivl.first in ctx.targets,
			"label": ctx.syms.get(ivl.first),
			"comment_before": None if c is None else c[0],
			"comment_after": None if c is None else c[1],
			"comment_inline": None if c is None else c[2]
			}
