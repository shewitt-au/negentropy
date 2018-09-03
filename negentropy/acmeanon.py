# Handle ACME anonymous labels.
# The ACME assembler can be found here: https://sourceforge.net/projects/acme-crossass/

import heapq

# ACME anonymous labels are a number of "+" (for forward references) or
# "-" (back references) symbols. "-" is a distinct symbol from '--' (the same
# goes for "+"). We use this class the track free "names", where a "name" is
# the number of times the symbol is repeated. It returns the lowest free "name".
class LowestFree(object):
	def __init__(self):
		self.free = -1

	# return the lowest free (starting from 1) and mark it as used
	def aquire(self):
		just_lowest = self.free&-self.free # a touch of bit twiddling is good for the soul
		self.free &= ~just_lowest
		return just_lowest.bit_length()

	# set num to free
	def release(self, num):
		self.free |= 1<<(num-1)

class RefInfo(object):
	def __init__(self, src, dst):
		self.src = src
		self.dst = dst

	def top(self):
		return min(self.src, self.dst)
	def bottom(self):
		return max(self.src, self.dst)
	def offset(self):
		return self.dst-self.src
	def size(self):
		return abs(self.dst-self.src)
	def dir(self):
		return 1 if self.dst>=self.src else -1

	# Decide whether to include a reference based on the one before it
	# as sorted by the comparison functions below.
	def filter(self, contender):
		if self.dst != contender.dst:
			return True
		assert (self.dir()==contender.dir()), "!!!" # TODO: this should be an exception
		return False

	# We compare by 'dst' first but back references are less than forward references.
	# If 'dst' and direction are the same references with larger scopes are less
	# than those with smaller scopes. The sorting order is important for the proper
	# functioning of the algorithm.
	def __eq__(self, other):
		return self.dst==other.dst and self.src==other.src
	def __ne__(self, other):
		return self.dst!=other.dst or self.src!=other.src
	def __lt__(self, other):
		return self.dst<other.dst or \
			(self.dst==other.dst and (self.dir()<other.dir() or \
				(self.dir()==other.dir() and self.size()>other.size())))
	def __le__(self, other):
		return self.dst<other.dst or \
			(self.dst==other.dst and (self.dir()<other.dir() or \
				(self.dir()==other.dir() and self.size()>=other.size())))
	def __gt__(self, other):
		return self.dst>other.dst or \
			(self.dst==other.dst and (self.dir()>other.dir() or \
				(self.dir()==other.dir() and self.size()<other.size())))
	def __ge__(self, other):
		return self.dst>other.dst or \
			(self.dst==other.dst and (self.dir()>other.dir() or \
				(self.dir()==other.dir() and self.size()<=other.size())))

	def __repr__(self):
		o = self.offset()
		if o>0:
			return "RefInfo(${:04x}-->${:04x})".format(self.src, self.dst)
		elif o<0:
			return "RefInfo(${:04x}<--${:04x})".format(self.dst, self.src)
		else:
			return "RefInfo(${0:04x}---${0:04x})".format(self.src)

# As long as two references overlap they can't have the same number.
# This class is used to track what is and isn't still in scope and assign
# labels using that data. 
class ScopeTracker(object):
	def __init__(self):
		self.lowest = LowestFree()
		self.active = [] # tuples: (bottom, label)

	def label(self, r):
		# first we remove any references we have overtaken
		top = r.top()
		if self.active:
			while top>self.active[0][0]:
				self.lowest.release(heapq.heappop(self.active)[1])
				if not self.active:
					break
		# label this one and add it to the active heap
		label = self.lowest.aquire()
		heapq.heappush(self.active, (r.bottom(), label))

		return label

class AcmeAnonAssigner(object):
	def __init__(self):
		self.refs = []

	def add(self, src, dst):
		self.refs.append(RefInfo(src, dst))

	def process(self):
		self.refs.sort()

		# forward and backward are in different namespaces so we need two
		forward = ScopeTracker()
		back = ScopeTracker()

		def process_item(r):
			offset = r.offset()
			if offset>=0:
				label = forward.label(r)
			else:
				label = back.label(r)
			print(r, ('+' if offset>=0 else '-')*label)

		it = iter(self.refs)
		try:
			r = next(it)
		except StopIteration:
			pass
		else:
			process_item(r)
			prev = r
			for r in it:
				if prev.filter(r):
					process_item(r)
				prev = r


if __name__=='__main__':
	x = AcmeAnonAssigner()
	r = [(3, 0x100), (1, 0x100), (0, 0x100), (5, 0x100)]
	r.extend([(0x80, 0x90), (0x85, 0x95)])
	r.extend([(0x200, 0x105)])
	for ri in r:
		x.add(ri[0], ri[1])
	x.process()
