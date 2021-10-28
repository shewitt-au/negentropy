import bisect
import numbers

from . import multiindex
from .interval import Interval
from .multidict import multidict
from .errors import *

class DictWithRange(multiindex.MultiIndex):
    def __init__(self):
        super().__init__()
        self.add_index("by_address", multidict, multiindex.dict_indexer, (lambda k: k[0]))
        self.add_index("sorted_address", list, multiindex.sorted_list_indexer, (lambda k: k[0]))

    def items_in_range(self, ivl):
        b = bisect.bisect_left(self.sorted_address, self.sorted_address_compare(ivl.first))
        e = bisect.bisect_right(self.sorted_address, self.sorted_address_compare(ivl.last), b)
        for i in range(b, e):
            yield self.sorted_address[i]

    def keys_in_range(self, ivl):
        for v in self.items_in_range(ivl):
            yield v[0]

    def values_in_range(self, ivl):
        for v in self.items_in_range(ivl):
            yield v[1]

class CommentInfo(object):
    def __init__(self, before="", after=""):
        self.before = before
        self.after = after

    def __repr__(self):
        return "CommentInfo(before='{}', after='{}')".format(self.before, self.after)

class Comments(object):
    def __init__(self):
        self.main = DictWithRange()
        self.inline = DictWithRange()

    def get(self, addr):
        ent = self.main.by_address.get(addr)
        return ent[1] if ent is not None else None

    def get_inline(self, addr):
        return self.inline.by_address.get(addr)

    def add_before(self, addr, txt):
        cmt = self.main.by_address.get(addr)
        if cmt is None:
            self.main.add((addr, CommentInfo(before=txt)))
        else:
            cmt[1].before += txt

    def add_after(self, addr, txt):
        cmt = self.main.by_address.get(addr)
        if cmt is None:
            self.main.add((addr, CommentInfo(after=txt)))
        else:
            cmt[1].after += txt

    def add_inline(self, addr, txt):
        cmt = self.inline.by_address.get(addr)
        if cmt is None:
            self.inline.add((addr, txt))
        else:
            cmt = (addr, txt)

    def cuts(self, ivl):
        return self.main.keys_in_range(ivl)

def format_op_adjust(adj):
    sgn = '+' if adj>=0 else '-'
    return '{}${:x}'.format(sgn, abs(adj)) if abs(adj)>=9 else '{}{}'.format(sgn, abs(adj))

class SymInfo(object):
    def __init__(self, name, addr, op_adjust):
        self.name = name
        self.addr = addr
        self.op_adjust = op_adjust

    def op_adjust_str(self):
        return format_op_adjust(self.op_adjust)

    def __repr__(self):
        return "SymInfo('{}', ${:04x}, {:+})".format(self.name, self.addr, self.op_adjust)

class SymbolTable(multiindex.MultiIndex):
    def __init__(self):
        super().__init__()
        self.add_index("sorted_address", list, multiindex.sorted_list_indexer, (lambda k: k[0])) # list sorted by address
        self.add_index("sorted_name", list, multiindex.sorted_list_indexer, (lambda k: k[1])) # list sorted by name
        self.add_index("by_name", multidict, multiindex.dict_indexer, (lambda k: k[1])) # dict of names
        self.black_list = None

    def out_of_range(self, ivl):
        b = bisect.bisect_left(self.sorted_address, self.sorted_address_compare(0))
        e = bisect.bisect_left(self.sorted_address, self.sorted_address_compare(ivl.first), b)
        for i in range(b, e):
            yield self.sorted_address[i]
        b = bisect.bisect_right(self.sorted_address, self.sorted_address_compare(ivl.last), e)
        for i in range(b, len(self.sorted_address)):
            yield self.sorted_address[i]

    def parse_add(self, ctx, ivl, name, in_index):
        ctx.have_indexables |= in_index
        self.add((ivl, name, in_index))

    def items_in_range(self, ivl):
        b = bisect.bisect_left(self.sorted_address, self.sorted_address_compare(ivl.first))
        e = bisect.bisect_right(self.sorted_address, self.sorted_address_compare(ivl.last), b)
        for i in range(b, e):
            yield self.sorted_address[i]

    def left_edges(self, ivl):
        for v in self.items_in_range(ivl):
            yield v[0].first

    def values_in_range(self, ivl):
        for v in self.items_in_range(ivl):
            yield v[1]

    def get_entry(self, addr):
        i = bisect.bisect_left(self.sorted_address, self.sorted_address_compare(addr))
        if i==len(self.sorted_address):
            return None
        ent = self.sorted_address[i]
        if not ent[0].contains(addr) or (self.black_list is not None and addr in self.black_list):
            return None
        return ent

    def lookup(self, addr, name_unknowns=True):
        e = self.get_entry(addr)
        if e is None:
            return SymInfo("${:04x}".format(addr) if name_unknowns else None, addr, 0)
        op_adjust = addr-e[0].first
        return SymInfo(e[1], e[0].first, op_adjust)

    def lookup_byname(self, name):
        s = self.by_name.get(name)
        if s:
            s = SymInfo(s[1], s[0].first, 0)
        return s

    def clashes(self):
        clashes = 0
        it = iter(self.sorted_address)
        try:
            ps = next(it)
        except StopIteration:
            pass
        else:
            for s in it:
                if not (ps[0]&s[0]).is_empty():
                    print("Symbol clash:\n\t{} @ {}\n\t{} @ {}".format(ps[1], ps[0], s[1], s[0]))
                    clashes += 1
                    if clashes==7:
                        print("***Stopping clash search***\n")
                        break
                ps = s

        return clashes!=0

class DirectiveInfo(object):
    def __init__(self, address, command, oaddress, osymbol):
        self.address = address
        self.command = command
        self.oaddress = oaddress # one or the other of these two
        self.osymbol = osymbol

    def resolve_syms(self, ctx):
        if self.osymbol:
            assert self.oaddress is None, "one or the other of 'oaddress' and 'osymbol'"
            sym_ent = ctx.syms.lookup_byname(self.osymbol)
            if sym_ent is None:
                raise Dis64Exception("Directive: '{}' symbol not found".format(self.osymbol))
            self.osymbol = sym_ent
            self.oaddress = sym_ent.addr
        else:
            assert self.oaddress is not None, "one or the other of 'oaddress' and 'osymbol'"
            self.osymbol = ctx.syms.lookup(self.oaddress)
        ctx.link_add_referenced(self.oaddress)

    def operand(self, ctx, oper):
        o = Operand(ctx)

        if 'r' in self.command:
            offset = oper-self.oaddress
            o.post(self.osymbol.name, self.osymbol.addr)
            if offset:
                o.post(format_op_adjust(offset))
        #TODO: handle a combination of these 
        if '<' in self.command:
            if oper != self.osymbol.addr&0x00ff:
                raise Dis64Exception("Directive: unexpected low byte")
            else:
                o.post("<")
                o.post(self.osymbol.name, self.osymbol.addr)
                if self.osymbol.op_adjust:
                    o.post(self.osymbol.op_adjust_str())
        elif '>' in self.command:
            if oper != self.osymbol.addr>>8:
                raise Dis64Exception("Directive: unexpected high byte")
            else:
                o.post(">")
                o.post(self.osymbol.name, self.osymbol.addr)
                if self.osymbol.op_adjust:
                    o.post(self.osymbol.op_adjust_str())

        return o

    def __eq__(self, other):
        if isinstance(other, numbers.Number):
            return self.address==other
        else:
            return self.address==other.address
    def __ne__(self, other):
        if isinstance(other, numbers.Number):
            return self.address!=other
        else:
            return self.address!=other.address
    def __lt__(self, other):
        if isinstance(other, numbers.Number):
            return self.address<other
        else:
            return self.address<other.address
    def __le__(self, other):
        if isinstance(other, numbers.Number):
            return self.address<=other
        else:
            return self.address<=other.address
    def __gt__(self, other):
        if isinstance(other, numbers.Number):
            return self.address>other
        else:
            return self.address>other.address
    def __ge__(self, other):
        if isinstance(other, numbers.Number):
            return self.address>=other
        else:
            return self.address>=other.address

    def __repr__(self):
        return "DirectiveInfo(${:04x}, {}, {}, ${:04x})".format(
            self.address,
            self.command,
            self.osymbol,
            self.oaddress
            )

class Directives(object):
    def parse_begin(self):
        self.dlist = []

    def parse_add(self, address, command, oaddress, osymbol):
        self.dlist.append(DirectiveInfo(address, command, oaddress, osymbol))

    def parse_end(self, ctx):
        for d in self.dlist:
            d.resolve_syms(ctx)
        self.dlist.sort()

    def reset(self, address):
        self.pos = bisect.bisect_left(self.dlist, address)

    def lookup(self, address):
        while self.pos<len(self.dlist):
            v = self.dlist[self.pos]
            if v==address:
                self.pos += 1
                return v
            elif v>address:
                return None
            else:
                self.pos += 1
        return None

class OperandPart(object):
    def __init__(self, s, l=None):
        self.s = s
        self.l = l

    def gettext(self):
        return self.s
    def settext(self, value):
        self.s = value
    text = property(gettext, settext)

    def getlink(self):
        return self.l
    def setlink(self, value):
        self.l = value
    link = property(getlink, setlink)

    def __str__(self):
        return self.s

class Operand(object):
    def __init__(self, ctx):
        self.ctx = ctx
        self.parts = []

    def pre(self, s, l=None):
        l = self.process_link(l)
        self.parts.insert(0, OperandPart(s, l))

    def post(self, s, l=None):
        l = self.process_link(l)
        self.parts.append(OperandPart(s, l))

    def process_link(self, l):
        if l:
            return "{:04x}".format(l) if self.ctx.is_destination(l) else None
        else:
            None

    def __iter__(self):
        return iter(self.parts)
    def __getitem__(self, k):
        return self.parts[k]
    def __len__(self):
        return len(self.parts)

    def __str__(self):
        return "".join([str(s) for s in self.parts])
