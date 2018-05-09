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
		self.link_sources = set()
		self.link_destinations = set()

	def items(self, ivl):
		return self.memtype.items(self, ivl)

class Prefix(object):
	def prefix(self, ctx, ivl, params):
		c = ctx.cmts.by_address.get(ivl.first)
		is_destination = ivl.first in ctx.link_sources
		params['target_already_exits'] = is_destination
		s = ctx.syms.by_address.get(ivl.first)
		return {
			'type': "prefix",
			'address': ivl.first,
			'is_destination' : is_destination,
			'label': None if s is None else s[1],
			'comment_before': None if c is None else c[1],
			'comment_after': None if c is None else c[2],
			'comment_inline': None if c is None else c[3]
			}
