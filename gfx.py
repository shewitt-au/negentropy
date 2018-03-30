from PIL import Image

c64Colours = (
	0x00, 0x00, 0x00, #  0 - Black
	0xff, 0xff, 0xff, #  1 - White
	0x89, 0x40, 0x36, #  2 - Red 
	0x7a, 0xbf, 0xc7, #  3 - Cyan
	0x8a, 0x46, 0xae, #  4 - Purple
	0x68, 0xa9, 0x41, #  5 - Green
	0x3e, 0x31, 0xa2, #  6 - Blue
	0xd0, 0xdc, 0x71, #  7 - Yellow
	0x90, 0x5f, 0x25, #  8 - Orange
	0x5c, 0x47, 0x00, #  9 - Brown
	0xbb, 0x77, 0x6d, # 10 - Light red
	0x55, 0x55, 0x55, # 11 - Dark grey
	0x80, 0x80, 0x80, # 12 - Grey
	0xac, 0xea, 0xa8, # 13 - Light green
	0x7c, 0x70, 0xda, # 14 - Light blue
	0xab, 0xab, 0xab  # 15 - Light grey
	)

class C64Bitmap(object):
	def __init__(self, w, h):
		self.image = Image.new("P", (w, h), 0)
		self.image.putpalette(c64Colours)
		self.pixels = self.image.load()

	def setchar(self, x, y, c, d):
		it = iter(d)
		for yy in range(y, y+8):
			v = next(it)
			for xx in range(x, x+8):
				self.pixels[xx, yy] = c if int(v)&0x80 else 0
				v = v<<1

	def setcharmcm(self, x, y, c, d):
		it = iter(d)
		for yy in range(y, y+8):
			v = next(it)
			for xx in range(x, x+8, 2):
				pc = c[(int(v)&0xc0)>>6]
				self.pixels[xx, yy] = pc
				self.pixels[xx+1, yy] = pc
				v = v<<2

	def save(self, fn):
		self.image.save(fn)

if __name__=="__main__":
	bm = C64Bitmap(128, 128)
	bm.setcharmcm(10, 10, [0, 1, 2, 3], [0xff, 0xff, 0xbf, 0x2f, 0x2f, 0x2f, 0xbf, 0xff])
	bm.save("out.png")
