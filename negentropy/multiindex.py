import bisect

# A crude implementation of a multi-index container.
# You should NOT carelessly change the key values in a way that invalidate
# the indices.

# Class needed because bisect doesn't support key extractors
class KeyWrapper(object):
	def __init__(self, key_extractor, value):
		self.key_extractor = key_extractor
		self.key = value

	def __eq__(self, other):
		return self.key == self.key_extractor(other)
	def __ne__(self, other):
		return self.key != self.key_extractor(other)
	def __lt__(self, other):
		return self.key < self.key_extractor(other)
	def __le__(self, other):
		return self.key <= self.key_extractor(other)
	def __gt__(self, other):
		return self.key > self.key_extractor(other)
	def __ge__(self, other):
		return self.key >= self.key_extractor(other)

def list_indexer(coll, value, key_extractor):
	coll.append(value)

def dict_indexer(coll, value, key_extractor):
	coll[key_extractor(value)] = value

def sorted_list_indexer(coll, value, key_extractor):
	idx = bisect.bisect_right(coll, KeyWrapper(key_extractor, key_extractor(value)))
	coll.insert(idx, value)

class MultiIndex(object):
	def __init__(self):
		self.indices = []

	# Add an index. When 'add' is called all indices added here are updated.
	# Supplements the instance with two attributes:
	#  1. index_name: a property which returns the index.
	#  2. index_name+'_compare': a method which returns a KeyWrapper instance
	#     for the index initialised with the argument it's called with.
	def add_index(self, index_name, collection, inserter, key_extractor=None):
		coll = collection()
		self.indices.append((coll, inserter, key_extractor))

		setattr(self, index_name, coll)
		def get_comp(value):
			return KeyWrapper(key_extractor, value)
		setattr(self, index_name+'_compare', get_comp)

	def add(self, value):
		for i in self.indices:
			i[1](i[0], value, i[2])

	def add_iter(self, iterable):
		for v in iterable:
			self.add(v)
