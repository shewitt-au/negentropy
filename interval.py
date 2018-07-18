import numbers
import copy
import itertools

def parse_number(s):
	s = s.strip()
	if s[0]=='$':
		return int(s[1:], 16)
	else:
		return int(s)

class Interval(object):
	def __init__(self, first=None, last=None, size=1):
		if first is None:
			self.first = 1
			self.last = 0
		else:
			if last is None:
				self.first = first
				self.last = first+size-1
			else:
				self.first = first
				self.last = last

	# Make an Interval from near anything
	@classmethod
	def conjure(cls, first=None, last=None, size=1):
		if isinstance(first, str):
			parts = first.split('-')
			if len(parts)!=1:
				return cls(parse_number(parts[0]), parse_number(parts[1]))
			first = parse_number(first)
		if isinstance(last, str):
			last = parse_number(last)
		return cls(first, last, size)

	def copy(self):
		return copy.copy(self)

	def assign(self, other):
		self.first = other.first
		self.last = other.last

	def is_empty(self):
		return self.first>self.last

	def is_singular(self):
		return not self.is_empty() and self.first==self.last

	def __iter__(self):
		for v in range(self.first, self.last+1):
			yield v

	def __len__(self):
		if self.is_empty():
			return 0
		else:
			return self.last-self.first+1

	def __eq__(self, other):
		if isinstance(other, __class__):
			return self.first==other.first and self.last==other.last
		elif isinstance(other, numbers.Number):
			return other>=self.first and other<=self.last
		else:
			return NotImplemented

	def __ne__(self, other):
		if isinstance(other, __class__):
			return self.first!=other.first or self.last!=other.last
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

	def __hash__(self):
		return hash((self.first, self.last))

	def __str__(self):
		if self.is_empty():
			return "{Empty}"
		elif self.is_singular():
			return "${:04x}".format(self.first)
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
	def inner_complement(cls, left, right):
		if cls.exclusive_left(left, right):
			return cls(left.last+1, right.first-1)
		elif cls.exclusive_left(right, left):
			return cls(right.last+1, left.first-1)
		else:
			return cls()

	# checks if two intervals are adjacent or overlapping
	@classmethod
	def friendly(cls, left, right):
		return cls.inner_complement(left, right).is_empty()

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

	@classmethod
	def envelope(cls, first, second):
		if first.is_empty():
			return second
		elif second.is_empty():
			return first
		else:
			return cls(min(first.first, second.first), max(first.last, second.last))

	def cut_left(self, pos):
		return (
			Interval(self.first, min(pos-1, self.last)),
			Interval(max(pos, self.first), self.last)
			)

	def cut_left_iter(self, cuts):
		l = self
		r = Interval()
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
			Interval(self.first, min(pos, self.last)),
			Interval(max(pos+1, self.first), self.last)
			)

	def cut_right_iter(self, cuts):
		l = self
		r = Interval()
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
