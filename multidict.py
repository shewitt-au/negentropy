# A python dictionary clone that supports multiple values with the same key.
# It is implemented in terms of a Python dictionary with lists as the values.
# We delegate rather than subclass so any missing/new methods won't be inherited
# (with the wrong semantics).

import copy

class multidict_items(object):
	def __init__(self, md):
		self._md = md

	def __len__(self):
		return self._md._len

	def __iter__(self):
		for ki in self._md._dict.items():
			for vi in ki[1]:
				yield (ki[0], vi)

	def __contains__(self, item):
		return item in iter(self)

	def isdisjoint(self, other):
		for v in other:
			if v in self:
				return False
		return True

class multidict_keys(object):
	def __init__(self, md):
		self._md = md

	def __len__(self):
		return self._md._len

	def __iter__(self):
		for ki in self._md._dict.items():
			for i in range(0, len(ki)):
				yield ki[0]

	def __contains__(self, key):
		return key in self._md._dict

	def isdisjoint(self, other):
		for v in other:
			if v in self:
				return False
		return True

class multidict_values(object):
	def __init__(self, md):
		self._md = md

	def __len__(self):
		return self._md._len

	def __iter__(self):
		for ki in self._md._dict.items():
			for vi in ki[1]:
				yield vi

	def __contains__(self, value):
		return value in iter(self)

	def isdisjoint(self, other):
		for v in other:
			if v in self:
				return False
		return True

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

	def items(self):
		return multidict_items(self)

	def keys(self):
		return multidict_keys(self)

	def values(self):
		return multidict_values(self)

	def pop(self, key, default=None):
		ki = self._dict.get(key)
		if ki is not None:
			v = ki.pop(self._sel)
			if len(ki)==0:
				del self._dict[key]
			return v
		else:
			if default is None:
				raise KeyError(key)
			else:
				return default

	def popitem(self):
		# From the docs:
		#	Changed in version 3.7.
		#	LIFO order is now guaranteed. In prior versions, popitem() would
		#	return an arbitrary key/value pair.
		#
		# I can't justify the runtime or effort required to comply with this
		# behaviour. I'll implement the method but with semantics that don't
		# comply with >=3.7 behaviour.

		try:
			ki = next(iter(self._dict.items()))
		except StopIteration:
			raise KeyError("popitem(): dictionary is empty")
		else:
			v = ki[1].pop(self._sel)
			if len(ki[1])==0:
				del self._dict[ki[0]]
			return (ki[0], v)

	def setdefault(self, key, default=None):
		val = self._dict.setdefault(key, [])
		val.append(default)
		return val[-1]

	def update(self, src=None, **kwargs):
		if isinstance(src, multidict):
			for ki in src._dict.items():
				for val in ki[1]:
					self[ki[0]] = val
		elif isinstance(src, dict):
			for item in src.items():
				self[item[0]] = item[1]
		else:
			for kv in enumerate(src):
				try:
					seq = iter(kv[1])
				except:
					raise TypeError("cannot convert dictionary update sequence element #{} to a sequence".format(kv[0]))
				def first10(it):
					for c in range(10):
						yield next(it)
				lst = list(first10(seq))
				l = len(lst)
				if l!=2:
					if l>=10:
						l = ">=10"
					raise ValueError("dictionary update sequence element #{} has length {}; 2 is required".format(kv[0], l))
				self[lst[0]] = lst[1]

		for arg in kwargs.items():
			self[arg[0]] = arg[1]

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
			del items[self._sel:]
		self._len -= 1

	def __iter__(self):
		return iter(self._dict)

	def __reversed__(self):
		raise TypeError("'multidict' object is not reversible")

	def __contains__(self, key):
		return key in self._dict

	def __repr__(self):
		return repr(self._dict)

	def __format__(self, format_spec):
		return self.dict.__format__(format_spec)

	def __eq__(self, other):
		return self._dict==other

	def __ne__(self, other):
		return self._dict!=other

if __name__=='__main__':
	m = multidict({1: ["one", "One"], 2:["two", "Two"]})
	print(m)
	r = m.setdefault(3, "three")
	print(m, r)
	r = m.setdefault(3, "Three")
	print(m, r)
	r = m.setdefault(4)
	print(m, r)
