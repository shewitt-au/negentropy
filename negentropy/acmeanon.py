# Handle ACME anonymous labels.
# The ACME assembler can be found here: https://sourceforge.net/projects/acme-crossass/

# ACME anonymous labels are a number of "+" (for forward references) or
# "-" (back references) symbols. "-" is a distinct symbol from '--' (the same
# goes for "+"). We use this class the track free "names", where a "name" is
# the number of times the symbol is repeated. It returns the lowest free "name".
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

	def offset(self):
		return self.dst-self.src

	def bottom(self):
		return max(self.src, self.dst)

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

if __name__=='__main__':
	r1 = RefInfo(0, 10)
	r2 = RefInfo(20, 11)
	r3 = RefInfo(12, 12)
	l = [r1, r2, r3]
	l.sort()
	print(l)
	print(r1.bottom())
