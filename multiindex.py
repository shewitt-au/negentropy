import bisect

# A crude implementation of a multi-index container.
# Since we read in the data files and then the in-memory data is never changed
# no attempt is made to implement updatability. This obviously implies that
# you should NOT change the key values in any of the collections as it will
# invalidate the indices.

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

	def add_index(self, mathod_name, collection, inserter, key_extractor=None):
		coll = collection()
		setattr(self, mathod_name, coll)
		self.indices.append((coll, inserter, key_extractor))
		return len(self.indices)-1

	def add(self, value):
		for i in self.indices:
			i[1](i[0], value, i[2])

	def add_iter(self, iterable):
		for v in iterable:
			self.add(v)

	# Do not change and keys in the returned collection
	def get_index(self, idx=0):
		return self.indices[idx][0]

	# Get an instance of the key comparison type for an index for value
	def get_key_compare(self, value, idx=0):
		return KeyWrapper(self.indices[idx][2], value)

	def get(self, key, default=None, idx=0):
		return self.indices[idx][0].get(key, default)
