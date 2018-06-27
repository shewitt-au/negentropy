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

	def parse_add(self, addr, name, in_index):
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

comments_re = re.compile(r"([0-9A-Fa-f]{4})\s*(.*)")

def read_comments(fname):
	comments = DictWithRange()
	inline_comments = DictWithRange()

	if not fname is None:
		with open(fname, "r") as f:
			before = ""
			after = ""
			inline = ""
			pos = 0 # before
			addr = -1

			for line in f:
				if line=="":
					continue
				m = re.match(comments_re, line)
				if not m:
					continue
				line = m[2]

				newaddr = int(m[1], 16)

				if addr!=newaddr:
					if before or after:
						comments.add((addr, before, after))
					if inline:
						inline = inline.rstrip()
						inline_comments.add((addr, inline))
					pos = 0 # before
					before = after = inline = ""

				if not line=="":
					if line[0:2] == r"\/":
						pos = 1 # after
						line = line[2:]
					elif line[0] == r";":
						pos = 2 # inline
						line = line[1:]
				if pos==0:
					before += line+"\n"
				elif pos==1:
					after += line+"\n"
				elif pos==2:
					inline += line+"\n"

				addr = newaddr

		# Add the last one
		if before or after:
			comments.add((addr, before, after))
		if inline:
			inline = inline.rstrip()
			inline_comments.add((addr, inline))

		#TODO: REVISIT THIS - WE CAN'T REMOVE NOW!
		#del comments[-1] # Remove the invalid entry

	return (comments, inline_comments)
