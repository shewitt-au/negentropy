from enum import Enum, unique, auto
from heapq import merge
import memory as memmod
import memmap
import symbols as symmod
from interval import Interval
from memtypeparser import *

@unique
class CuttingPolicy(Enum):
	Automatic = auto()
	Guided  = auto()
	Dont = auto()

class GuidedCutter(object):
	def __init__(self, ctx, ivl, coll):
		self.cuts = merge(ctx.syms.keys_in_range(ivl), ctx.cmts[0].keys_in_range(ivl))
		self.current = Interval()
		self.coll = coll
		self._next_cut()

	def _next_cut(self):
		try:
			self.cut = next(self.cuts)
		except StopIteration:
			self.cut = None

	# Add an atomic region that can't be cut. Cuts only occur at joins.
	# If a cut point isn't present at a join the regions are merged.
	# Cuts at other locations are ignored.
	# TODO: flag the ignored cuts and log.
	def atomic(self, ivl):
		self.current = Interval.union(self.current, ivl)
		if self.cut is None:
			return

		while self.cut<=ivl.last:
			self._next_cut()
			if self.cut is None:
				return

		if self.cut==(ivl.last+1):
			self.coll.append(self.current)
			self.current = Interval()

	def done(self):
		if not self.current.is_empty():
			self.coll.append(self.current)

class Context(object):
	def __init__(self, args, decoders):
		self.args = args
		self.decoders = decoders
		with open(args.input, "rb") as f:
			contents = f.read()
			self.mem = memmod.Memory(contents, args.origin)
		self.mem_range = self.mem.range()
		self.syms = symmod.SymbolTable()
		#self.cmts = symmod.read_comments(comments)
		# TODO: This is a mess. Make a comments class
		self.cmts = (symmod.DictWithRange(), symmod.DictWithRange())
		#
		self.links_referenced_addresses = set()
		self.links_reachable_addresses = set()
		self.memtype = memmap.MemType(self, args.defaultdecoder)
		self.holes = 0

		# parse
		l = Listener(self, self.args.memtype)

	def link_add_referenced(self, addr):
		self.links_referenced_addresses.add(addr)

	def link_add_reachable(self, addr):
		self.links_reachable_addresses.add(addr)

	def is_destination(self, addr):
		 return (addr in self.links_reachable_addresses and 
		 		 addr in self.links_referenced_addresses)

	def preprocess(self, ivl=None):
		self.memtype.preprocess(self, ivl)

	def items(self, ivl=None):
		return self.memtype.items(self, ivl)

class Prefix(object):
	def intro(self, ctx, memtype):
		if ctx.args.info:
			return {
				'type': "intro",
				'ivl': memtype.ivl,
				'section_type': self.name
				}
		else:
			return None

	def prefix(self, ctx, ivl, params):
		c = ctx.cmts[0].by_address.get(ivl.first)
		is_destination = ctx.is_destination(ivl.first)
		params['target_already_exits'] = is_destination
		s = ctx.syms.by_address.get(ivl.first)
		return {
			'type': "prefix",
			'address': ivl.first,
			'is_destination' : is_destination,
			'label': None if s is None else s[1],
			'comment_before': None if c is None else c[1],
			'comment_after': None if c is None else c[2]
			}

	def cutting_policy(self):
		return CuttingPolicy.Automatic
