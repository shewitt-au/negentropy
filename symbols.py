import re

symbols_re = re.compile(r"ali?\s*C:([0-9A-Fa-f]{4})\s*(.?\w*)")

def read_symbols():
	symbols = {}

	with open("BD.txt", "r") as f:
		for line in f:
			if line=="":
				continue
			m = re.match(symbols_re, line)
			if m:
				symbols[int(m[1], 16)] = m[2]

	return symbols

comments_re = re.compile(r"([0-9A-Fa-f]{4})\s*(.*)")

def read_comments():
	comments = {}

	def add():
		if cmt[0:2] == r"\/":
			comments[addr] = (True, cmt[2:])
		else:
			comments[addr] = (False, cmt)

	cmt = ""
	addr = None

	with open("Comments.txt", "r") as f:
		for line in f:
			if line=="":
				continue
			m = re.match(comments_re, line)
			if not m:
				continue

			newaddr = int(m[1], 16)
			if m:
				if addr == None:
					addr = newaddr
					cmt += m[2]
				else:
					if addr == newaddr:
						cmt += "\n"+m[2]
					else:
						add() # Add the previous complete comment
						addr = newaddr
						cmt = m[2]

	# Add the last one
	add()

	return comments
