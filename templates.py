import jinja2

def get_name():
	return "Stephen"

nums = [3, 1, 4, 1, 5, 9]

_env = jinja2.Environment(
		loader=jinja2.PackageLoader(__name__)
	)
_env.globals['name'] = get_name
_env.globals['nums'] = nums

def render(template_name, **template_vars):
	template = _env.get_template(template_name)
	return template.render(**template_vars)

if __name__ == '__main__':
	s = render('hello.html')
	print(s)
