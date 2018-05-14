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
					"-w", "--webbrowser",
					action="store_true",
					help="open OUT in webbrowser when done")
	parser.add_argument(
					"-t", "--title",
					help="title of the generated HTML page")
	parser.add_argument(
					"-m", "--memtype",
					help="file that describes what kind of data address ranges contain"
					)
	parser.add_argument(
					"-g", "--gaps",
					action="store_true",
					help="show gaps in memtype file (implies '--defaultdecoder data' if no decoder specified)"
					)
	parser.add_argument(
					"-d", "--defaultdecoder",
					help="default decoder if address is not in MEMTYPE file (implies --gaps)"
					)
	parser.add_argument(
					"-l", "--labels",
					action="append",
					help="file for mapping addresses to symbolic names (labels)")
	parser.add_argument(
					"-c", "--comments",
					help="file used to inject comments into the disassembly")
	parser.add_argument(
					"-o", "--origin",
					type=(lambda v: int(v, 16)),
					help="address IN expects to be loaded at (if absent the first two bytes are used)")

	args = parser.parse_args()

	# post-processing
	if args.gaps is True and args.defaultdecoder is None:
		args.defaultdecoder = "data"
	
	templates.run(args)

main()
