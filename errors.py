class Dis64Exception(Exception):
	pass

class MemoryException(Dis64Exception):
	def __init__(self, msg, envelope=None, subset=None):
		super().__init__(msg)
		self.envelope = envelope
		self.subset = subset

	def __str__(self):
		bs = super().__str__()
		bs += "\n\tenvelope: {}\n\tsubset  : {}".format(self.envelope, self.subset)
		return bs

class ParserException(Dis64Exception):
	def __init__(self, msg):
		super().__init__(msg)

#TODO: this is on death row!
class UnprocessedData(Dis64Exception):
	def __init__(self, msg, region=None, ivl=None):
		super().__init__(msg)
		self.region = region
		self.ivl = ivl

	def __str__(self):
		bs = super().__str__()
		bs += "\n\tregion: {}\n\tunprocessed  : {}".format(self.region, self.ivl)
		return bs
