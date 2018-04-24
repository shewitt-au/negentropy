import numbers

class Interval(object):
	def __init__(self, tuple_or_first=None, last=None):
		if tuple_or_first is None:
			# an empty interval
			self.first = 1
			self.last = 0
		elif last is None:
			self.value = tuple_or_first
		else:
			if isinstance(tuple_or_first, str):
				self.first = int(tuple_or_first, 16)
			else:
				self.first = tuple_or_first
			if isinstance(last, str):
				self.last = int(last, 16)
			else:
				self.last = last

	def _get(self):
		return (self.first, self.last)
	def _set(self, ivl):
		self.first = ivl[0]
		self.last = ivl[1]
	value = property(_get, _set)

	def is_empty(self):
		return self.first>self.last

	def __len__(self):
		if self.is_empty():
			return 0
		else:
			return self.last-self.first-1

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

	# Intersection
	def __and__(self, other):
		if self.is_empty() or other.is_empty():
			return Interval()
		else:
			return Interval(max(self.first, other.first), min(self.last, other.last))

	def cut_left(self, pos):
		return (Interval(self.first, min(pos-1, self.last)), Interval(max(pos, self.first), self.last))

	def cut_left_iter(self, cuts):
		l = self
		r = Interval()

		for p in cuts:
			l , r = l.cut_left(p)
			if l.is_empty():
				l = r
				continue
			yield l
			l = r
		if not r.is_empty():
			yield r

	def cut_right(self, pos):
		return (Interval(self.first, min(pos, self.last)), Interval(max(pos+1, self.first), self.last))

	def cut_right_iter(self, cuts):
		l = self
		r = Interval()

		for p in cuts:
			l , r = l.cut_right(p)
			if l.is_empty():
				l = r
				continue
			yield l
			l = r
		if not r.is_empty():
			yield r

	def __len__(self):
		if self.is_empty():
			return 0
		return self.last-self.first+1
