#!/usr/bin/env python3

from argparse import ArgumentParser
import templates

def main():
	parser = ArgumentParser(
					description="Disassemble a C64 image."
					)
	parser.add_argument(
					"input",
					metavar="IN",
					help="the binary file to disassemble"
					)
	parser.add_argument(
					"output",
					metavar="OUT",
					help="file to write the disassembly to"
					)
	parser.add_argument(
					"-m", "--memtype",
					help="file that describes what kind of data address ranges contain"
					)
	parser.add_argument(
					"-d", "--defaultdecoder",
					help="default decoder if address is not in MEMTYPE file"
					)
	parser.add_argument(
					"-o", "--origin",
					type=(lambda v: int(v, 16)),
					help="address IN expects to be loaded at (if absent the first two bytes are used)")
	parser.add_argument(
					"-l", "--labels",
					help="file for mapping addresses to symbolic names (labels)")
	parser.add_argument(
					"-c", "--comments",
					help="file used to inject comments into the disassembly")
	parser.add_argument(
					"-w", "--webbrowser",
					action="store_true",
					help="open OUT in webbrowser when done")

	args = parser.parse_args()
	
	templates.run(args)

main()
