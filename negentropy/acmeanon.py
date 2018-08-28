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

if __name__=='__main__':
	pass
