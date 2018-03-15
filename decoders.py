import M6502
import data

class NullDecoder(object):
	def __init__(self, name):
		self.name = name
	
	def decode(self, addr):
		print(self.name + ": decoder not implemmented!")

decoders = None

def init_decoders(mem, syms, cmts):
	global decoders
	decoders = {
		"bitmap" : NullDecoder("bitmap"),
		"data" : data.DataDecoder(1, mem, syms, cmts),
		"ptr16" : NullDecoder("ptr16"),
		"code" : M6502.Diss(mem, syms, cmts)
		}
