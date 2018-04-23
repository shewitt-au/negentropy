import M6502
import data
import gfx

class Context(object):
	def __init__(self, mem, syms, cmts):
		self.mem = mem
		self.syms = syms
		self.cmts = cmts

def base_decoder(ctx, ivl):
	c = ctx.cmts.get(ivl.first)
	return {
		"label" : ctx.syms.get(ivl.first),
		"comment_before": None if c is None else c[0],
		"comment_after": None if c is None else c[1],
		"comment_inline": None if c is None else c[2]
		}

decoders = None

def init_decoders(ctx):
	global decoders
	decoders = {
		"bitmap" : gfx.decode_chars,
		"data" : data.data_decoder("data", 1, 16),
		"ptr16" : data.data_decoder("ptr16", 2, 8),
		"code" : M6502.decode_6502
		}
