# A python dictionary clone that supports multiple values with the same key.
# We delegate rather than subclass so any missing/new methods won't be inherited
# (with the wrong semantics).

import copy

class multidict(object):
	def __init__(self, d=None):
		self._sel = 0
		if d is None:
			self._dict = {}
			self._len = 0
		elif isinstance(d, dict):
			# Allow initialisation from a regular dict 
			self._dict = d
			self._calclen()
		else:
			raise ValueError # TODO: match dict behaviour

	def clear(self):
		self._dict.clear()

	def copy(self):
		return copy.copy(self)

	@classmethod
	def fromkeys(cls, seq, value=None):
		md = cls()
		for v in seq:
			md[v] = value
		return md

	def get(self, key, default=None):
		items = self._dict.get(key)
		if items is None:
			return default
		else:
			return items[self._sel]

	def _calclen(self):
		self._len = 0
		for v in self._dict.values():
			self._len += len(v)

	def __len__(self):
		return self._len

	def __getitem__(self, key):
		try:
			items = self._dict[key]
		except KeyError:
			return self.__missing__(key)
		else:
			return items[self._sel]

	def __missing__(self, key):
		raise KeyError(key)

	def __setitem__(self, key, value):
		self._dict.setdefault(key, []).append(value)
		self._len += 1

	def __delitem__(self, key):
		#TODO: is this the behaviour we want?
		items = self._dict[key]
		if len(items)==1:
			del self._dict[key]
		else:
			del items[self._sel]
		self._len -= 1

	def __iter__(self):
		return iter(self._dict)

	def __reversed__(self):
		raise TypeError("'multidict' object is not reversible")

	def __contains__(self, key):
		return key in self._dict

	def __str__(self):
		return str(self._dict)

	def __repr__(self):
		return repr(self._dict)

	def __format__(self, format_spec):
		return self.dict.__format__(format_spec)

	def __eq__(self, other):
		return self._dict==other

	def __ne__(self, other):
		return self._dict!=other

if __name__=='__main__':
	a = {1: ["one", "One"], 2: ["two", "Two"], 3: ["three", "Three"]}
	m = multidict(a)
	print(len(m))
	print(m[1])
	try:
		print(m[0])
	except KeyError as e:
		print("Expected: {}".format(e))

	print(len(m))
	m[0] = "zero"
	print(len(m))
	m[0] = "Zero"
	print(len(m))
	print(m._dict)

	del m[0]
	print(len(m))
	print(m._dict)
	del m[0]
	print(len(m))
	print(m._dict)
	try:
		del m[0]
	except KeyError as e:
		print("Expected: {}".format(e))
	print(len(m))
	print(m._dict)

	print([v for v in iter(m)])

	try:
		print([v for v in reversed(m)])
	except TypeError as e:
		print("Expected: {}".format(e))

	print(1 in m)
	print(0 in m)

	print(str(m))
	print(repr(m))

	print("fmt: {}".format(a))

	d1 = multidict({1: "one"})
	d2 = multidict({2: "two"})
	print(d1!=d2)

	print(dir(m))

	print(multidict.fromkeys([1, 2, 3], "who knows?"))

	print(m.get(1))
	print(m.get(7))
	print(m.get(7, "seven"))
