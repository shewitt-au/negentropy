from heapq import merge
from interval import Interval

class DataDecoder(object):
	def __init__(self, size, mem, syms, cmts):
		self.size = size
		self.mem = mem
		self.syms = syms
		self.cmts = cmts
	
	def decode(self, ivl):
		for i in ivl.cut_left_iter(merge(self.syms.keys_in_range(ivl), self.cmts.keys_in_range(ivl))):

			c = self.cmts.get(i.first)
			if c and c[0]:
				print("".join(["; {}\n".format(cl) for cl in c[0].splitlines()]), end="")
			s = self.syms.get(i.first)
			if s:
				print(s, end="")
			if c and c[1]:
				print()
				print("".join(["; {}\n".format(cl) for cl in c[1].splitlines()]).rstrip(), end="")


			for n in range(len(i)):
				if n%16 == 0:
					print("\n{:04x}\t".format(i.first+n), end="\t")
				elif n%4 == 0:
					print(" ", end="")
				print("{:02x}".format(self.mem.r8(i.first+n)), end=" ")
			print()
