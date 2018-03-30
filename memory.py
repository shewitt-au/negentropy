import re
import bisect
import decoders
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

memtype_re = re.compile(r"^\s*([^\s]+)\s*([0-9A-Fa-f]{4})\s*([0-9A-Fa-f]{4})\s*$")

class MemType(object):
	def __init__(self, fname):
		self.map = []
		with open(fname, "r") as f:
			for line in enumerate(f):
				m = re.match(memtype_re, line[1])
				if m is None:
					print("Error in line {} of memtype file".format(line[0]+1))
					raise ValueError("Error in memtype file")
				self.map.append(MemRegion(decoders.decoders[m[1]], m[2], m[3]))
		self.map.sort()

	def __len__(self):
		return len(self.map)

	def __getitem__(self, key):
		return self.map[key]

	def overlapping_indices(self, ivl):
		b = bisect.bisect_left(self.map, ivl.first)
		e = bisect.bisect_right(self.map, ivl.last, b)
		return range(b, e)

	def decode(self, ctx, ivl):
		for i in self.overlapping_indices(ivl):
			yield from self[i].decode(ctx, self[i]&ivl)

class MemRegion(interval.Interval):
	def __init__(self, decoder, tuple_or_first, last=None):
		super().__init__(tuple_or_first, last)
		self.decoder = decoder

	def decode(self, ctx, ivl):
		return self.decoder(ctx, ivl)

	def __str__(self):
		return "{}: ${:04x}-${:04x}".format(self.decoder, self.first, self.last)

	def __repr__(self):
		return "MemRegion({}: ${:04x}-${:04x})".format(self.decoder, self.first, self.last)

if __name__ == '__main__':
	import symbols
	import memory
	sym = symbols.read_symbols("BD.txt", "BD-BM.txt")
	cmt = symbols.read_comments()
	with open("5000-8fff.bin", "rb") as f:
		f = open("5000-8fff.bin", "rb")
		m = memory.Memory(f.read(), 0x5000)
	decoders.init_decoders(m, sym, cmt)
	mmap = MemType("MemType.txt")

#	ivl = interval.Interval(0x72e1, 0x7302)
#	for v in sym.keys_in_range(ivl):
#		print(v)
#	for v in sym.values_in_range(ivl):
#		print(v)
#	for v in sym.items_in_range(ivl):
#		print(v)

#	print()

	# code	6c80 6da4
	# data	6da5 6db3
	# code	6db4 6e4e
	ivl2 = interval.Interval(0x8317, 0x838d-1)
	mmap.decode(ivl2)
