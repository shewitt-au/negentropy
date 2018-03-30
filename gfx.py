from PIL import Image, ImageFont, ImageDraw

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

	def plotpixel(self, pos, c, zoom=8):
		if zoom==1:
			self.pixels[pos[0], pos[1]] = c
		else:
			draw = ImageDraw.Draw(self.image)
			draw.rectangle([pos[0], pos[1], pos[0]+zoom, pos[1]+zoom], fill=c, outline=c)

	def setchar(self, data, ch, pos, c, zoom=1):
		it = iter(data[ch*8:])
		for yy in range(pos[1], pos[1]+8*zoom, zoom):
			v = next(it)
			for xx in range(pos[0], pos[0]+8*zoom, zoom):
				self.plotpixel((xx, yy), (c if int(v)&0x80 else 0), zoom)
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
	def setcharmcm(self, data, ch, pos, c, zoom=1):
		if c[3]&8 == 0:
			self.setchar(data, ch, pos, c[3], zoom)
		else:
			cd = list(c)
			cd[3] = cd[3]&7 # Clear the MCM bit
			it = iter(data[ch*8:])
			for yy in range(pos[1], pos[1]+8*zoom, zoom):
				v = next(it)
				for xx in range(pos[0], pos[0]+8*zoom, 2*zoom):
					pc = cd[(int(v)&0xc0)>>6]
					self.plotpixel((xx, yy), pc, zoom)
					if zoom==1:
						self.plotpixel((xx+1, yy), pc, zoom)
					v = v<<2

	def save(self, fn):
		self.image.save(fn)

	def grid(self, pos, c, zoom):
		off = 8*zoom

		draw = ImageDraw.Draw(self.image)
		for i in range(0, 9):
			draw.line((pos[0], pos[1]+i*zoom, pos[0]+off, pos[1]+i*zoom), fill=c)
			draw.line((pos[0]+i*zoom, pos[1], pos[0]+i*zoom, pos[1]+off), fill=c)

	def charset(self, data, c):
		zoom = 8
		char_sz = 8*zoom
		sep = 8
		cell_sz = char_sz+sep

		draw = ImageDraw.Draw(self.image)
		font = ImageFont.truetype("arial.ttf", 36)

		for x in range(0, 16):
			draw.text((char_sz+x*cell_sz, 0), "{:02x}".format(x), fill=1, font=font)
		for y in range(0, 16):
			draw.text((0, char_sz+y*cell_sz), "{:02x}".format(y<<4), fill=1, font=font)

		for y in range(0, 16):
			for x in range(0, 16):
				bm.setchar(data, x+y*16, (char_sz+x*cell_sz, char_sz+y*cell_sz), c, zoom)
				self.grid((char_sz+x*cell_sz, char_sz+y*cell_sz), 11, zoom)

if __name__=="__main__":
	with open("chargen", "rb") as f:
		chars = f.read();
	bm = C64Bitmap(1280, 1280)
	#for y in range(0, 16):
	#	for x in range(0, 16):
	#		bm.setcharmcm(chars, y*16+x, (x*8, y*8), (0,2,3,9))
	bm.charset(chars, 1)
	bm.save("out.png")
