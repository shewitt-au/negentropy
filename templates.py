import jinja2
import webbrowser
import decoders
import gfx
import data
import M6502
import index

def render(env, template_name, **template_vars):
	template = env.get_template(template_name)
	return template.render(**template_vars)

@jinja2.contextfilter
def dispatch(context, macro_name, *args, **kwargs):
	return context.vars[macro_name+'_handler'](*args, **kwargs)

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

def next_item(coll):
	i = iter(coll)
	return next(i)

def run(args):
	bd = decoders.Context(
				decoders = {
					"bitmap" : gfx.CharDecoder("chars"),
					"data" : data.BytesDecoder("data", 16),
					"ptr16" : data.PointerDecoder("ptr16", 4),
					"code" : M6502.M6502Decoder("code")
					},
				default_decoder = args.defaultdecoder,
				address = args.origin,
				memory = args.input,
				memtype = args.memtype,
				symbols = ("BD.txt", "BD-BM.txt"),
				comments = "Comments.txt"
		)

	env = jinja2.Environment(loader=jinja2.PackageLoader(__name__))
	env.globals['title'] ="Boulder Dash Disassembly"
	env.globals['items'] = bd.items()
	env.globals['next_item'] = next_item
	env.globals['index'] = index.get_index(bd)
	env.filters['seq2str'] = sequence_to_string
	env.filters['dispatch'] = dispatch

	s = render(env, 'template.html')
	with open(args.output, "w") as of:
		of.write(s)

	if args.webbrowser:
		webbrowser.open(args.output)
