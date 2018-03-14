#!/usr/bin/env python3

import M6502
import memory
import symbols
import decoders

def main():
	sym = symbols.read_symbols()
	cmt = symbols.read_comments()

	with open("5000-8fff.bin", "rb") as f:
		f = open("5000-8fff.bin", "rb")
		m = memory.Memory(f.read(), 0x5000)

	decoders.init_decoders(m, sym, cmt)

	d = M6502.Diss(m, sym, cmt)
	a = 0x6b16
	while a!=0x6b5d:
		a = d.analyse(a)

	mmap = memory.MemType("MemType.txt")
	print(mmap.mem_map)

main()
