import M6502

class NullDecoder(object):
	pass

decoders = None

def init_decoders(mem, syms, cmts):
	decoders = {
		"bitmap" : NullDecoder,
		"data" : NullDecoder,
		"ptr16" : NullDecoder,
		"code" : M6502.Diss(mem, syms, cmts)
		}
