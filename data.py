from interval import Interval

class DataDecoder(object):
	def __init__(self, size, mem, syms, cmts):
		self.size = size
		self.mem = mem
		self.syms = syms
		self.cmts = cmts
	
	def decode(self, ivl):
		addr = ivl.first

		for i in ivl.cut_left_iter(self.syms.keys_in_range(ivl)):
			if i.first in self.syms:
				print(self.syms[i.first], end="")
			for n in range(0, len(i)):
				if n%16 == 0:
					print("\n{:04x}\t".format(i.first+n), end="\t")
				elif n%4 == 0:
					print(" ", end="")
				print("{:02x}".format(self.mem.r8(i.first+n)), end=" ")
			print()
