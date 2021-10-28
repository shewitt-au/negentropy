import webbrowser
import datetime
import os
import glob

import jinja2

from . import errors
from . import decoders
from . import gfx
from . import data
from . import M6502decoder
from . import index
from . import cbmbasicdecoder
from . import dontcaredecoder

class TemplateMgr(object):
    def __init__(self, ctx, name):
        self.name = name
        self.source = ctx.sourcedir
        self.templates = ctx.source_file("templates")
        self.templatefiles = os.path.join(self.templates, self.name)

    def template(self):
        l = glob.glob(os.path.join(self.templatefiles, "template.*"))
        if len(l)==0:
            raise errors.Dis64Exception("'{}' template not found".format(self.name))
        elif len(l)>1:
            raise errors.Dis64Exception("Too many candidates for '{}' template".format(self.name))
        return os.path.relpath(l[0], start=self.templates).replace("\\", "/")
            # https://github.com/pallets/jinja/issues/767 ---/\

    def script(self):
        s = os.path.join(self.templatefiles, "script.txt")
        return s if os.path.exists(s) else None

def render(env, template_name, **template_vars):
    template = env.get_template(template_name)
    return template.render(**template_vars)

def add_dispatcher(env, filter_name, markup):
    @jinja2.contextfilter
    def dispatch(context, tag, *args, **kwargs):
        return context.vars[markup.format(tag)](*args, **kwargs)
    env.filters[filter_name] = dispatch

_mdescape = {
    '\\' :  '\\\\',
    '`'  :  '\\`',
    '*'  :  '\\*',
    '_'  :  '\\_',
    '{' :  '\\{',
    '[' :  '\\[',
    '(' :  '\\(',
    '}' :  '\\}',
    ']' :  '\\]',
    ')' :  '\\)',
    '#'  :  '\\#',
    '+'  :  '\\+',
    '-'  :  '\\-',
    '.'  :  '\\.',
    '!'  :  '\\!'
    }
_bdecsapetrans = str.maketrans(_mdescape)
def mdescape(s, *args, **kwargs):
    return s.translate(_bdecsapetrans)

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

def hexnum(n):
    if n<0x100:
        return "${:02x}".format(n)
    else:
        return "${:04x}".format(n)

def run(args):
    ctx = decoders.Context(
                args,
                decoders = {
                    "bitmap" : gfx.CharDecoder("chars"),
                    "data" : data.BytesDecoder("data", 16),
                    "ptr16" : data.PointerDecoder("ptr16", 4), # TODO: Rename to ptrtable or something
                    "code" : M6502decoder.M6502Decoder("code"),
                    "basic" : cbmbasicdecoder.BasicDecoder("basic"),
                    "dontcare" : dontcaredecoder.DontCareDecoder("dontcare")
                    }
                )
    ctx.preprocess()

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(ctx.template_mgr.templates))
    env.globals['title'] = args.title
    if args.builton:
        env.globals['builton'] = datetime.datetime.now().astimezone().isoformat(sep=' ', timespec='seconds')
    env.globals['items'] = ctx.items()
    env.globals['has_index'] = index.has_index(ctx)
    env.globals['index'] = index.get_index(ctx)
    env.globals['have_holes'] = ctx.holes>0
    env.globals['flags'] = args.flags
    env.filters['seq2str'] = sequence_to_string
    env.filters['mdescape'] = mdescape
    env.filters['hexnum'] = hexnum
    add_dispatcher(env, "dispatch", "{}_handler")
    add_dispatcher(env, "cbmbasic_dispatch", "cbmbasic_{}_handler")

    s = render(env, ctx.template_mgr.template())
    with open(args.output, "w", encoding='utf-8') as of:
        if args.prefix:
            with open(args.prefix, "r") as pf:
                of.write(pf.read())
        of.write(s)

    if args.webbrowser:
        webbrowser.open(args.output)
