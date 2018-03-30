import jinja2
import decoders
import memory

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
	import symbols
	from interval import Interval
	import memory
	sym = symbols.read_symbols("BD.txt", "BD-BM.txt")
	cmt = symbols.read_comments()
	with open("5000-8fff.bin", "rb") as f:
		f = open("5000-8fff.bin", "rb")
		m = memory.Memory(f.read(), 0x5000)
	ctx = decoders.Context(m, sym, cmt)
	decoders.init_decoders(ctx)
	mmap = memory.MemType("MemType.txt")

	global _env
	_env = jinja2.Environment(
			loader=jinja2.PackageLoader(__name__)
		)
	_env.globals['items'] = mmap.decode(ctx, Interval(0x5000, 0x8fff))
	_env.filters['seq2str'] = sequence_to_string

	s = render('hello.html')
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
