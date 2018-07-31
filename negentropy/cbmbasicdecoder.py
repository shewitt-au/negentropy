from .interval import Interval
from . import decoders
from .cbmbasic import *

class TokenDecoder(object):
	def __init__(self, mem, codec):
		self.mem = mem
		self.codec = codec

	def value(self, token):
		return token.value(mem=self.mem, codec=self.codec)

class BasicDecoder(decoders.Prefix):
	def __init__(self, name):
		self.name = name

	def cutting_policy(self):
		return decoders.CuttingPolicy.Guided

	def preprocess(self, ctx, ivl, cutter):
		token = None
		p = Parser(ctx.mem, ivl)
		for token in p.tokens():
			if token.type == TokenType.LineLink:
				line_first = token.ivl.first
				ctx.link_add_reachable(line_first)
			elif token.type == TokenType.LineEnd:
				cutter.atomic(Interval(line_first, token.ivl.last))
			elif token.type == TokenType.LineNumberReference:
				addr = line_to_address(ctx.mem, ivl, token.value(mem=ctx.mem))
				ctx.link_add_referenced(addr)
			elif token.type == TokenType.Address:
				addr = token.value(ctx.mem)
				ctx.link_add_referenced(addr)
		cutter.done()

		# return the non-processed part of the interval
		unproc = Interval(token.ivl.last+1, ivl.last) if token else ivl
		return unproc

	_tt2name = {
		#TokenType.LineLink: "",
		TokenType.LineNumber: "line_num",
		TokenType.Command: "command",
		TokenType.Quoted: "quoted",
		TokenType.Colon: "text",
		TokenType.Semicolon: "text",
		TokenType.Comma: "text",
		TokenType.OpenBracket: "text",
		TokenType.CloseBracket: "text",
		TokenType.Spaces: "text",
		TokenType.Number: "text",
		TokenType.Text: "text",
		TokenType.LineNumberReference: "line_ref",
		TokenType.Address: "address"
		#TokenType.LineEnd: ""
		}

	def decode(self, ctx, ivl, params=None):
		def lines():
			def line_tokens():
				line_parser = Line(gen)
				for line_token in line_parser.tokens():
					tts = self._tt2name.get(line_token.type, None)
					if tts is not None:
						if line_token.type == TokenType.LineNumberReference:
							target = line_to_address(ctx.mem, ivl, line_token.value(mem=ctx.mem))
							link_info['is_source'] = ctx.is_destination(target)
							link_info['target'] = target
						elif line_token.type == TokenType.Address:
							target = line_token.value(ctx.mem)
							link_info['is_source'] = ctx.is_destination(target)
							link_info['target'] = target
						else:
							link_info = {}
						yield {
							'type': tts,
							'ivl': line_token.ivl,
							'val': td.value(line_token),
							**link_info
						}

			td = TokenDecoder(ctx.mem, "c64font" if "c64font" in ctx.args.flags else "petscii-ctrl")
			gen = Parser(ctx.mem, ivl).tokens()
			target_already_exits = params['target_already_exits']
			for token in gen:
				if token.type==TokenType.LineLink:
					yield {
						'type': 'line',
						'address': token.ivl.first,
						'tokens': line_tokens(),
						'is_destination': (not target_already_exits) and (ctx.is_destination(token.ivl.first))
					}

		return {
			'type': self.name,
			'lines': lines()
		}
