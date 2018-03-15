#!/usr/bin/env python3

from interval import Interval
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
	mmap = memory.MemType("MemType.txt")
	mmap.decode(Interval(0x74e0, 0x7ccc))

main()
