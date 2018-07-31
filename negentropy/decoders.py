import os
import glob
from enum import Enum, unique, auto
from heapq import merge

from .interval import Interval
from . import memory as memmod
from . import memmap
from . import symbols as symmod
from . import scriptparser

@unique
class CuttingPolicy(Enum):
	Automatic = auto()
	Guided  = auto()
	Dont = auto()

class GuidedCutter(object):
	def __init__(self, ctx, ivl, coll):
		self.cuts = merge(ctx.syms.left_edges(ivl), ctx.cmts.cuts(ivl))
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

		self.basedir = os.path.dirname(args.output)
		if self.basedir and not os.path.exists(self.basedir):
			os.makedirs(self.basedir)

		self.sourcedir = os.path.dirname(__file__)

		self.decoders = decoders
		self.syms = symmod.SymbolTable()
		self.cmts = symmod.Comments()
		self.directives = symmod.Directives()
		self.links_referenced_addresses = set()
		self.links_reachable_addresses = set()
		self.memtype = memmap.MemType(self, args.defaultdecoder)
		self.holes = 0
		self.datasource_props = {}
		self.have_indexables = False

		# parse
		config = args.config if args.config is not None else []
		if not args.noc64symbols:
			config.append(self.source_file("symbols", "c64.txt"))
		if config:
			self.directives.parse_begin()
			for fn in config:
				scriptparser.parse(self, fn)
			self.directives.parse_end(self)

		self.syms.clashes()

		# read the file
		if not args.input:
			input = self.datasource_props.get('file', args.input)
			origin = self.datasource_props.get('origin', args.origin)
		else:
			input = args.input
			origin = args.origin
		with open(input, "rb") as f:
			contents = f.read()
			self.mem = memmod.Memory(contents, origin)

	def file(self, fn):
		return os.path.join(self.basedir, fn)

	def source_file(self, *fns):
		return os.path.join(self.sourcedir, *fns)

	def template(self):
		return os.path.basename(glob.glob("{}/templates/{}.*".format(os.path.dirname(__file__), self.args.format))[0])

	def implfile(self, fn):
		return os.path.join(os.path.dirname(__file__), fn)

	def parse_datasource(self, props):
		self.datasource_props = props


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
		c = ctx.cmts.get(ivl.first)
		is_destination = ctx.is_destination(ivl.first)
		params['target_already_exits'] = is_destination
		s = ctx.syms.lookup(ivl.first, name_unknowns=False)
		return {
			'type': "prefix",
			'address': ivl.first,
			'is_destination' : is_destination,
			'label': s.name,
			'comment_before': None if c is None else c.before,
			'comment_after': None if c is None else c.after
			}

	def cutting_policy(self):
		return CuttingPolicy.Automatic
