from PIL import Image, ImageFont, ImageDraw
import decoders

class CharDecoder(decoders.Prefix):
	def __init__(self, name):
		self.name = name

	def targets(self, ctx, ivl):
		return set()

	def decode(self, ctx, ivl, first_target, params):
		num_chars = len(ivl)//8
		cx = num_chars if num_chars<16 else 16
		cy = num_chars//16 + (1 if num_chars%16!=0 else 0)
		mcm = params.get("mcm", False)
		pallet = params.get("pallet", 1)
		base_char = params.get("base_char", 0)

		def generate():
			fn = "{:04x}.png".format(ivl.first)
			bm = C64Bitmap.genset(ctx.mem.r8m(ivl.first, len(ivl)), num_chars, mcm, pallet, base_char);
			bm.save(fn)
			return fn

		c = ctx.cmts.get(ivl.first)
		return {
				"type"   : self.name,
				"address": ivl.first,
				"is_destination" : first_target and ivl.first in ctx.targets,
				"label"  : ctx.syms.get(ivl.first),
				"comment_before" : None if c is None else c[0],
				"comment_after"  : None if c is None else c[1],
				"comment_inline" : None if c is None else c[2],
				"generate" : generate
				}

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
	def __init__(self, sz):
		self.image = Image.new("P", sz, 0)
		self.image.putpalette(c64Colours)
		self.pixels = self.image.load()

	@classmethod
	def genset(cls, data, num_chars=256, mcm=False, pallet=1, base_char=0):
		cx = num_chars if num_chars<16 else 16
		cy = num_chars//16 + (1 if num_chars%16!=0 else 0)
		instance = cls(cls.charset_size(cx, cy))
		instance.charset(data, num_chars, mcm, pallet, base_char)
		return instance

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
					self.plotpixel((xx+zoom, yy), pc, zoom)
					v = v<<2

	def save(self, fn):
		self.image.save(fn)

	def grid(self, pos, mcm, c, zoom):
		off = 8*zoom

		draw = ImageDraw.Draw(self.image)
		if mcm:
			for i in range(0, 9):
				draw.line((pos[0], pos[1]+i*zoom, pos[0]+off, pos[1]+i*zoom), fill=c)
			for i in range(0, 9, 2):
				draw.line((pos[0]+i*zoom, pos[1], pos[0]+i*zoom, pos[1]+off), fill=c)
		else:
			for i in range(0, 9):
				draw.line((pos[0], pos[1]+i*zoom, pos[0]+off, pos[1]+i*zoom), fill=c)
				draw.line((pos[0]+i*zoom, pos[1], pos[0]+i*zoom, pos[1]+off), fill=c)

	def ctext(self, rc, text, c, font):
		draw = ImageDraw.Draw(self.image)
		sz = draw.textsize(text, font=font)

		x = rc[0]+(rc[2]-rc[0]-sz[0])/2
		y = rc[1]+(rc[3]-rc[1]-sz[1])/2

		draw.text((x, y), text, font=font, fill=c)

	zoom = 4
	sep = 4
	font_sz = 18
	char_sz = 8*zoom
	cell_sz = char_sz+sep
	@classmethod
	def charset_size(cls, cx, cy):
		return (cls.char_sz+cx*cls.cell_sz, cls.char_sz+cy*cls.cell_sz)

	def charset(self, data, num_chars, mcm, pallet, base_char=0):
		cx = num_chars if num_chars<16 else 16
		cy = num_chars//16 + (1 if num_chars%16!=0 else 0)

		draw = ImageDraw.Draw(self.image)
		font = ImageFont.truetype("arial.ttf", self.font_sz)

		# We don't and to count the descenders when centering. Compensating
		# for the horizontal numbers makes them look worse, so we just do
		# the vertical ones. I'm not sure if all PILLOW's font classes provide
		# 'getmetrics' so fail gracefully if this one doesn't.
		try:
			ascent, descent = font.getmetrics()
		except AttributeError:
			descent = 0

		xbase = base_char%16
		for x in range(0, cx):
			self.ctext((self.char_sz+x*self.cell_sz, 0, self.char_sz+(x+1)*self.cell_sz, self.char_sz), "{:02x}".format(xbase+x), 1, font)
		ybase = base_char-xbase
		for y in range(0, cy):
			self.ctext((0, self.char_sz+y*self.cell_sz-descent, self.char_sz, self.char_sz+(y+1)*self.cell_sz-descent), "{:02x}".format(ybase+(y<<4)), 1, font)

		for y in range(0, cy):
			for x in range(0, cx):
				if num_chars == 0:
					break
				num_chars = num_chars-1
				if mcm:
					self.setcharmcm(data, x+y*16, (self.char_sz+x*self.cell_sz, self.char_sz+y*self.cell_sz), pallet, self.zoom)
				else:
					self.setchar(data, x+y*16, (self.char_sz+x*self.cell_sz, self.char_sz+y*self.cell_sz), pallet, self.zoom)
				self.grid((self.char_sz+x*self.cell_sz, self.char_sz+y*self.cell_sz), mcm, 11, self.zoom)
