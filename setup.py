from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='negentropy',
      version='0.1',
      description='C64 disassembler',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Disassemblers',
        'Topic :: Utilities'
      ],
      keywords='C64 disassembler 6502 6510',
      url='https://github.com/shewitt-au/negentropy',
      author='Stephen Hewitt',
      author_email='retrointernals@gmail.com',
      license='MIT',
      packages=['negentropy'],
      install_requires=['jinja2', 'pillow', 'lark'],
      entry_points={
          'console_scripts': ['negentropy=negentropy.negentropy:main'],
      },
      include_package_data=True,
      zip_safe=False)
