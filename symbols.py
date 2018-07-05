import re
import bisect
import multiindex
from interval import Interval

class DictWithRange(multiindex.MultiIndex):
	def __init__(self):
		super().__init__()
		self.add_index("by_address", dict, multiindex.dict_indexer, (lambda k: k[0]))
		self.add_index("sorted_address", list, multiindex.sorted_list_indexer, (lambda k: k[0]))

	def items_in_range(self, ivl):
		b = bisect.bisect_left(self.sorted_address, self.sorted_address_compare(ivl.first))
		e = bisect.bisect_right(self.sorted_address, self.sorted_address_compare(ivl.last), b)
		for i in range(b, e):
			yield self.sorted_address[i]

	def keys_in_range(self, ivl):
		for v in self.items_in_range(ivl):
			yield v[0]

	def values_in_range(self, ivl):
		for v in self.items_in_range(ivl):
			yield v[1]

class SymbolTable(multiindex.MultiIndex):
	def __init__(self):
		super().__init__()
		self.add_index("sorted_address", list, multiindex.sorted_list_indexer, (lambda k: k[0])) # list sorted by address
		self.add_index("sorted_name", list, multiindex.sorted_list_indexer, (lambda k: k[1])) # list sorted by name
		self.black_list = None

	def parse_add(self, ctx, ivl, name, in_index):
		ctx.have_indexables |= in_index
		self.add((ivl, name, in_index))

	def items_in_range(self, ivl):
		b = bisect.bisect_left(self.sorted_address, self.sorted_address_compare(ivl.first))
		e = bisect.bisect_right(self.sorted_address, self.sorted_address_compare(ivl.last), b)
		for i in range(b, e):
			yield self.sorted_address[i]

	def left_edges(self, ivl):
		for v in self.items_in_range(ivl):
			yield v[0].first

	def values_in_range(self, ivl):
		for v in self.items_in_range(ivl):
			yield v[1]

	def get_entry(self, addr):
		i = bisect.bisect_left(self.sorted_address, self.sorted_address_compare(addr))
		if i==len(self.sorted_address):
			return None
		ent = self.sorted_address[i]
		if not ent[0].contains(addr) or (self.black_list is not None and addr in self.black_list):
			return None
		return ent

	def lookup(self, addr):
		e = self.get_entry(addr)
		if e is None:
			return None
		return e[1]

	def name(self, addr):
		n = self.lookup(addr)
		if n is None:
			return "${:04x}".format(addr)
		return n
