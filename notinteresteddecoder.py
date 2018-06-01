import decoders
from interval import Interval

class NotInterestedDecoder(decoders.Prefix):
	def __init__(self, name):
		self.name = name

	def preprocess(self, ctx, ivl):
		return Interval()

	def decode(self, ctx, ivl, params):
		return {
				'type': self.name,
				'ivl': ivl
				}
