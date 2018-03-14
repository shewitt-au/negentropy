#!/usr/bin/env python3

import M6502
import memtype
import symbols
import decoders

class Memory(object):
	def __init__(self, data, org):
		self.data = data
		self.org = org

	def r(self, addr, sz):
		return self.data[addr-self.org : addr-self.org+sz]

	def r8(self, addr):
		return self.data[addr-self.org]

	def r16(self, addr):
		return self.data[addr-self.org] + self.data[addr-self.org+1]*256

def main():
	sym = symbols.read_symbols()
	cmt = symbols.read_comments()

	with open("5000-8fff.bin", "rb") as f:
		f = open("5000-8fff.bin", "rb")
		m = Memory(f.read(), 0x5000)

	decoders.init_decoders(m, sym, cmt)

	d = M6502.Diss(m, sym, cmt)
	a = 0x6b16
	while a!=0x6b5d:
		a = d.analyse(a)

	mmap = memtype.MemType("MemType.txt")
	print(mmap.mem_map)

main()
