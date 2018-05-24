import re
import bisect
from heapq import merge
import copy
from interval import Interval, with_holes
import errors 

class Memory(object):
	def __init__(self, data, org=None):
		self.data = data
		if org is None:
			self.ivl = Interval(0x0000, 0x0001)
			org = self.r16(0)
			off = 2
		else:
			off = 0

		self.data = self.data[off:]
		self.ivl = Interval(org, org+len(self.data)-1)

		print("Loaded: {}".format(self.ivl))

	def view(self, ivl):
		if not self.ivl.contains(ivl):
			raise errors.MemoryException("Attempt to map view that's not in range")
		cpy = copy.copy(self)
		cpy.data = self.data[ivl.first-self.ivl.first:]
		cpy.ivl = ivl.copy()
		return cpy

	def _map(self, addr, sz=1):
		rd = Interval(addr, addr+sz-1)
		if not self.ivl.contains(rd):
			raise errors.MemoryException("Address not in range", self.ivl, rd)
		return addr-self.ivl.first

	def r8(self, addr):
		return self.data[self._map(addr)]

	def r8m(self, addr, sz):
		ma = self._map(addr, sz)
		return self.data[ma : ma+sz]

	def r16(self, addr):
		ma = self._map(addr, 2)
		return self.data[ma] + self.data[ma+1]*256

	def r16m(self, addr, sz):
		ma = self._map(addr, sz*2)
		return [self.r16(a) for a in range(ma, ma+sz, 2)]

	def __len__(self):
		return len(self.ivl)

	def range(self):
		return self.ivl

# Represents a region of memory (C64's) and associates it with a specific decoder.
class MemRegion(Interval):
	def __init__(self, decoder, tuple_or_first, last=None, params=None):
		super().__init__(tuple_or_first, last)
		self.decoder = decoder
		self.params = params
		self.is_hole = False

	def preprocess(self, ctx):
		return self.decoder.preprocess(ctx, self)

	def items(self, ctx):
		params = self.params.copy()
		yield self.decoder.prefix(ctx, self, params)
		yield self.decoder.decode(ctx, self, params)

	def __and__(self, other):
		cpy = copy.copy(self)
		ivl = super().__and__(other)
		cpy.first = ivl.first
		cpy.last = ivl.last
		return cpy

	def __str__(self):
		return "{}: ${:04x}-${:04x}".format(self.decoder, self.first, self.last)

	def __repr__(self):
		return "MemRegion({}: ${:04x}-${:04x})".format(self.decoder, self.first, self.last)

class CompoundMemRegion(Interval):
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

	def __and__(self, other):
		cpy = copy.copy(self)
		ivl = super().__and__(other)
		cpy.first = ivl.first
		cpy.last = ivl.last
		return cpy

	def __str__(self):
		return "CompoundMemRegion {}".format(self.contents)

	def __repr__(self):
		return "CompoundMemRegion {}".format(self.contents)
		
memtype_re = re.compile(r"\s*([^\s]+)\s*([0-9A-Fa-f]{4})\s*([0-9A-Fa-f]{4})\s*^({.*?^})?", re.MULTILINE|re.DOTALL)

# A representation of the MemType.txt file. A collection of 'MemRegion's.
class MemType(object):
	def __init__(self, ctx, fname, decoders, default_decoder=None):
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

				self.map.append(MemRegion(decoders[m[1]], m[2], m[3], params))
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

	# Iterates over the overlapping regions clipping the ends if they only
	# partially overlap.
	def overlapping(self, ivl):
		b = bisect.bisect_left(self.map, ivl.first)
		e = bisect.bisect_right(self.map, ivl.last, b)
		for idx in range(b, e):
			yield self[idx]&ivl

	def contains(self, addr):
		i = bisect.bisect_left(self.map, addr)
		return i!=len(self) and self[i]==addr

	def _region_iterator(self, ivl):
		if self.default_decoder:
			return with_holes(ivl, self.overlapping(ivl))
		else:
			return self.overlapping(ivl)

# self.cut_left_iter(merge(ctx.syms.keys_in_range(self), ctx.cmts.keys_in_range(self)))

	def preprocess(self, ctx, ivl):
		new_map = []

		for rgntocut in self._region_iterator(ivl):
			for region in rgntocut.cut_left_iter(merge(ctx.syms.keys_in_range(rgntocut), ctx.cmts.keys_in_range(rgntocut))):
				try:
					pp = region.preprocess
				except AttributeError:
					# we found a hole and we've got a default decoder
					ctx.holes += 1
					dr = MemRegion(self.default_decoder, region.first, region.last, {})
					remains = dr.preprocess(ctx)
					if remains.is_empty():
						new_map.append(dr)
					else:
						cr = CompoundMemRegion()
						dr.last = remains.first-1
						cr.add(dr)
						cr.add(MemRegion(ctx.decoders['data'], remains.first, remains.last, {}))
						cr.is_hole = True
						new_map.append(cr)
				else:
					remains = pp(ctx)
					print(region)
					print(remains)
					if not remains.is_empty():
						region.last = remains.first-1
						new_map.append(region)
						new_map.append(MemRegion(ctx.decoders['data'], remains.first, remains.last, {}))
					else:
						new_map.append(region)

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
