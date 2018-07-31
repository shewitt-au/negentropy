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
			for i in range(len(ki[1])):
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

# Used to pass a dict to multidict that is used as the representation.
# multidict takes ownership of the wrapped dict. 
class hijack(object):
	def __init__(self, d):
		self._dict = d

class multidict(object):
	def __init__(self, src=None, **kwargs):
		if src is None:
			self._dict = {}
			self._len = 0
			self.update(**kwargs)
		elif isinstance(src, hijack):
			# Allow initialisation from a regular dict 
			self._dict = src._dict
			self._recalclen()
			self.update(**kwargs)
		else:
			self._dict = {}
			self._len = 0
			self.update(src, **kwargs)

	@classmethod
	def fromkeys(cls, seq, value=None):
		md = cls()
		for v in seq:
			md[v] = value
		return md

	def clear(self):
		self._dict.clear()
		self._len = 0

	def copy(self):
		return copy.copy(self)

	def get(self, key, default=None):
		items = self._dict.get(key)
		if items is None:
			return default
		else:
			return items[-1]

	def items(self):
		return multidict_items(self)

	def keys(self):
		return multidict_keys(self)

	def values(self):
		return multidict_values(self)

	def pop(self, key, default=None):
		ki = self._dict.get(key)
		if ki is not None:
			v = ki.pop(-1)
			if len(ki)==0:
				del self._dict[key]
			self._len -= 1
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
		# I can't justify the cost or effort required to comply with this
		# behaviour. I'll implement the method but with semantics that don't
		# comply with >=3.7 behaviour.

		try:
			ki = next(iter(self._dict.items()))
		except StopIteration:
			raise KeyError("popitem(): dictionary is empty")
		else:
			v = ki[1].pop(-1)
			if len(ki[1])==0:
				del self._dict[ki[0]]
			self._len -= 1
			return (ki[0], v)

	def setdefault(self, key, default=None):
		val = self._dict.setdefault(key, [])
		if len(val)==0:
			val.append(default)
			self._len += 1
			return default
		else:
			return val[-1]

	def update(self, src=None, **kwargs):
		if isinstance(src, multidict):
			for ki in src._dict.items():
				self._dict.setdefault(ki[0], []).extend(ki[1])
				self._len += len(ki[1])
		elif isinstance(src, dict):
			for item in src.items():
				self[item[0]] = item[1]
		elif src is not None:
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

	def __len__(self):
		return self._len

	def __getitem__(self, key):
		try:
			ki = self._dict[key]
		except KeyError:
			return self.__missing__(key)
		else:
			return ki[-1]

	def __missing__(self, key):
		raise KeyError(key)

	def __setitem__(self, key, value):
		self._dict.setdefault(key, []).append(value)
		self._len += 1

	def __delitem__(self, key):
		#TODO: is this the behaviour we want?
		ki = self._dict[key]
		if len(ki)==1:
			del self._dict[key]
		else:
			del ki[-1]
		self._len -= 1

	def __iter__(self):
		return iter(self._dict)

	def __reversed__(self):
		raise TypeError("'multidict' object is not reversible")

	def __contains__(self, key):
		return key in self._dict

	def __repr__(self):
		if len(self._dict)!=0:
			return "multidict(hijack({}))".format(repr(self._dict))
		else:
			return "multidict()"

	def __format__(self, format_spec):
		return self._dict.__format__(format_spec)

	def __eq__(self, other):
		return self._dict==other

	def __ne__(self, other):
		return self._dict!=other

	def _recalclen(self):
		self._len = 0
		for v in self._dict.values():
			self._len += len(v)

if __name__=='__main__':
	print("Empty construction")
	print("------------------")
	ed = multidict()
	print(ed)
	print("len:", len(ed))
	print("keys:", [k for k in ed.keys()], len(ed.keys()))
	print("value:", [v for v in ed.values()], len(ed.values()))
	print("items:", [i for i in ed.items()], len(ed.items()))
	print()

	print("Hijack construction")
	print("-------------------")
	hjd = multidict(hijack({1:["one", "One"], 2:["two", "Two"]}))
	print(hjd)
	print("len:", len(hjd))
	print("keys:", [k for k in hjd.keys()], len(hjd.keys()))
	print("value:", [v for v in hjd.values()], len(hjd.values()))
	print("items:", [i for i in hjd.items()], len(hjd.items()))
	print()

	print("Construction from dict")
	print("-----------------------")
	sd = {"abba": "cool", "rap": "shit", "blues": "influential"}
	print("Source dict:", sd)
	fdd = multidict(sd)
	print(fdd)
	print("len:", len(fdd))
	print("keys:", [k for k in fdd.keys()], len(fdd.keys()))
	print("value:", [v for v in fdd.values()], len(fdd.values()))
	print("items:", [i for i in fdd.items()], len(fdd.items()))
	print()

	print("Construction iterable")
	print("---------------------")
	sl = {("old car", "smashed"), ("new car", "thank goodness")}
	print("Source list:", sl)
	itd = multidict(sl)
	print(itd)
	print("len:", len(itd))
	print("keys:", [k for k in itd.keys()], len(itd.keys()))
	print("value:", [v for v in itd.values()], len(itd.values()))
	print("items:", [i for i in itd.items()], len(itd.items()))
	print()

	print("fromkeys")
	print("--------")
	fkd = multidict.fromkeys(range(0, 4), "a number")
	print(fkd)
	print("len:", len(fkd))
	print("keys:", [k for k in fkd.keys()], len(fkd.keys()))
	print("value:", [v for v in fkd.values()], len(fkd.values()))
	print("items:", [i for i in fkd.items()], len(fkd.items()))
	print()

	print("pop")
	print("---")
	pd = multidict(hijack({1:["one", "One"], 2:["two", "Two"]}))
	print(pd)
	print("len:", len(pd))
	print("pd.pop(1): '{}' len: {}".format(pd.pop(1), len(pd)))
	print(pd)
	print("pd.pop(1): '{}' len: {}".format(pd.pop(1), len(pd)))
	print(pd)
	try:
		print("pd.pop(1): '{}' len: {}".format(pd.pop(1), len(pd)))
		print(pd)
	except KeyError as e:
		print("Expected: KeyError({})".format(e))
	print("pd.pop(1, 'default'): '{}' len: {}".format(pd.pop(1, 'default'), len(pd)))
	print(pd)
	print()

	print("popitem")
	print("-------")
	pid = multidict(hijack({1:["one", "One"], 2:["two", "Two"], "yellow":["colour", "slur"]}))
	print(pid)
	print("len:", len(pid))
	try:
		while True:
			print(pid.popitem())
	except KeyError as e:
		print("Expected: KeyError({})".format(e))
	print()

	print("setdefault")
	print("----------")
	sdd = multidict(hijack({1:["one", "One"], 2:["two", "Two"], "yellow":["colour", "slur"]}))
	print(sdd)
	print("len:", len(sdd))
	print("sdd.setdefault(1): {}, len: {}".format(sdd.setdefault(1), len(sdd)))
	print(sdd)
	print("sdd.setdefault(6, 'six'): {}, len: {}".format(sdd.setdefault(6, 'six'), len(sdd)))
	print(sdd)
	print()

	print("update")
	print("------")
	ud = multidict()
	print(ud)
	print("len:", len(ud))
	print("From sdd (multidict): {}".format(sdd))
	ud.update(sdd)
	print("ud.update(sdd): {}, len: {}".format(ud, len(ud)))
	print("From itd (multidict): {}".format(itd))
	ud.update(itd)
	print("ud.update(itd): {}, len: {}".format(ud, len(ud)))
	print()
