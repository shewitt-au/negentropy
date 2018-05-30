import decoders
from M6502 import *

class M6502Decoder(decoders.Prefix):
	def __init__(self, name):
		self.name = name

	def cutting_policy(self):
		return decoders.CuttingPolicy.Guided

	def preprocess(self, ctx, ivl, cutter):
		ii = None
		for ii in M6502Iterator(ctx.mem, ivl):
			cutter.atomic(ii.ivl)
			ctx.link_add_reachable(ii.ivl.first)
			if ii.target is not None:
				ctx.link_add_referenced(ii.target)
		cutter.done()
		# return the non-processed part of the interval
		return ivl if ii is None else Interval(ii.ivl.last+1, ivl.last)

	def decode(self, ctx, ivl, params):
		def lines(self):
			target_already_exits = params['target_already_exits']

			for ii in M6502Iterator(ctx.mem, ivl):
				def format_numerical_operand(v):
					if ii.mode_info.operand_size==0:
						return ""
					elif ii.op_info.mode==AddrMode.Relative or ii.mode_info.operand_size==2:
						return "${:04x}".format(v)
					elif ii.mode_info.operand_size==1:
						return "${:02x}".format(v)

				target = None
				if ii.target:
					# If we have a target look it up. If we don't find it try the address
					# before (we'll tack on a '+1').
					s = ctx.syms.by_address.get(ii.target)
					if s:
						one_before = False
						target = ii.target
					else:
						s = ctx.syms.by_address.get(ii.target-1)
						one_before = s is not None
						target = ii.target-1 if one_before else ii.target

					if s:
						operand_body = s[1]
					else:
						operand_body = format_numerical_operand(ii.target)
				else:
					one_before = False
					operand_body = format_numerical_operand(ii.operand)

				yield {
					'address': ii.ivl.first,
					'is_destination' : (not target_already_exits) and ctx.is_destination(ii.ivl.first),
					'bytes': ctx.mem.r8m(ii.ivl.first, ii.mode_info.operand_size+1),
					'instruction': {
						'mnemonic': ii.op_info.mnemonic,
						'pre': ii.mode_info.pre,
						'post': ii.mode_info.post,
						'operand': operand_body,
						'op_adjust': '+1' if one_before else '',
						'is_source' : ctx.is_destination(target),
						'target' : target
						}
					}

				target_already_exits = False

		return {
				'type': self.name,
				'lines': lines(self)
				}
