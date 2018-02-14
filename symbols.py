import re

line_re = re.compile(r"ali?\s*C:([0-9A-Fa-f]{4})\s*(.?\w*)")

def read_symbols():
	symbols = {}

	with open("BD.txt", "r") as f:
		for line in f:
			if line=="":
				continue
			m = re.match(line_re, line)
			if m:
				symbols[int(m[1], 16)] = m[2]

	return symbols
