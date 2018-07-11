from lark import Lark

if __name__=='__main__':
	with open("MemType.txt", "r") as f:
		t = f.read()

	l = Lark(open("script.lark").read())

	t = l.parse(t)

	print(t.pretty())
