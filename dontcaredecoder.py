import decoders
from interval import Interval

class DontCareDecoder(decoders.Prefix):
	def __init__(self, name):
		self.name = name

	def preprocess(self, ctx, ivl):
		return Interval()

	def decode(self, ctx, ivl, params):
		title = params.get('title', "Don't care")
		return {
				'type': self.name,
				'title': title,
				'ivl': ivl
				}
