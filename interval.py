import numbers

class Interval(object):
	def __init__(self, tuple_or_first, last=None):
		if last is None:
			self.value = tuple_or_first
		else:
			if isinstance(tuple_or_first, str):
				self.first = int(tuple_or_first, 16)
				self.last = int(last, 16)
			else:
				self.first = tuple_or_first
				self.last = last
		assert self.first<=self.last, "Interval: first > last"

	def _get(self):
		return (self.first, self.last)

	def _set(self, ivl):
		self.first = ivl[0]
		self.last = ivl[1]
		assert self.first<=self.last, "Interval: first > last"

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
		return "${:04x}-${:04x}".format(self.first, self.last)

	def __repr__(self):
		return "Interval(${:04x}-${:04x})".format(self.first, self.last)

	value = property(_get, _set)
