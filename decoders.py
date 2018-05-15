import memory as memmod
import symbols as symmod
from interval import Interval

class Context(object):
	def __init__(self, decoders, address, memory, memtype, default_decoder, symbols, comments):
		self.decoders = decoders
		self.memtype = memmod.MemType(self, memtype, decoders, default_decoder)
		with open(memory, "rb") as f:
			contents = f.read()
			self.mem = memmod.Memory(contents, 0 if address is None else address)
			if address is None:
				address = self.mem.r16(0)
				self.mem.org = address
		self.mem_range = Interval(address, address+len(contents)-1)
		self.syms = symmod.read_symbols(symbols)
		self.cmts = symmod.read_comments(comments)
		self.link_sources = set()
		self.link_destinations = set()
		self.holes = 0

	def preprocess(self, ivl=None):
		if not ivl:
			ivl = self.mem_range
		self.memtype.preprocess(self, ivl)

	def items(self, ivl=None):
		if not ivl:
			ivl = self.mem_range
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
