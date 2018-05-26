import errors
from interval import Interval
import copy

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
