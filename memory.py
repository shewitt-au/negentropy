import re
import bisect
import decoders

class Memory(object):
	def __init__(self, data, org):
		self.data = data
		self.org = org

	def r(self, addr, sz):
		return self.data[addr-self.org : addr-self.org+sz]

	def r8(self, addr):
		return self.data[addr-self.org]

	def r16(self, addr):
		return self.data[addr-self.org] + self.data[addr-self.org+1]*256

memtype_re = re.compile(r"^\s*([^\s]+)\s*([0-9A-Fa-f]{4})\s*([0-9A-Fa-f]{4})\s*$")

class MemType(object):
	def __init__(self, fname):
		self.ivl = None
		self.map = []
		with open(fname, "r") as f:
			for line in enumerate(f):
				m = re.match(memtype_re, line[1])
				if m is None:
					print("Error in line {} of memtype file".format(line[0]+1))
					raise ValueError("Error in memtype file")
				self.map.append(Interval(decoders.decoders[m[1]], m[2], m[3]))
		self.map.sort()

	def __len__(self):
		return len(self.map)

	def __getitem__(self, key):
		return self.map[key]

	def decode(self, addr):
		if self.ivl is None or self.ivl != addr:
			index = bisect.bisect_left(self.map, addr)
			if index==len(self.map) or self.map[index]!=addr:
				ValueError("Address not in memtype file")
			self.ivl = self.map[index]

		return self.ivl.decode(addr)

class Interval(object):
	def __init__(self, decoder, ivl):
		self.decoder = decoder
		self.value = ivl

	def __init__(self, decoder, first, last):
		self.decoder = decoder
		self.first = int(first, 16)
		self.last = int(last, 16)
		assert self.first<=self.last, "Interval: first > last"

	def decode(self, addr):
		return self.decoder.decode(addr)

	def _get(self):
		return (self.first, self.last)

	def _set(self, ivl):
		self.first = ivl[0]
		self.last = ivl[1]
		assert self.first<=self.last, "Interval: first > last"

	def __eq__(self, other):
		if isinstance(other, __class__):
			return self.value == other.value
		else:
			return other>=self.first and other<=self.last

	def __ne__(self, other):
		if isinstance(other, __class__):
			return self.value != other.value
		else:
			return other<self.first or other>self.last

	def __lt__(self, other):
		if isinstance(other, __class__):
			return (self.first<other.first) or (self.first==other.first and self.last<other.last)
		else:
			return self.last<other

	# There is no __rlt__
	def __gt__(self, other):
		if isinstance(other, __class__):
			return (self.first>other.first) or (self.first==other.first and self.last>other.last)
		else:
			return self.first>other

	def __str__(self):
		return "{}: ${:04x}-${:04x}".format(self.decoder, self.first, self.last)

	def __repr__(self):
		return "Interval({}: ${:04x}-${:04x})".format(self.decoder, self.first, self.last)

	value = property(_get, _set)
