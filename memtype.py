import re

memtype_re = re.compile(r"^\s*([^\s]+)\s*([0-9A-Fa-f]{4})\s*([0-9A-Fa-f]{4})\s*$")

def read_memtype():
	ret = []
	with open("MemType.txt", "r") as f:
		for line in enumerate(f):
			m = re.match(memtype_re, line[1])
			if m is None:
				print("Error in line {} of memtype file".format(line[0]+1))
				raise ValueError("Error in memtype file")
			#print(m[1]+"\t"+m[2]+" "+m[3])
			ret.append(Interval(m[2], m[3]))

		ret.sort(reverse=True)
		return ret

class Interval(object):
	def __init__(self, ivl):
		self.value = ivl

	def __init__(self, first, last):
		self.first = int(first, 16)
		self.last = int(last, 16)
		assert self.first<=self.last, "Interval: first > last"

	def _get(self):
		return (self.first, self.last)

	def _set(self, ivl):
		self.first = ivl[0]
		self.last = ivl[1]
		assert self.first<=self.last, "Interval: first > last"

	def __eq__(self, other):
		return self.value == other.value
	def __ne__(self, other):
		return self.value != other.value
	def __lt__(self, other):
		return (self.first<other.first) or (self.first==other.first and self.last<other.last)
	def __gt__(self, other):
		return (self.first>other.first) or (self.first==other.first and self.last>other.last)
	def __le__(self, other):
		return (self.first<=other.first) and (self.last<=other.last)
	def __ge__(self, other):
		return (self.first>=other.first) and (self.last>=other.last)

	def __str__(self):
		return "${:04x}-${:04x}".format(self.first, self.last)

	def __repr__(self):
		return "Interval(${:04x}-${:04x})".format(self.first, self.last)

	value = property(_get, _set)
