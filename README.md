# negentropy

Negentropy is a disassembler for the C64 that I'm working on written in Python. It's the tool used to generate the disassemblies on this site, all of which are unedited output, images and all. It's my first real Python program and is still a work in progress, but nevertheless it's quite useful. The repo can be found [here](https://github.com/shewitt-au/negentropy). Here's a list of some of the features currently implemented:
* Generate HTML pages, complete with images and links.
* Disassemble 6502 machine code.
* List BASIC programs.
* Annotate the generated output with labels and comments provided in configuration files.
* Generate images for character sets.
* Links, including in BASIC programs, machine code programs and even from SYS commands in BASIC to the target code.

In addition to Python's standard library the following packages are used:
* *Jinja2* - used for templates. Currently only HTML is supported (there are other incomplete templates). Checkout its website [here](http://jinja.pocoo.org/)
* *Pillow* - for image generation. It's [website](https://python-pillow.org/)
* *Lark* - for parsing. It's LALR parser is bloody fast (and its author tolerant of stupid questions😊). It's [website](https://github.com/lark-parser/lark)
