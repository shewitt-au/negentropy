import jinja2
import webbrowser
import decoders
import gfx
import data
import M6502decoder
import index
import cbmbasicdecoder

def render(env, template_name, **template_vars):
	template = env.get_template(template_name)
	return template.render(**template_vars)

def add_dispatcher(env, filter_name, markup):
	@jinja2.contextfilter
	def dispatch(context, tag, *args, **kwargs):
		return context.vars[markup.format(tag)](*args, **kwargs)
	env.filters[filter_name] = dispatch

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

def run(args):
	bd = decoders.Context(
				decoders = {
					"bitmap" : gfx.CharDecoder("chars"),
					"data" : data.BytesDecoder("data", 16),
					"ptr16" : data.PointerDecoder("ptr16", 4),
					"code" : M6502decoder.M6502Decoder("code"),
					"basic" : cbmbasicdecoder.BasicDecoder("basic")
					},
				default_decoder = args.defaultdecoder,
				address = args.origin,
				memory = args.input,
				memtype = args.memtype,
				symbols = args.labels,
				comments = args.comments
		)
	bd.preprocess()

	env = jinja2.Environment(loader=jinja2.PackageLoader(__name__))
	env.globals['title'] = args.title
	env.globals['items'] = bd.items()
	env.globals['index'] = index.get_index(bd)
	env.globals['have_holes'] = bd.holes>0 
	env.filters['seq2str'] = sequence_to_string
	add_dispatcher(env, "dispatch", "{}_handler")
	add_dispatcher(env, "cbmbasic_dispatch", "cbmbasic_{}_handler")

	s = render(env, 'template.html')
	with open(args.output, "w", encoding='utf-8') as of:
		of.write(s)

	if args.webbrowser:
		webbrowser.open(args.output)
