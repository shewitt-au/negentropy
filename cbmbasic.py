import decoders

# $80 - $a2
_commands = (
	"END",    "FOR",   "NEXT", "DATA", "INPUT#",  "INPUT",  "DIM",   "READ",
	"LET",    "GOTO",  "RUN",  "IF",   "RESTORE", "GOSUB",  "RETURN", "REM",
	"STOP",   "ON",    "WAIT", "LOAD", "SAVE",    "VERIFY", "DEF",    "POKE",
	"PRINT#", "PRINT", "CONT", "LIST", "CLR",     "CMD",    "SYS",    "OPEN",
	"CLOSE",  "GET",   "NEW")

def command(token):
	if token==0xb2:
		return "="
	elif token-0x80>=len(_commands):
		return "?"
	else:
		return _commands[token-0x80]

# https://en.wikipedia.org/wiki/PETSCII
_substitute = {
#TODO: Some of these may be reverse video
		0x5c: '£',
		0x5e: '↑',
		0x5f: '←',
		0x60: '─',
		0x61: '♠',
		0x62: '│',
		0x63: '─',
		0x64: None,
		0x65: None,
		0x66: None,
		0x67: None,
		0x68: None,
		0x69: '╮',
		0x6a: '╰',
		0x6b: '╯',
		0x6c: None,
		0x6d: '╲',
		0x6e: '╱',
		0x6f: None,
		0x70: None,
		0x71: '●',
		0x72: None,
		0x73: '♥',
		0x74: None,
		0x75: '╭',
		0x76: '╳',
		0x77: '○',
		0x78: '♣',
		0x79: None,
		0x7a: '♦',
		0x7b: '┼',
		0x7c: None,
		0x7d: '│',
		0x7e: 'π',
		0x7f: '◥',
		0xa1: '▌',
		0xa2: '▄',
		0xa3: '▔',
		0xa4: '▁',
		0xa5: '▏',
		0xa6: '▒',
		0xa7: '▕',
		0xa8: None,
		0xa9: '◤',
		0xaa: None,
		0xab: '├',
		0xac: '▗',
		0xad: '└',
		0xae: '┐',
		0xaf: '▂',
		0xb0: '┌',
		0xb1: '┴',
		0xb2: '┬',
		0xb3: '┤',
		0xb4: '▎',
		0xb5: '▍',
		0xb6: None,
		0xb7: None,
		0xb8: None,
		0xb9: '▃',
		0xba: None,
		0xbb: '▖',
		0xbc: '▝',
		0xbd: '┘',
		0xbe: '▘',
		0xbf: '▚',
		0xc0: '━',
		0xc1: '♠',
		0xc2: '│',
		0xc3: '━',
		0xc4: None,
		0xc5: None,
		0xc6: None,
		0xc7: None,
		0xc8: None,
		0xc9: '╮',
		0xca: '╰',
		0xcc: None,
		0xcb: '╯',
		0xcd: '╲',
		0xce: '╱',
		0xcf: None,
		0xd0: None,
		0xd1: '●',
		0xd2: None,
		0xd3: '♥',
		0xd4: None,
		0xd5: '╭',
		0xd6: '╳',
		0xd7: '○',
		0xd8: '♣',
		0xd9: None,
		0xda: '♦',
		0xdb: '┼',
		0xdc: None,
		0xdd: '│',
		0xde: 'π',
		0xdf: '◥',
		0xe0: chr(0xa0),
		0xe1: '▌',
		0xe2: '▄',
		0xe3: '▔',
		0xe4: '▁',
		0xe5: '▏',
		0xe6: '▒',
		0xe7: '▕',
		0xe8: None,
		0xe9: '◤',
		0xea: None,
		0xeb: '├',
		0xec: '▗',
		0xed: '└',
		0xee: '┐',
		0xef: '▂',
		0xf0: '┌',
		0xf1: '┴',
		0xf2: '┬',
		0xf3: '┤',
		0xf4: '▎',
		0xf5: '▍',
		0xf6: '◤',
		0xf7: '◤',
		0xf8: '◤',
		0xf9: '▃',
		0xfa: '◤',
		0xfb: '▖',
		0xfc: '▝',
		0xfd: '┘',
		0xfe: '▘',
		0xff: 'π'
		}

def pettoascii(c):
	return _substitute.get(c, chr(c))

class BasicDecoder(decoders.Prefix):
	def decode(self, ctx, ivl):
		addr = ivl.first
		while True:
			# link to next line
			link = ctx.mem.r16(addr)
			if link==0:
				break # a line link of 0 end the program
			addr += 2

			# line number
			# line numbers from 0-65535
			# largest enter-able is 63999 (not sure why), but larger runs and list fine
			print(ctx.mem.r16(addr), end=' ') # line numbers separated by a space
			addr += 2

			while True:
				token = ctx.mem.r8(addr)
				addr += 1

				if token==0x22: # quotes
					print('"', end='')
					while True:
						token = ctx.mem.r8(addr)
						addr += 1
						if token==0x22: # quotes
							print('"', end='')
							break
						elif token==0x00:
							break
						else:
							print(pettoascii(token), end='')
					if token==0x00: #H!!!ACK!!!
						break
				else:
					if token == 0: # end of line
						break
					elif token&0x80:
						print(command(token), end='')
					else:
						print(pettoascii(token), end='')

			print()

if __name__=='__main__':
	import memory
	from interval import Interval

	class Context(object):
		def __init__(self, mem):
			self.mem = mem

	address = None
	with open("monopoly.prg", "rb") as f:
		contents = f.read()
		mem = memory.Memory(contents)

	ctx = Context(mem)

	bd = BasicDecoder()
	bd.decode(ctx, mem.range())
