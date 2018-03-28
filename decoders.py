import M6502
import data

class Context(object):
	def __init__(self, mem, syms, cmts):
		self.mem = mem
		self.syms = syms
		self.cmts = cmts

decoders = None

def init_decoders(ctx):
	global decoders
	decoders = {
		"bitmap" : None,
		"data" : data.decode,
		"ptr16" :None,
		"code" : M6502.decode
		}
