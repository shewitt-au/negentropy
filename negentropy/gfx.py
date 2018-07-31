from enum import Enum, unique, auto

from PIL import Image, ImageFont, ImageDraw

from .interval import Interval
from . import decoders
from . import errors

@unique
class Mode(Enum):
	Standard = auto()
	MCM  = auto()

def mode_standard(ch):
	return Mode.Standard

def mode_mcm(ch):
	return Mode.mode_mcm

class ModeClassifier(object):
	def __init__(self, params):
		self.default = Mode.Standard

		mcm = params.get('mcm')
		standard = params.get('standard')

		if standard is None and mcm is None:
			self.mode = self._mode_always_default
		elif mcm is True:
			self.default = Mode.MCM
			if not standard:
				self.mode = self._mode_always_default
			else:
				self.other = Mode.Standard
				self.others = {o for o in standard}
		else:
			self.default = Mode.Standard
			if not mcm:
				self.mode = self._mode_always_default
			else:
				self.other = Mode.MCM
				self.others = {o for o in mcm}

	def _mode_always_default(self, ch):
		return self.default
	def mode(self, ch):
		return self.other if ch in self.others else self.default

	def __call__(self, ch):
		return self.mode(ch)

class Palette(object):
	def __init__(self, params=None):
		self.palette = params.get('palette')
		self.mcmpalette = params.get('mcmpalette')
		if self.palette is None and self.mcmpalette is None:
			self.palette = [0, 1]
			self.mcmpalette = [0, 2, 3, 9]
		elif self.palette is None:
			self.palette = [self.mcmpalette[0], self.mcmpalette[3]&3]
		elif self.palette is None:
			self.mcmpalette = [self.palette[0], 1, 2, self.palette[1]]

	def std(self):
		return self.palette

	def mcm(self):
		return self.mcmpalette

class CharDecoder(decoders.Prefix):
	def __init__(self, name):
		self.name = name

	def preprocess(self, ctx, ivl):
		ctx.link_add_reachable(ivl.first)
		# return the non-processed part of the interval
		num_chars = len(ivl)//8
		return Interval(ivl.first+8*num_chars, ivl.last)

	def decode(self, ctx, ivl, params):
		mem = ctx.mem.view(ivl)
		num_chars = len(ivl)//8

		mc = ModeClassifier(params)

		palette = Palette(params)
		first_number = params.get('first_number', 0)
		first_char_at = params.get('first_char_at', None)
		if first_char_at is None:
			first_char_at = first_number
		cx, cy = C64Bitmap.calcgridsize(num_chars, first_number, first_char_at)

		def generate():
			fn = "{:04x}.png".format(ivl.first)
			fpath = ctx.file(fn)
			bm = C64Bitmap.genset(
							mem.r8m(ivl.first, len(ivl)),
							palette,
							num_chars,
							mc,
							first_number,
							first_char_at
							);
			bm.save(fpath)
			return fn

		target_already_exits = params['target_already_exits']
		params['first_number'] = (first_char_at+num_chars)&~0xf
		params['first_char_at'] = first_char_at+num_chars

		return {
				'type'   : self.name,
				'address': ivl.first,
				'is_destination' : not target_already_exits and ctx.is_destination(ivl.first),
				'label'  : ctx.syms.lookup(ivl.first).name,
				'generate' : generate
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
	def __init__(self, sz, bgcol=0):
		self.image = Image.new("P", sz, bgcol)
		self.image.putpalette(c64Colours)
		self.pixels = self.image.load()

	@staticmethod
	def calcgridsize(num_chars=256, first_number=0, first_char_at=0):
		num_cells = num_chars+first_char_at-first_number
		cx = num_cells if num_cells<16 else 16
		cy = num_cells//16 + (1 if num_cells%16!=0 else 0)
		return (cx, cy)

	@classmethod
	def genset(cls, data, palette, num_chars=256, mode_fn=mode_standard, first_number=0, first_char_at=0):
		assert (first_char_at>=first_number), "first_char_at too small!"
		cx, cy = C64Bitmap.calcgridsize(num_chars, first_number, first_char_at)
		instance = cls(cls.charset_size(cx, cy))
		instance.charset(data, num_chars, mode_fn, palette, first_number, first_char_at)
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
				if int(v)&0x80:
					self.plotpixel((xx, yy), c, zoom)
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

	def ctext(self, rc, text, c, font, yoff=0):
		draw = ImageDraw.Draw(self.image)
		sz = draw.textsize(text, font=font)

		x = rc[0]+(rc[2]-rc[0]-sz[0])/2
		y = rc[1]+(rc[3]-rc[1]-sz[1]-yoff)/2

		draw.text((x, y), text, font=font, fill=c)

	zoom = 4
	sep = 4
	font_sz = 18
	char_sz = 8*zoom
	cell_sz = char_sz+sep
	@classmethod
	def charset_size(cls, cx, cy):
		return (cls.char_sz+cx*cls.cell_sz, cls.char_sz+cy*cls.cell_sz)

	# first_number: start numbering the cells from this
	# first_char_at: in which cell to place the first character (as numbered above)
	# NOTE: the data always comes from the same place regardless of these two variables!
	def charset(self, data, num_chars, mode_fn, palette, first_number=0, first_char_at=0):
		cx, cy = C64Bitmap.calcgridsize(num_chars, first_number, first_char_at)

		draw = ImageDraw.Draw(self.image)
		font = ImageFont.truetype("arial.ttf", self.font_sz)
		yoff = font.getoffset("M")[1] # yoff is the gap between the top of the 'M' and the cell.

		xbase = first_number%16
		for x in range(0, cx):
			x1 = self.char_sz+x*self.cell_sz
			self.ctext((x1, 0, x1+self.char_sz, self.char_sz), "{:02x}".format(xbase+x), 1, font, yoff)
		ybase = first_number-xbase
		for y in range(0, cy):
			y1 = self.char_sz+y*self.cell_sz
			self.ctext((0, y1, self.char_sz, y1+self.char_sz), "{:02x}".format(ybase+(y<<4)), 1, font, yoff)

		for y in range(0, cy):
			for x in range(0, cx):
				char = x+y*16+first_number-first_char_at
				if char<0:
					continue
				if num_chars == 0:
					break
				num_chars -= 1
				mcm = mode_fn(char+first_number)==Mode.MCM
				if mcm:
					self.setcharmcm(data, char, (self.char_sz+x*self.cell_sz, self.char_sz+y*self.cell_sz), palette.mcm(), self.zoom)
				else:
					self.setchar(data, char, (self.char_sz+x*self.cell_sz, self.char_sz+y*self.cell_sz), palette.std()[1], self.zoom)
				self.grid((self.char_sz+x*self.cell_sz, self.char_sz+y*self.cell_sz), mcm, 11, self.zoom)

if __name__ == '__main__':
	b = C64Bitmap((128, 64), 6)
	with open("chargen", "rb") as f:
		d = f.read()
	for y in range(0, 8):
		for x in range(0, 16):
			b.setchar(d, x+y*16, (x*8, y*8), 14)
	b.save("chars.png")
