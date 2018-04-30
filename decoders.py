import memory as memmod
import symbols as symmod
import M6502
import data
import gfx

class BaseDecoder(object):
	def __init__(self, decoders, address, memory, memtype, symbols, comments):
		self.decoders = decoders
		self.memtype = memmod.MemType(memtype, decoders)
		with open("5000-8fff.bin", "rb") as f:
			self.mem = memmod.Memory(f.read(), address)
		self.syms = symmod.read_symbols(*symbols)
		self.cmts = symmod.read_comments(comments)

	def prefix(self, ivl):
		c = self.cmts.get(ivl.first)
		return {
			"label" : self.syms.get(ivl.first),
			"comment_before": None if c is None else c[0],
			"comment_after": None if c is None else c[1],
			"comment_inline": None if c is None else c[2]
			}

	def targets(self, ivl):
		return self.memtype.targets(self, ivl)

	def decode(self, ivl):
		return self.memtype.decode(self, ivl)
