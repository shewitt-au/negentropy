# Handle ACME anonymous labels.
# The ACME assembler can be found here: https://sourceforge.net/projects/acme-crossass/

# ACME anonymous labels are a number of "+" (for forward references) or
# "-" (back references) symbols. "-" is a distinct symbol from '--' (the same
# goes for "+"). We use this class the track free "names", where a "name" is
# the number of times the symbol is repeated. It returns the lowest free "name".

import heapq

class LowestFree(object):
	def __init__(self):
		self.free = -1

	# return the lowest free (starting from 1) and mark it as used
	def aquire(self):
		just_lowest = self.free&-self.free
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

	# we sort by 'dst', which is the end the label is applied to.
	def __eq__(self, other):
		return self.dst == other.dst
	def __ne__(self, other):
		return self.dst != other.dst
	def __lt__(self, other):
		return self.dst < other.dst
	def __le__(self, other):
		return self.dst <= other.dst
	def __gt__(self, other):
		return self.dst > other.dst
	def __ge__(self, other):
		return self.dst >= other.dst

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
				overtaken = heapq.heappop(self.active)
				self.lowest.release(overtaken[1])
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

		for r in self.refs:
			offset = r.offset()
			if offset>=0:
				label = forward.label(r)
			else:
				label = back.label(r)
			print(r, ('+' if offset>=0 else '-')*label)

if __name__=='__main__':
	x = AcmeAnonAssigner()
	x.add(0x0, 0x30)
	x.add(0x10, 0x40)
	x.add(0x020, 0x3e)
	x.add(0x3c, 0x3d)

	x.process()
