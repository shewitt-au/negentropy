# A python dictionary clone that supports multiple values with the same key.
# We delegate rather than subclass so any missing/new methods won't be inherited
# (with the wrong semantics).

class multidict(object):
	def __init__(self):
		self._dict = {1: ["one", "One"], 2: ["two", "Two"], 3: ["three", "Three"]}
		self._len = 0
		self._sel = 0

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


if __name__=='__main__':
	m = multidict()
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

	print(m)
