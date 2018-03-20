import jinja2
import M6502

_end = None

def setup():
	import symbols
	from interval import Interval
	import memory
	sym = symbols.read_symbols("BD.txt", "BD-BM.txt")
	cmt = symbols.read_comments()
	with open("5000-8fff.bin", "rb") as f:
		f = open("5000-8fff.bin", "rb")
		m = memory.Memory(f.read(), 0x5000)

	d = M6502.Diss(m, sym, cmt)

	global _env
	_env = jinja2.Environment(
			loader=jinja2.PackageLoader(__name__)
		)
	_env.globals['items'] = d.get_items(Interval(0x6c80, 0x6c9a))

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

