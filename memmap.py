import re
import bisect
from heapq import merge
import copy
from interval import Interval
import decoders

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
	def __init__(self, decoder, first, last=None, params=None):
		super().__init__(first, last)
		self.decoder = decoder
		self.params = params
		self.is_hole = False
		self.subregions = []

	def _region_iterator(self, ctx):
		return self.ivl.cut_left_iter(merge(ctx.syms.keys_in_range(self.ivl), ctx.cmts.keys_in_range(self.ivl)))

	def preprocess(self, ctx):
		cp = self.decoder.cutting_policy()
		if cp==decoders.CuttingPolicy.Automatic:
			remains = self.ivl
			for region in self._region_iterator(ctx):
				self.subregions.append(region)
			remains = self.decoder.preprocess(ctx, self.ivl)
		elif cp==decoders.CuttingPolicy.Guided:
			cutter = decoders.GuidedCutter(ctx, self.ivl, self.subregions)
			remains = self.decoder.preprocess(ctx, self.ivl, cutter)
		else: # CuttingPolicy.Dont
			remains = self.decoder.preprocess(ctx, self.ivl)

		return remains

	def items(self, ctx):
		params = self.params.copy()
		for ivl in self.subregions:
			# using a clipped interval like this is the easiest way to allow
			# altering the interval without rewriting the subregions list.
			clipped_interval = ivl&self.ivl
			if not clipped_interval.is_empty():
				yield self.decoder.prefix(ctx, clipped_interval, params)
				yield self.decoder.decode(ctx, clipped_interval, params)

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
		if self.is_empty():
			self.assign(r)
		else:
			self.assign(Interval.union(self, r))

	def items(self, ctx):
		for r in self.contents:
			yield from r.items(ctx)

	def __str__(self):
		return "{}".format(self.contents)

	def __repr__(self):
		return "CompoundMemRegion({})".format(self.contents)
		
memtype_re = re.compile(r"\s*([^\s]+)\s*([0-9A-Fa-f]{4})\s*([0-9A-Fa-f]{4})\s*^({.*?^})?", re.MULTILINE|re.DOTALL)

# A representation of the MemType.txt file. A collection of 'MemRegion's.
class MemType(object):
	def __init__(self, ctx, fname, default_decoder=None):
		self.map = [] # A list of 'MemRegion's
		if default_decoder:
			self.default_decoder = ctx.decoders[default_decoder]
		else:
			self.default_decoder = None

		txt = None
		if fname:
			with open(fname, "r") as f:
				txt = f.read()

		if txt:
			pos, endpos = 0, len(txt)
			while pos!=endpos:
				m = memtype_re.match(txt, pos, endpos)
				if m is None:
					raise ValueError("Error in memtype file")

				# Poor man's configuration parser
				params = {}
				if m[4]:
					params = eval(m[4], {})

				self.map.append(MemRegion(ctx.decoders[m[1]], m[2], m[3], params))
				pos = m.end()
		else:
			if self.default_decoder is None:
				self.default_decoder = 'data'
			self.map.append(MemRegion(self.default_decoder, ctx.mem_range.first, ctx.mem_range.last, {}))

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

	def preprocess(self, ctx, ivl):
		new_map = []

		def process_hole(self):
			hole = hole_finder.hole()
			if not hole.is_empty():
				# we found a hole and we've got a default decoder
				ctx.holes += 1
				dr = MemRegion(self.default_decoder, hole.first, hole.last, {})
				remains = dr.preprocess(ctx)
				if remains.is_empty():
					dr.is_hole = True
					new_map.append(dr)
				else:
					cr = CompoundMemRegion()
					dr.last = remains.first-1
					cr.add(dr)
					mr = MemRegion(ctx.decoders['data'], remains.first, remains.last, {})
					mr.preprocess(ctx)
					cr.add(mr)
					cr.is_hole = True
					new_map.append(cr)

		hole_finder = HoleFinder(ivl) if self.default_decoder else FakeHoleFinder()

		for region in self.overlapping(ivl):
			hole_finder.feed(region.ivl)

			process_hole(self)

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

		hole_finder.feed()
		process_hole(self)

		self.map = new_map

	def items(self, ctx, ivl):
		hole_idx = 0
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

class FakeHoleFinder(object):
	def __init__(self):
		self.empty = Interval()

	def feed(self, ivl=None):
		pass

	def hole(self):
		return self.empty

class HoleFinder(object):
	def __init__(self, envelope):
		self.empty = Interval()
		self.envelope = envelope
		self.current = None
		self.last = None

	def feed(self, ivl=None):
		if self.current is None:
			self.current = ivl
		else:
			self.last = self.current
			self.current = ivl

	def hole(self):
		if self.current is None:
			if self.last is None:
				# we've been fed no intervals, return the envelope as a hole
				return self.envelope
			else:
				# a hole between the last interval and the envelope
				return Interval(self.last.last+1, self.envelope.last)

		# if we have a hole between the first interval and the envelope
		if self.last is None:
			if self.current.first > self.envelope.first:
				return Interval(self.envelope.first, self.current.first-1)
			else:
				return self.empty

		return Interval(self.last.last+1, self.current.first-1)

if __name__=='__main__':
	hf = HoleFinder(Interval(0, 0x100))
	hf.feed(Interval(0x1, 0xff))
	print(hf.hole())
	hf.feed()
	print(hf.hole())
