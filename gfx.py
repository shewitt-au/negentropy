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
	#
	#  MULTI-COLOR CHARACTER MODE (MCM = 1, BMM = ECM = 0 )
	#
	#    Multi-color mode provides additional color flexibility allowing up to
	#  four colors within each character but with reduced resolution. The multi-
	#  color mode is selected by setting the MCM bit in register 22 ($16) to
	#  "1," which causes the dot data stored in the character base to be
	#  interpreted in a different manner. If the MSB of the color nybble is a
	#  "0," the character will be displayed as described in standard character
	#  mode, allowing the two modes to be inter-mixed (however, only the lower
	#  order 8 colors are available). When the MSB of the color nybble is a "1"
	#  (if MCM:MSB(CM) = 1) the character bits are interpreted in the multi-
	#  color mode:
	#
	#                | CHARACTER  |
	#     FUNCTION   |  BIT PAIR  |               COLOR DISPLAYED
	#  --------------+------------+---------------------------------------------
	#    Background  |     00     |  Background #0 Color
	#                |            |  (register 33 ($21))
	#    Background  |     01     |  Background #1 Color
	#                |            |  (register 34 ($22)
	#    Foreground  |     10     |  Background #2 Color
	#                |            |  (register 35 ($23)
	#    Foreground  |     11     |  Color specified by 3 LSB
	#                |            |  of color nybble
	#
	#  Since two bits are required to specify one dot color, the character is
	#  now displayed as a 4*8 matrix with each dot twice the horizontal size as
	#  in standard mode. Note, however, that each character region can now
	#  contain 4 different colors, two as foreground and two as background (see
	#  MOB priority).
	#
	def setcharmcm(self, x, y, c, d):
		if c[3]&8 == 0:
			self.setchar(x, y, c[3], d)
		else:
			cd = list(c)
			cd[3] = cd[3]&7 # Clear the MCM bit
			it = iter(d)
			for yy in range(y, y+8):
				v = next(it)
				for xx in range(x, x+8, 2):
					pc = cd[(int(v)&0xc0)>>6]
					self.pixels[xx, yy] = pc
					self.pixels[xx+1, yy] = pc
					v = v<<2

	def save(self, fn):
		self.image.save(fn)

if __name__=="__main__":
	bm = C64Bitmap(128, 128)
	bm.setcharmcm(10, 10, [0, 2, 3, 9], [0xff, 0xff, 0xbf, 0x2f, 0x2f, 0x2f, 0xbf, 0xff])
	bm.save("out.png")
