import re
import bisect
from heapq import merge
import copy
import numbers

from .interval import Interval
from . import decoders

class BaseRegion(object):
	def __init__(self, first=None, last=None):
		self.ivl = Interval(first, last)

	def __eq__(self, other):
		return self.ivl == other

	def __ne__(self, other):
		return self.ivl != other

	def __lt__(self, other):
		return self.ivl < other

	def __le__(self, other):
		return self.ivl <= other

	def __gt__(self, other):
		return self.ivl > other

	def __ge__(self, other):
		return self.ivl >= other

	def __and__(self, other):
		cpy = copy.copy(self)
		cpy.ivl = self.ivl & other
		return cpy

# Represents a region of memory (C64's) and associates it with a specific decoder.
# Handles splitting the region into smaller ones at labels and comments.
class MemRegion(BaseRegion):
	def __init__(self, decoder, first, last=None, params=None, at=None):
		super().__init__(first, last)
		self.decoder = decoder
		self.params = params
		self.at = at
		self.is_hole = False
		self.subregions = []
		self.black_list = params.get('symbol_bypass')
		if self.black_list is not None:
			if isinstance(self.black_list, numbers.Number):
				self.black_list = [self.black_list]

	def context(self, ctx):
		if self.at is None:
			return ctx
		else:
			cpy = copy.copy(ctx)
			cpy.mem = ctx.mem.view(self.ivl, self.at)
			return cpy

	def _region_iterator(self, ctx):
		return self.ivl.cut_left_iter(
			merge(ctx.syms.left_edges(self.ivl), ctx.cmts.cuts(self.ivl))
			)

	def preprocess(self, ctx):
		ctx = self.context(ctx)
		cp = self.decoder.cutting_policy()
		if cp==decoders.CuttingPolicy.Automatic:
			regions = self._region_iterator(ctx)
			try:
				rgn = next(regions)
				self.subregions.append(rgn)
				remains = self.decoder.preprocess(ctx, rgn)
			except StopIteration:
				remains = self.ivl
			else:
				for rgn in regions:
					assert remains.is_empty(), "Cutting error! Consider using a guided cutter"
					self.subregions.append(rgn)
					remains = self.decoder.preprocess(ctx, rgn)
		elif cp==decoders.CuttingPolicy.Guided:
			cutter = decoders.GuidedCutter(ctx, self.ivl, self.subregions)
			remains = self.decoder.preprocess(ctx, self.ivl, cutter)
		else: # CuttingPolicy.Dont
			remains = self.decoder.preprocess(ctx, self.ivl)
			self.subregions.add(self.ivl)

		return remains

	def items(self, ctx):
		ctx = self.context(ctx)
		ctx.syms.black_list = self.black_list
		i = self.decoder.intro(ctx, self)
		if i is not None:
			yield i
		params = self.params.copy()
		for ivl in self.subregions:
			# using a clipped interval like this is the easiest way to allow
			# altering the interval without rewriting the subregions list.
			clipped_interval = ivl&self.ivl
			if not clipped_interval.is_empty():
				yield self.decoder.prefix(ctx, clipped_interval, params)
				yield self.decoder.decode(ctx, clipped_interval, params)
		ctx.syms.black_list = None

	def __str__(self):
		return "{}: decoder={}".format(self.ivl, self.decoder)

	def __repr__(self):
		return "MemRegion({})".format(str(self))

class CompoundMemRegion(BaseRegion):
	def __init__(self):
		super().__init__()
		self.contents = []

	def add(self, r):
		self.contents.append(r)
		if self.ivl.is_empty():
			self.ivl.assign(r.ivl)
		else:
			self.ivl.assign(Interval.union(self.ivl, r.ivl))

	def items(self, ctx):
		for r in self.contents:
			yield from r.items(ctx)

	def __str__(self):
		return "{}".format(self.contents)

	def __repr__(self):
		return "CompoundMemRegion({})".format(self.contents)

def fake_with_holes(envelope, coll):
	for ivl in coll:
		yield (ivl, False)

def with_holes(envelope, coll):
	it = iter(coll)
	try:
		first = next(coll)
	except StopIteration:
		# if the interval collection is empty return the envelope as a hole
		yield (envelope, True)
	else:
		assert envelope.contains(first.ivl), "'envelope' must contains all items in 'coll'"
		if first.ivl.first > envelope.first:
			# we have a hole before the contents of 'coll'
			yield (Interval(envelope.first, first.ivl.first-1), True)

		last = first
		for n in it:
			assert envelope.contains(n), "'envelope' must contains all items in 'coll'"
			yield (last, False)

			hole = Interval(last.ivl.last+1, n.ivl.first-1)
			if not hole.is_empty():
				yield (hole, True)

			last = n
	
		yield (last, False)

		if last.ivl.last < envelope.last:
			# we have a hole after the contents of 'coll'
			yield (Interval(last.ivl.last+1, envelope.last), True)

# A representation of the MemType.txt file. A collection of 'MemRegion's.
class MemType(object):
	def __init__(self, ctx, default_decoder=None):
		self.map = [] # A list of 'MemRegion's
		if default_decoder:
			self.default_decoder = ctx.decoders[default_decoder]
		else:
			self.default_decoder = None

	def parse_begin(self):
		self.got_parse_data = False

	def parse_add(self, ivl, decoder, props, data_addr):
		self.map.append(MemRegion(decoder, ivl.first, ivl.last, props, data_addr))
		self.got_parse_data = True

	def parse_end(self, ctx):
		if not self.got_parse_data:
			if self.default_decoder is None:
				self.default_decoder = ctx.decoders['data']
			self.map.append(MemRegion(self.default_decoder, ctx.mem.range().first, ctx.mem.range().last, {}))
		# Sort so adjacent ranges are next to each other. See 'overlapping_indices'.
		self.map.sort()

	def __len__(self):
		return len(self.map)

	def __getitem__(self, key):
		return self.map[key]

	def contains(self, addr):
		i = bisect.bisect_left(self.map, addr)
		return i!=len(self) and self[i]==addr

	# Iterates over the overlapping regions clipping the ends if they only
	# partially overlap.
	def overlapping(self, ivl):
		b = bisect.bisect_left(self.map, ivl.first)
		e = bisect.bisect_right(self.map, ivl.last, b)
		for idx in range(b, e):
			yield self[idx]&ivl

	def _region_iter(self, ctx, ivl):
		if self.default_decoder:
			return with_holes(ivl, self.overlapping(ivl))
		else:
			return fake_with_holes(ivl, self.overlapping(ivl))

	def envelope(self, ivl):
		if len(self)<1:
			return ivl
		return Interval.envelope(ivl, Interval(self[0].ivl.first, self[-1].ivl.last))

	def preprocess(self, ctx, ivl):
		new_map = []

		if ivl is None:
			ivl = ctx.mem.range()
			ivl = self.envelope(ivl)

		for region, is_hole in self._region_iter(ctx, ivl):
			if  is_hole:
				# we found a hole and we've got a default decoder
				if ctx.args.gaps:
					ctx.holes += 1
				dr = MemRegion(self.default_decoder, region.first, region.last, {})
				remains = dr.preprocess(ctx)
				if remains.is_empty():
					dr.is_hole = ctx.args.gaps
					new_map.append(dr)
				else:
					cr = CompoundMemRegion()
					dr.last = remains.first-1
					cr.add(dr)
					mr = MemRegion(ctx.decoders['data'], remains.first, remains.last, {})
					mr.preprocess(ctx)
					cr.add(mr)
					cr.is_hole = ctx.args.gaps
					new_map.append(cr)
			else:
				remains = region.preprocess(ctx)
				if not remains.is_empty():
					region_cpy = copy.copy(region)
					region_cpy.last = remains.first-1
					new_map.append(region_cpy)
					mr = MemRegion(ctx.decoders['data'], remains.first, remains.last, {})
					mr.preprocess(ctx)
					new_map.append(mr)
				else:
					new_map.append(region)

		self.map = new_map

	def items(self, ctx, ivl):
		hole_idx = 0

		if ivl is None:
			ivl = ctx.mem.range()
			ivl = self.envelope(ivl)

		for region in self.overlapping(ivl):
			if region.is_hole:
				# we found a hole and we've got a default decoder
				yield {
					'type': "hole",
					'contents': region.items(ctx),
					'name': "hole_"+str(hole_idx),
					'next': "hole_"+str(hole_idx+1) if (hole_idx+1<ctx.holes) else None
					}
				hole_idx += 1
			else:
				yield from region.items(ctx)
