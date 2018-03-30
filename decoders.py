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
		"bitmap" : data.data_decoder("data"),
		"data" : data.data_decoder("data"),
		"ptr16" : data.data_decoder("ptr16", 16),
		"code" : M6502.decode_6502
		}
