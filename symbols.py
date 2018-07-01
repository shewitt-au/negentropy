import re
import bisect
import multiindex

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
		self.add_index("by_address", dict, multiindex.dict_indexer, (lambda k: k[0])) # dict keyed on address
		self.add_index("sorted_address", list, multiindex.sorted_list_indexer, (lambda k: k[0])) # list sorted by address
		self.add_index("sorted_name", list, multiindex.sorted_list_indexer, (lambda k: k[1])) # list sorted by name

	def parse_begin(self, ctx):
		pass

	def parse_add(self, ctx, addr, name, in_index):
		ctx.have_indexables |= in_index
		self.add((addr, name, in_index))

	def parse_end(self, ctx):
		pass

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

	def lookup(self, addr):
		return self.by_address.get(addr)

	def format(self, addr):
		s = self.by_address.get(addr)
		return "{:04x}".format(addr) if s is None else s[1]
