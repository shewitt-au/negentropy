from heapq import merge
from interval import Interval
import decoders

class DataDecoder(object):
	def __init__(self, name, wordlen, linelen):
		self.name = name
		self.wordlen = wordlen
		self.linelen = linelen

	def targets(self, ctx, ivl):
		return set()

	def decode(self, ctx, ivl, params):
		if self.wordlen==1:
			rd = ctx.mem.r8m
		elif self.wordlen==2:
			rd = ctx.mem.r16m
		else:
			raise IndexError("Illegal operand size.")
		bpl = self.wordlen*self.linelen

		for i in ivl.cut_left_iter(merge(ctx.syms.keys_in_range(ivl), ctx.cmts.keys_in_range(ivl))):
			base_val = ctx.prefix(i)
			yield {
					**base_val,
					**{
						"type" : self.name,
						"address": i.first,
						"bytes": rd(i.first, min(len(i), self.linelen))
					}
				}
			for addr in range(i.first+bpl, i.last+1, bpl):
				yield {
					"type" : self.name,
					"address": addr,
					"bytes": rd(addr, min(i.last-addr+1, self.linelen))
					}
