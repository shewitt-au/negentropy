import memory as memmod
import memmap
import symbols as symmod
from interval import Interval

class Context(object):
	def __init__(self, decoders, address, memory, memtype, default_decoder, symbols, comments, flags):
		self.decoders = decoders
		with open(memory, "rb") as f:
			contents = f.read()
			self.mem = memmod.Memory(contents, address)
		self.mem_range = self.mem.range()
		self.syms = symmod.read_symbols(symbols)
		self.cmts = symmod.read_comments(comments)
		self.links_referenced_addresses = set()
		self.links_reachable_addresses = set()
		self.holes = 0
		self.memtype = memmap.MemType(self, memtype, default_decoder)
		self.flags = flags

	def link_add_referenced(self, addr):
		self.links_referenced_addresses.add(addr)

	def link_add_reachable(self, addr):
		self.links_reachable_addresses.add(addr)

	def is_destination(self, addr):
		 return (addr in self.links_reachable_addresses and 
		 		 addr in self.links_referenced_addresses)

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
		is_destination = ctx.is_destination(ivl.first)
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
