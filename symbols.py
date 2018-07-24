import bisect

import multiindex
from interval import Interval
from multidict import multidict

class DictWithRange(multiindex.MultiIndex):
	def __init__(self):
		super().__init__()
		self.add_index("by_address", multidict, multiindex.dict_indexer, (lambda k: k[0]))
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

class CommentInfo(object):
	def __init__(self, before=None, after=None):
		self.before = before
		self.after = after

	def __repr__(self):
		return "CommentInfo(before='{}', after='{}')".format(self.before, self.after)

class Comments(object):
	def __init__(self):
		self.main = DictWithRange()
		self.inline = DictWithRange()

	def get(self, addr):
		ent = self.main.by_address.get(addr)
		return ent[1] if ent is not None else None

	def get_inline(self, addr):
		return self.inline.by_address.get(addr)

	def add_before(self, addr, txt):
		cmt = self.main.by_address.get(addr)
		if cmt is None:
			self.main.add((addr, CommentInfo(before=txt)))
		else:
			cmt[1].before = txt

	def add_after(self, addr, txt):
		cmt = self.main.by_address.get(addr)
		if cmt is None:
			self.main.add((addr, CommentInfo(after=txt)))
		else:
			cmt[1].after = txt

	def add_inline(self, addr, txt):
		cmt = self.inline.by_address.get(addr)
		if cmt is None:
			self.inline.add((addr, txt))
		else:
			cmt = (addr, txt)

	def cuts(self, ivl):
		return self.main.keys_in_range(ivl)

class SymInfo(object):
	def __init__(self, name, addr, op_adjust):
		self.name = name
		self.addr = addr
		self.op_adjust = op_adjust

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

	def lookup(self, addr, name_unknowns=True):
		e = self.get_entry(addr)
		if e is None:
			return SymInfo("${:04x}".format(addr) if name_unknowns else None, addr, "")
		offset = addr-e[0].first
		if offset!=0:
			op_adjust = '+${:x}'.format(offset) if offset>=9 else '+{}'.format(offset)
		else:
			op_adjust = ''
		return SymInfo(e[1], e[0].first, op_adjust)

	def clashes(self):
		clashes = 0
		it = iter(self.sorted_address)
		try:
			ps = next(it)
		except StopIteration:
			pass
		else:
			for s in it:
				if not (ps[0]&s[0]).is_empty():
					print("Symbol clash:\n\t{} @ {}\n\t{} @ {}".format(ps[1], ps[0], s[1], s[0]))
					clashes += 1
					if clashes==7:
						print("***Stopping clash search***\n")
						break
				ps = s

		return clashes!=0
