import re
import bisect
from heapq import merge
import copy
from interval import Interval, with_holes

class Memory(object):
	def __init__(self, data, org):
		self.data = data
		self.org = org

	def r8(self, addr):
		return self.data[addr-self.org]

	def r8m(self, addr, sz):
		return self.data[addr-self.org : addr-self.org+sz]

	def r16(self, addr):
		return self.data[addr-self.org] + self.data[addr-self.org+1]*256

	def r16m(self, addr, sz):
		return [self.r16(a) for a in range(addr, addr+sz, 2)]

# Represents a region of memory (C64's) and associates it with a specific decoder.
class MemRegion(Interval):
	def __init__(self, decoder, tuple_or_first, last=None, params=None):
		super().__init__(tuple_or_first, last)
		self.decoder = decoder
		self.params = params

	def links(self, ctx, ivl=None):
		ptn = self if (ivl is None) else ivl
		for i in ptn.cut_left_iter(merge(ctx.syms.keys_in_range(ptn), ctx.cmts.keys_in_range(ptn))):
			self.decoder.links(ctx, i)

	def items(self, ctx, ivl=None):
		ptn = self if (ivl is None) else ivl
		params = self.params.copy()
		for i in ptn.cut_left_iter(merge(ctx.syms.keys_in_range(ptn), ctx.cmts.keys_in_range(ptn))):
			yield self.decoder.prefix(ctx, i, params)
			yield self.decoder.decode(ctx, i, params)

	def __and__(self, other):
		cpy = copy.copy(self)
		ivl = super().__and__(other)
		cpy.first = ivl.first
		cpy.lasr = ivl.last
		return cpy

	def __str__(self):
		return "{}: ${:04x}-${:04x}".format(self.decoder, self.first, self.last)

	def __repr__(self):
		return "MemRegion({}: {:04x}-${:04x})".format(self.decoder, self.first, self.last)

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
					print("Error in line {} of memtype file".format(line[0]+1))
					raise ValueError("Error in memtype file")

				# Poor man's configuration parser
				params = {}
				if m[4]:
					params = eval(m[4], {})

				self.map.append(MemRegion(decoders[m[1]], m[2], m[3], params))
				pos = m.end()
		else:
			self.map.append(MemRegion(decoders[default_decoder], 0x0000, 0xffff, {}))

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
			return with_holes(self.overlapping(ivl))
		else:
			return self.overlapping(ivl)

	def _links(self, ctx, ivl):
		for region in self._region_iterator(ivl):
			try:
				region.links(ctx)
			except AttributeError:
				# we found a hole and we've got a default decoder
				dr = MemRegion(self.default_decoder, region.first, region.last, {})
				dr.links(ctx)

	def items(self, ctx, ivl):
		self._links(ctx, ivl)
		gen = self._region_iterator(ivl)
		for region in gen:
			try:
				yield from region.items(ctx)
			except AttributeError:
				# we found a hole and we've got a default decoder
				yield {
					'type': "hole",
					'contents': gen
					}
				dr = MemRegion(self.default_decoder, region.first, region.last, {})
				yield from dr.items(ctx)
