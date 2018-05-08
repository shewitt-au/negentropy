import re
import bisect
import multiindex
from interval import Interval

class DictWithRange(multiindex.MultiIndex):
	def __init__(self):
		super().__init__()
		self.add_index(dict, multiindex.dict_indexer, (lambda k: k[0]))
		self.add_index(list, multiindex.sorted_list_indexer, (lambda k: k[0]))

	def items_in_range(self, ivl):
		b = bisect.bisect_left(self.get_index(1), self.get_key_compare(ivl.first, 1))
		e = bisect.bisect_right(self.get_index(1), self.get_key_compare(ivl.last, 1), b)
		for i in range(b, e):
			yield self.get_index(1)[i]

	def keys_in_range(self, ivl):
		for v in self.items_in_range(ivl):
			yield v[0]

	def values_in_range(self, ivl):
		for v in self.items_in_range(ivl):
			yield v[1]

class SymbolTable(multiindex.MultiIndex):
	def __init__(self):
		super().__init__()
		self.add_index(dict, multiindex.dict_indexer, (lambda k: k[0])) # dict keyed on address
		self.add_index(list, multiindex.sorted_list_indexer, (lambda k: k[0])) # list sorted by address
		self.add_index(list, multiindex.sorted_list_indexer, (lambda k: k[1])) # list sorted by name

	def items_in_range(self, ivl):
		b = bisect.bisect_left(self.get_index(1), self.get_key_compare(ivl.first, 1))
		e = bisect.bisect_right(self.get_index(1), self.get_key_compare(ivl.last, 1), b)
		for i in range(b, e):
			yield self.get_index(1)[i]

	def keys_in_range(self, ivl):
		for v in self.items_in_range(ivl):
			yield v[0]

	def values_in_range(self, ivl):
		for v in self.items_in_range(ivl):
			yield v[1]

symbols_re = re.compile(r"al(i)?\s*C:([0-9A-Fa-f]{4})\s*([^\s]*)")

def read_symbols(*fns):
	symbols = SymbolTable()

	for fn in fns:
		with open(fn, "r") as f:
			for line in f:
				if line=="":
					continue
				m = re.match(symbols_re, line)
				if m:
					symbols.add((int(m[2], 16), m[3], m[1]=='i'))

	return symbols

comments_re = re.compile(r"([0-9A-Fa-f]{4})\s*(.*)")

def read_comments(fnname):
	comments = DictWithRange()

	with open(fnname, "r") as f:

		before = ""
		after = ""
		inline = ""
		pos = 0 # before
		addr = -1

		def update_stinggs():
			if line[0:2] == r"\/":
				line = line[2:]
				after += line+"\n"
			elif line[0] == r">":
				line = line[1:]
				inline += line+"\n"
			else:
				before += line+"\n"

		for line in f:
			if line=="":
				continue
			m = re.match(comments_re, line)
			if not m:
				continue
			line = m[2]

			newaddr = int(m[1], 16)

			if addr!=newaddr:
				comments.add((addr, before, after, inline))
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
	comments.add((addr, before, after, inline))

	#TODO: REVISIT THIS - WE CAN'R REMOVE NOW!
	#del comments[-1] # Remove the invalid entry

	return comments
