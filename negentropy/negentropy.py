#!/usr/bin/env python3

import time
from datetime import timedelta
from argparse import ArgumentParser

from . import templates
from . import errors

def main():
	start_time = time.time()

	parser = ArgumentParser(
					description="Disassemble a C64 image."
					)
	parser.add_argument(
					"input",
					nargs='?',
					metavar="IN",
					help="the binary file to disassemble"
					)
	parser.add_argument(
					"output",
					metavar="OUT",
					help="file to write the disassembly to"
					)
	parser.add_argument(
					"-c", "--config",
					action="append",
					help="specify configuration file (can be used multiple times)"
					)
	parser.add_argument(
					"-f", "--flag",
					dest="flags",
					default=[],
					action="append",
					help="set various flags")
	parser.add_argument(
					"-g", "--gaps",
					action="store_true",
					help="highlight gaps in memtype file (implies '--defaultdecoder data' if no decoder specified)"
					)
	parser.add_argument(
					"-d", "--defaultdecoder",
					help="default decoder if address is not in MEMTYPE file"
					)
	parser.add_argument(
					"-t", "--title",
					help="title of the generated HTML page")
	parser.add_argument(
					"-w", "--webbrowser",
					action="store_true",
					help="open OUT in webbrowser when done")
	parser.add_argument(
					"-i", "--info",
					action="store_true",
					help="include authoring info")
	parser.add_argument(
					"-o", "--origin",
					type=(lambda v: int(v, 16)),
					help="address IN expects to be loaded at (if absent the first two bytes are used)")
	parser.add_argument(
					"-r", "--format",
					default="html",
					help="the format of the output file")
	parser.add_argument(
					"-p", "--prefix",
					help="a file to prepend to the start of the output file")
	parser.add_argument(
					"--noc64symbols",
					action="store_true",
					help="don't use internal C64 symbol table")
	parser.add_argument(
					"-b", "--builton",
					action="store_true",
					help="include the date & time of the build")

	args = parser.parse_args()

	# post-processing
	if args.gaps is True and args.defaultdecoder is None:
		args.defaultdecoder = "data"
	try:
		templates.run(args)
	except errors.Dis64Exception as e:
		print(e)

	elapsed_time_secs = time.time() - start_time
	msg = "\nExecution took: %s secs" % timedelta(seconds=round(elapsed_time_secs))
	print(msg)

