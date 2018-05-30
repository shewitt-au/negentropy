import numbers
import copy
import itertools

class Interval(object):
	# Interval(): an empty Interval
	# Interval((f, l)): an Interval from f to l (inclusive)
	# Interval(f, l): an Interval from f to l (inclusive)
	def __init__(self, first=None, last=None, size=None):
		if isinstance(first, str):
			first = int(first, 16)
		if isinstance(last, str):
			last = int(last, 16)

		if size is not None:
			last = first+size-1

		if first is None and last is None:
			# an empty interval
			self.first = 1
			self.last = 0
		elif last is None:
			if isinstance(first, tuple):
				self.first = first[0]
				self.last = first[1]
			else:
				self.first = first
				self.last = first
		else:
			self.first = first
			self.last = last

	def copy(self):
		return copy.copy(self)

	# useful when Interval is used as a base class (to alter the Interval part but keep the rest)
	def copy_and_assign(self, ivl):
		cp = self.copy()
		cp.assign(ivl)
		return cp

	def assign(self, other):
		self.first = other.first
		self.last = other.last

	def _get(self):
		return (self.first, self.last)
	def _set(self, ivl):
		self.first = ivl[0]
		self.last = ivl[1]
	value = property(_get, _set)

	def is_empty(self):
		return self.first>self.last

	def __iter__(self):
		for v in range(self.first, self.last):
			yield v

	def __len__(self):
		if self.is_empty():
			return 0
		else:
			return self.last-self.first+1

	def __eq__(self, other):
		if isinstance(other, __class__):
			return self.value == other.value
		elif isinstance(other, numbers.Number):
			return other>=self.first and other<=self.last
		else:
			return NotImplemented

	def __ne__(self, other):
		if isinstance(other, __class__):
			return self.value != other.value
		elif isinstance(other, numbers.Number):
			return other<self.first or other>self.last
		else:
			return NotImplemented

	def __lt__(self, other):
		if isinstance(other, __class__):
			return (self.first<other.first) or (self.first==other.first and self.last<other.last)
		elif isinstance(other, numbers.Number):
			return self.last<other
		else:
			return NotImplemented

	def __le__(self, other):
		if isinstance(other, __class__):
			return (self.first<other.first) or (self.first==other.first and self.last<=other.last)
		elif isinstance(other, numbers.Number):
			return self.last<other or (other>=self.first and other<=self.last)
		else:
			return NotImplemented

	def __gt__(self, other):
		if isinstance(other, __class__):
			return (self.first>other.first) or (self.first==other.first and self.last>other.last)
		elif isinstance(other, numbers.Number):
			return self.first>other
		else:
			return NotImplemented

	def __ge__(self, other):
		if isinstance(other, __class__):
			return (self.first>other.first) or (self.first==other.first and self.last>=other.last)
		elif isinstance(other, numbers.Number):
			return self.first>other or (other>=self.first and other<=self.last)
		else:
			return NotImplemented

	def __str__(self):
		if self.is_empty():
			return "{Empty}"
		else:
			return "${:04x}-${:04x}".format(self.first, self.last)

	def __repr__(self):
		return "Interval({})".format(str(self))

	def __and__(self, other):
		if self.is_empty() or other.is_empty():
			return Interval()
		else:
			return Interval(max(self.first, other.first), min(self.last, other.last))

	@staticmethod
	def exclusive_left(left, right):
		return left.last<right.first

	def contains(self, other):
		if isinstance(other, __class__):
			return other.first>=self.first and other.last<=self.last
		else:
			return other>=self.first and other<=self.last

	@classmethod
	def inner_comlement(cls, left, right):
		if cls.exclusive_left(left, right):
			return cls(left.last+1, right.first-1)
		elif cls.exclusive_left(right, left):
			return cls(right.last+1, left.first-1)
		else:
			return cls()

	# checks if two intervals are adjacent or overlapping
	@classmethod
	def friendly(cls, left, right):
		return cls.inner_comlement(left, right).is_empty()

	@classmethod
	def disjoint(cls, left, right):
		return cls.exclusive_left(left, right) or cls.exclusive_left(right, left)

	@classmethod
	def union(cls, first, second):
		if first.is_empty():
			return second
		elif second.is_empty():
			return first
		else:
			assert cls.friendly(first, second), "Can't make a union of separated intervals"
			return cls(min(first.first, second.first), max(first.last, second.last))

	def cut_left(self, pos):
		return (
			self.copy_and_assign(Interval(self.first, min(pos-1, self.last))),
			self.copy_and_assign(Interval(max(pos, self.first), self.last))
			)

	def cut_left_iter(self, cuts):
		l = self
		r = self.copy_and_assign(Interval())
		it = iter(cuts)

		try:
			first = next(it)
		except StopIteration:
			yield self
		else:
			for p in itertools.chain([first], it):
				l , r = l.cut_left(p)
				if l.is_empty():
					l = r
					continue
				yield l
				l = r
			if not r.is_empty():
				yield r

	def cut_right(self, pos):
		return (
			self.copy_and_assign(Interval(self.first, min(pos, self.last))),
			self.copy_and_assign(Interval(max(pos+1, self.first), self.last))
			)

	def cut_right_iter(self, cuts):
		l = self
		r = self.copy_and_assign(Interval())
		it = iter(cuts)

		try:
			first = next(it)
		except StopIteration:
			yield self
		else:
			for p in itertools.chain([first], it):
				l , r = l.cut_right(p)
				if l.is_empty():
					l = r
					continue
				yield l
				l = r
			if not r.is_empty():
				yield r


def nop_hole_decorator(ivl, is_hole):
	return ivl

def hole_decorator(ivl, is_hole):
	cpy = copy.copy(ivl)
	cpy.is_hole = is_hole
	return cpy

def with_holes(envelope, coll, decorator=nop_hole_decorator):
	it = iter(coll)
	try:
		first = next(coll)
	except StopIteration:
		# if the interval collection is empty return the envelope as a hole
		yield decorator(envelope, True)
	else:
		assert envelope.contains(first), "'envelope' must contains all items in 'coll'"
		if first.first > envelope.first:
			# we have a hole before the contents of 'coll'
			yield decorator(Interval(envelope.first, first.first-1), True)

		last = first
		for n in it:
			assert envelope.contains(n), "'envelope' must contains all items in 'coll'"
			yield decorator(last, False)

			hole = Interval(last.last+1, n.first-1)
			if not hole.is_empty():
				yield decorator(hole, True)

			last = n
	
		yield decorator(last, False)

		if last.last < envelope.last:
			# we have a hole after the contents of 'coll'
			yield decorator(Interval(last.last+1, envelope.last), True)
