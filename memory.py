import errors
from interval import Interval
import copy

class Bytes16(bytes):
	def __len__(self):
		return super().__len__()//2

	def __getitem__(self, idx):
		if isinstance(idx, slice):
			stop = None if idx.stop is None else idx.stop*2
			step = None if idx.step is None else idx.step*2
			return Bytes16(super().__getitem__(slice(idx.start*2, stop, step)))
		else:
			return super().__getitem__(idx)+super().__getitem__(idx+1)*256

	class Bytes16Iter(object):
		def __init__(self, itr):
			self.itr = itr

		def __next__(self):
			l = next(self.itr)
			h = next(self.itr)
			return l+h*256

	def __iter__(self):
		return Bytes16.Bytes16Iter(super().__iter__())

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
		self.ivl = Interval(org, size=len(self.data))

		print("Loaded: {}".format(self.ivl))

	def view(self, ivl):
		if not self.ivl.contains(ivl):
			raise errors.MemoryException("Attempt to map view that's not in range")
		cpy = copy.copy(self)
		cpy.data = self.data[ivl.first-self.ivl.first:]
		cpy.ivl = ivl.copy()
		return cpy

	def _map(self, addr, sz=1):
		rd = Interval(addr, size=sz)
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
		return Bytes16(self.data[ma: ma+sz*2])

	def __len__(self):
		return len(self.ivl)

	def range(self):
		return self.ivl
