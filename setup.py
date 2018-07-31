from setuptools import setup

setup(name='negentropy',
      version='0.1',
      description='C64 disassembler',
      url='https://github.com/shewitt-au/negentropy',
      author='Stephen Hewitt',
      author_email='retrointernals@gmail.com',
      license='MIT',
      packages=['negentropy'],
      install_requires=['jinja2', 'pillow', 'lark'],
      include_package_data=True,
      zip_safe=False)
