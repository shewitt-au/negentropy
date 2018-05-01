import jinja2
import decoders

def sequence_to_string(it, pat, **kwargs):
	sep = kwargs.get("s")
	if sep is None or isinstance(sep, str):
		if sep is None:
			sep = " "
		ret = sep.join([pat.format(i) for i in it])
	else:
		ret = ""
		sep.sort(reverse=True)
		for i in enumerate(it):
			if i[0]!=0:
				for s in sep:
					if i[0]%s[0]==0:
						ret = ret+s[1]
						break
			ret = ret+pat.format(i[1])

	pad = kwargs.get("w")
	if pad:
		ret = ret.ljust(pad)

	return ret

def setup():
	from interval import Interval
	import gfx
	import data
	import M6502

	bd = decoders.BaseDecoder(
				decoders = {
					"bitmap" : gfx.CharDecoder("chars"),
					"data" : data.DataDecoder("data", 1, 16),
					"ptr16" : data.DataDecoder("ptr16", 2, 8),
					"code" : M6502.M6502Decoder("code")
					},
				address = 0x5000,
				memory = "5000-8fff.bin",
				memtype = "MemType.txt",
				symbols = ("BD.txt", "BD-BM.txt"),
				comments = "Comments.txt"
		)

	global _env
	_env = jinja2.Environment(loader=jinja2.PackageLoader(__name__))
	_env.globals['items'] = bd.decode(Interval(0x5000, 0x8fff))
	_env.filters['seq2str'] = sequence_to_string

	s = render('template.html')
	print(s)

	with open("out.html", "w") as of:
		of.write(s)
	import webbrowser
	webbrowser.open("out.html")

def render(template_name, **template_vars):
	template = _env.get_template(template_name)
	return template.render(**template_vars)

if __name__ == '__main__':
	setup()
