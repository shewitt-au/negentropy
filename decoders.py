import diss

class NullDecoder(object):
	pass

decoders = {
	"bitmap" : NullDecoder,
	"data" : NullDecoder,
	"ptr16" : NullDecoder,
	"code" : diss.Diss
	}
