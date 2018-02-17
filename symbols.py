import re

symbols_re = re.compile(r"ali?\s*C:([0-9A-Fa-f]{4})\s*([^\s]*)")

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

	with open("Comments.txt", "r") as f:

		before = ""
		after = ""
		inline = ""
		pos = 0 # before
		addr = -1

		def update_stinggs():
			if line[0:2] == r"\/":
				line = line[2:]
				after += line+"\n"
			elif line[0] == r">":
				line = line[1:]
				inline += line+"\n"
			else:
				before += line+"\n"

		for line in f:
			if line=="":
				continue
			m = re.match(comments_re, line)
			if not m:
				continue
			line = m[2]

			newaddr = int(m[1], 16)

			if addr!=newaddr:
				comments[addr] = (before, after, inline)
				pos = 0 # before
				before = after = inline = ""

			if not line=="":
				if line[0:2] == r"\/":
					pos = 1 # after
					line = line[2:]
				elif line[0] == r">":
					pos = 2 # inline
					line = line[1:]
			if pos==0:
				before += line+"\n"
			elif pos==1:
				after += line+"\n"
			elif pos==2:
				inline += line+"\n"

			addr = newaddr

	# Add the last one
	comments[addr] = (before, after, inline)

	del comments[-1] # Remove the invalid entry

	return comments
