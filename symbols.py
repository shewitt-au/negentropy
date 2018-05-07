import re
import bisect
from interval import Interval

class DictWithRange(dict):
	def build_index(self):
		self.inorder = sorted(self.items(), key=(lambda t: t[0]))

	def items_in_range(self, ivl):
		# Class needed because bisect doesn't support key extractors
		class TupleKey(object):
			def __init__(self, key):
				self.key = key
			def __eq__(self, other):
				return self.key == other[0]
			def __ne__(self, other):
				return self.key != other[0]
			def __lt__(self, other):
				return self.key < other[0]
			def __le__(self, other):
				return self.key <= other[0]
			def __gt__(self, other):
				return self.key > other[0]
			def __ge__(self, other):
				return self.key >= other[0]

		b = bisect.bisect_left(self.inorder, TupleKey(ivl.first))
		e = bisect.bisect_right(self.inorder, TupleKey(ivl.last), b)
		for i in range(b, e):
			yield self.inorder[i]

	def keys_in_range(self, ivl):
		for v in self.items_in_range(ivl):
			yield v[0]

	def values_in_range(self, ivl):
		for v in self.items_in_range(ivl):
			yield v[1]

symbols_re = re.compile(r"ali?\s*C:([0-9A-Fa-f]{4})\s*([^\s]*)")

def read_symbols(*fns):
	symbols = DictWithRange()

	for fn in fns:
		with open(fn, "r") as f:
			for line in f:
				if line=="":
					continue
				m = re.match(symbols_re, line)
				if m:
					symbols[int(m[1], 16)] = m[2]

		symbols.build_index()

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
				comments[addr] = (before, after, inline)
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
	comments[addr] = (before, after, inline)

	del comments[-1] # Remove the invalid entry

	comments.build_index()

	return comments
