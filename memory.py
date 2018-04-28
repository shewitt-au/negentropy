import re
import bisect
import interval

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
class MemRegion(interval.Interval):
	def __init__(self, decoder, tuple_or_first, last=None, params=None):
		super().__init__(tuple_or_first, last)
		self.decoder = decoder
		self.params = params

	def decode(self, ctx, ivl):
		return self.decoder.decode(ctx, ivl, self.params)

	def __str__(self):
		return "{}: ${:04x}-${:04x}".format(self.decoder, self.first, self.last)

	def __repr__(self):
		return "MemRegion({}: ${:04x}-${:04x})".format(self.decoder, self.first, self.last)

memtype_re = re.compile(r"\s*([^\s]+)\s*([0-9A-Fa-f]{4})\s*([0-9A-Fa-f]{4})\s*^({.*?^})?", re.MULTILINE|re.DOTALL)

# A representation of the MemType.txt file. A collection of 'MemRegion's.
class MemType(object):
	def __init__(self, fname, decoders):
		self.map = [] # A list of 'MemRegion's

		with open(fname, "r") as f:
			txt = f.read()

		pos, endpos = 0, len(txt)
		while pos!=endpos:
			m = memtype_re.match(txt, pos, endpos)
			if m is None:
				print("Error in line {} of memtype file".format(line[0]+1))
				raise ValueError("Error in memtype file")

			# Poor man's configuration parser
			params = {}
			if m[4]:
				params = eval(m[4],{})

			self.map.append(MemRegion(decoders[m[1]], m[2], m[3], params))
			pos = m.end()

		# Sort so adjacent ranges are next to each other. See 'overlapping_indices'.
		self.map.sort()

	def __len__(self):
		return len(self.map)

	def __getitem__(self, key):
		return self.map[key]

	# Get the range of indices that overlap the provided interval
	def overlapping_indices(self, ivl):
		b = bisect.bisect_left(self.map, ivl.first)
		e = bisect.bisect_right(self.map, ivl.last, b)
		return range(b, e)

	def decode(self, ctx, ivl):
		for i in self.overlapping_indices(ivl):
			yield from self[i].decode(ctx, self[i]&ivl)
