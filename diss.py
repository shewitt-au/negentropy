#!/usr/bin/env python3

from enum import Enum, unique, auto

@unique
class AddrMode(Enum):
	Implied = auto()
	Accumulator = auto()
	Immediate = auto()
	ZeroPage = auto()
	ZeroPageX = auto()
	ZeroPageY = auto()
	Absolute = auto()
	AbsoluteX = auto()
	AbsoluteY = auto()
	AbsIndirect = auto()
	IndirectX = auto()
	IndirectY = auto()
	Relative = auto()

modes = {
	AddrMode.Implied		: (0, ""),
	AddrMode.Accumulator	: (0, "A"),
	AddrMode.Immediate		: (1, "#{}"),
	AddrMode.ZeroPageX		: (1, "{},X"),
	AddrMode.ZeroPageY		: (1, "{},Y"),
	AddrMode.Absolute		: (2, "{}"),
	AddrMode.AbsoluteX		: (2, "{},X"),
	AddrMode.AbsoluteY		: (2, "{},Y"),
	AddrMode.AbsIndirect	: (2, "({})"),
	AddrMode.IndirectX		: (1, "({},X)"),
	AddrMode.IndirectY		: (1, "({}),Y"),
	AddrMode.Relative		: (1, "{}")
	}

menumonics = [
	("BRK",   AddrMode.Implied),		#$00
	("ORA",   AddrMode.IndirectX),		#$01
	("JAM",   AddrMode.Implied),		#$02
	("SLO",   AddrMode.IndirectX),		#$03
	("NOOP",  AddrMode.ZeroPage),		#$04
	("ORA",   AddrMode.ZeroPage),		#$05
	("ASL",   AddrMode.ZeroPage),		#$06
	("SLO",   AddrMode.ZeroPage),		#$07
	("PHP",   AddrMode.Implied),		#$08
	("ORA",   AddrMode.Immediate),		#$09
	("ASL",   AddrMode.Accumulator),	#$0a
	("ANC",   AddrMode.Immediate),		#$0b
	("NOOP",  AddrMode.Absolute),		#$0c
	("ORA",   AddrMode.Absolute),		#$0d
	("ASL",   AddrMode.Absolute),		#$0e
	("SLO",   AddrMode.Absolute),		#$0f
	("BPL",   AddrMode.Relative),		#$10
	("ORA",   AddrMode.IndirectY),		#$11
	("JAM",   AddrMode.Implied),		#$12
	("SLO",   AddrMode.IndirectY),		#$13
	("NOOP",  AddrMode.ZeroPageX),		#$14
	("ORA",   AddrMode.ZeroPageX),		#$15
	("ASL",   AddrMode.ZeroPageX),		#$16
	("SLO",   AddrMode.ZeroPageX),		#$17
	("CLC",   AddrMode.Implied),		#$18
	("ORA",   AddrMode.AbsoluteY),		#$19
	("NOOP",  AddrMode.Implied),		#$1a
	("SLO",   AddrMode.AbsoluteY),		#$1b
	("NOOP",  AddrMode.AbsoluteX),		#$1c
	("ORA",   AddrMode.AbsoluteX),		#$1d
	("ASL",   AddrMode.AbsoluteX),		#$1e
	("SLO",   AddrMode.AbsoluteX),		#$1f
	("JSR",   AddrMode.Absolute),		#$20
	("AND",   AddrMode.IndirectX),		#$21
	("JAM",   AddrMode.Implied),		#$22
	("RLA",   AddrMode.IndirectX),		#$23
	("BIT",   AddrMode.ZeroPage),		#$24
	("AND",   AddrMode.ZeroPage),		#$25
	("ROL",   AddrMode.ZeroPage),		#$26
	("RLA",   AddrMode.ZeroPage),		#$27
	("PLP",   AddrMode.Implied),		#$28
	("AND",   AddrMode.Immediate),		#$29
	("ROL",   AddrMode.Accumulator),	#$2a
	("ANC",   AddrMode.Immediate),		#$2b
	("BIT",   AddrMode.Absolute),		#$2c
	("AND",   AddrMode.Absolute),		#$2d
	("ROL",   AddrMode.Absolute),		#$2e
	("RLA",   AddrMode.Absolute),		#$2f
	("BMI",   AddrMode.Relative),		#$30
	("AND",   AddrMode.IndirectY),		#$31
	("JAM",   AddrMode.Implied),		#$32
	("RLA",   AddrMode.IndirectY),		#$33
	("NOOP",  AddrMode.ZeroPageX),		#$34
	("AND",   AddrMode.ZeroPageX),		#$35
	("ROL",   AddrMode.ZeroPageX),		#$36
	("RLA",   AddrMode.ZeroPageX),		#$37
	("SEC",   AddrMode.Implied),		#$38
	("AND",   AddrMode.AbsoluteY),		#$39
	("NOOP",  AddrMode.Implied),		#$3a
	("RLA",   AddrMode.AbsoluteY),		#$3b
	("NOOP",  AddrMode.AbsoluteX),		#$3c
	("AND",   AddrMode.AbsoluteX),		#$3d
	("ROL",   AddrMode.AbsoluteX),		#$3e
	("RLA",   AddrMode.AbsoluteX),		#$3f
	("RTI",   AddrMode.Implied),		#$40
	("EOR",   AddrMode.IndirectX),		#$41
	("JAM",   AddrMode.Implied),		#$42
	("SRE",   AddrMode.IndirectX),		#$43
	("NOOP",  AddrMode.ZeroPage),		#$44
	("EOR",   AddrMode.ZeroPage),		#$45
	("LSR",   AddrMode.ZeroPage),		#$46
	("SRE",   AddrMode.ZeroPage),		#$47
	("PHA",   AddrMode.Implied),		#$48
	("EOR",   AddrMode.Immediate),		#$49
	("LSR",   AddrMode.Accumulator),	#$4a
	("ASR",   AddrMode.Immediate),		#$4b
	("JMP",   AddrMode.Absolute),		#$4c
	("EOR",   AddrMode.Absolute),		#$4d
	("LSR",   AddrMode.Absolute),		#$4e
	("SRE",   AddrMode.Absolute),		#$4f
	("BVC",   AddrMode.Relative),		#$50
	("EOR",   AddrMode.IndirectY),		#$51
	("JAM",   AddrMode.Implied),		#$52
	("SRE",   AddrMode.IndirectY),		#$53
	("NOOP",  AddrMode.ZeroPageX),		#$54
	("EOR",   AddrMode.ZeroPageX),		#$55
	("LSR",   AddrMode.ZeroPageX),		#$56
	("SRE",   AddrMode.ZeroPageX),		#$57
	("CLI",   AddrMode.Implied),		#$58
	("EOR",   AddrMode.AbsoluteY),		#$59
	("NOOP",  AddrMode.Implied),		#$5a
	("SRE",   AddrMode.AbsoluteY),		#$5b
	("NOOP",  AddrMode.AbsoluteX),		#$5c
	("EOR",   AddrMode.AbsoluteX),		#$5d
	("LSR",   AddrMode.AbsoluteX),		#$5e
	("SRE",   AddrMode.AbsoluteX),		#$5f
	("RTS",   AddrMode.Implied),		#$60
	("ADC",   AddrMode.IndirectX),		#$61
	("JAM",   AddrMode.Implied),		#$62
	("RRA",   AddrMode.IndirectX),		#$63
	("NOOP",  AddrMode.ZeroPage),		#$64
	("ADC",   AddrMode.ZeroPage),		#$65
	("ROR",   AddrMode.ZeroPage),		#$66
	("RRA",   AddrMode.ZeroPage),		#$67
	("PLA",   AddrMode.Implied),		#$68
	("ADC",   AddrMode.Immediate),		#$69
	("ROR",   AddrMode.Accumulator),	#$6a
	("ARR",   AddrMode.Immediate),		#$6b
	("JMP",   AddrMode.AbsIndirect),	#$6c
	("ADC",   AddrMode.Absolute),		#$6d
	("ROR",   AddrMode.Absolute),		#$6e
	("RRA",   AddrMode.Absolute),		#$6f
	("BVS",   AddrMode.Relative),		#$70
	("ADC",   AddrMode.IndirectY),		#$71
	("JAM",   AddrMode.Implied),		#$72
	("RRA",   AddrMode.IndirectY),		#$73
	("NOOP",  AddrMode.ZeroPageX),		#$74
	("ADC",   AddrMode.ZeroPageX),		#$75
	("ROR",   AddrMode.ZeroPageX),		#$76
	("RRA",   AddrMode.ZeroPageX),		#$77
	("SEI",   AddrMode.Implied),		#$78
	("ADC",   AddrMode.AbsoluteY),		#$79
	("NOOP",  AddrMode.Implied),		#$7a
	("RRA",   AddrMode.AbsoluteY),		#$7b
	("NOOP",  AddrMode.AbsoluteX),		#$7c
	("ADC",   AddrMode.AbsoluteX),		#$7d
	("ROR",   AddrMode.AbsoluteX),		#$7e
	("RRA",   AddrMode.AbsoluteX),		#$7f
	("NOOP",  AddrMode.Immediate),		#$80
	("STA",   AddrMode.IndirectX),		#$81
	("NOOP",  AddrMode.Immediate),		#$82
	("SAX",   AddrMode.IndirectX),		#$83
	("STY",   AddrMode.ZeroPage),		#$84
	("STA",   AddrMode.ZeroPage),		#$85
	("STX",   AddrMode.ZeroPage),		#$86
	("SAX",   AddrMode.ZeroPage),		#$87
	("DEY",   AddrMode.Implied),		#$88
	("NOOP",  AddrMode.Immediate),		#$89
	("TXA",   AddrMode.Implied),		#$8a
	("ANE",   AddrMode.Immediate),		#$8b
	("STY",   AddrMode.Absolute),		#$8c
	("STA",   AddrMode.Absolute),		#$8d
	("STX",   AddrMode.Absolute),		#$8e
	("SAX",   AddrMode.Absolute),		#$8f
	("BCC",   AddrMode.Relative),		#$90
	("STA",   AddrMode.IndirectY),		#$91
	("JAM",   AddrMode.Implied),		#$92
	("SHA",   AddrMode.IndirectY),		#$93
	("STY",   AddrMode.ZeroPageX),		#$94
	("STA",   AddrMode.ZeroPageX),		#$95
	("STX",   AddrMode.ZeroPageY),		#$96
	("SAX",   AddrMode.ZeroPageY),		#$97
	("TYA",   AddrMode.Implied),		#$98
	("STA",   AddrMode.AbsoluteY),		#$99
	("TXS",   AddrMode.Implied),		#$9a
	("SHS",   AddrMode.AbsoluteY),		#$9b
	("SHY",   AddrMode.AbsoluteX),		#$9c
	("STA",   AddrMode.AbsoluteX),		#$9d
	("SHX",   AddrMode.AbsoluteY),		#$9e
	("SHA",   AddrMode.AbsoluteY),		#$9f
	("LDY",   AddrMode.Immediate),		#$a0
	("LDA",   AddrMode.IndirectX),		#$a1
	("LDX",   AddrMode.Immediate),		#$a2
	("LAX",   AddrMode.IndirectX),		#$a3
	("LDY",   AddrMode.ZeroPage),		#$a4
	("LDA",   AddrMode.ZeroPage),		#$a5
	("LDX",   AddrMode.ZeroPage),		#$a6
	("LAX",   AddrMode.ZeroPage),		#$a7
	("TAY",   AddrMode.Implied),		#$a8
	("LDA",   AddrMode.Immediate),		#$a9
	("TAX",   AddrMode.Implied),		#$aa
	("LXA",   AddrMode.Immediate),		#$ab
	("LDY",   AddrMode.Absolute),		#$ac
	("LDA",   AddrMode.Absolute),		#$ad
	("LDX",   AddrMode.Absolute),		#$ae
	("LAX",   AddrMode.Absolute),		#$af
	("BCS",   AddrMode.Relative),		#$b0
	("LDA",   AddrMode.IndirectY),		#$b1
	("JAM",   AddrMode.Implied),		#$b2
	("LAX",   AddrMode.IndirectY),		#$b3
	("LDY",   AddrMode.ZeroPageX),		#$b4
	("LDA",   AddrMode.ZeroPageX),		#$b5
	("LDX",   AddrMode.ZeroPageY),		#$b6
	("LAX",   AddrMode.ZeroPageY),		#$b7
	("CLV",   AddrMode.Implied),		#$b8
	("LDA",   AddrMode.AbsoluteY),		#$b9
	("TSX",   AddrMode.Implied),		#$ba
	("LAS",   AddrMode.AbsoluteY),		#$bb
	("LDY",   AddrMode.AbsoluteX),		#$bc
	("LDA",   AddrMode.AbsoluteX),		#$bd
	("LDX",   AddrMode.AbsoluteY),		#$be
	("LAX",   AddrMode.AbsoluteY),		#$bf
	("CPY",   AddrMode.Immediate),		#$c0
	("CMP",   AddrMode.IndirectX),		#$c1
	("NOOP",  AddrMode.Immediate),		#$c2
	("DCP",   AddrMode.IndirectX),		#$c3
	("CPY",   AddrMode.ZeroPage),		#$c4
	("CMP",   AddrMode.ZeroPage),		#$c5
	("DEC",   AddrMode.ZeroPage),		#$c6
	("DCP",   AddrMode.ZeroPage),		#$c7
	("INY",   AddrMode.Implied),		#$c8
	("CMP",   AddrMode.Immediate),		#$c9
	("DEX",   AddrMode.Implied),		#$ca
	("SBX",   AddrMode.Immediate),		#$cb
	("CPY",   AddrMode.Absolute),		#$cc
	("CMP",   AddrMode.Absolute),		#$cd
	("DEC",   AddrMode.Absolute),		#$ce
	("DCP",   AddrMode.Absolute),		#$cf
	("BNE",   AddrMode.Relative),		#$d0
	("CMP",   AddrMode.IndirectY),		#$d1
	("JAM",   AddrMode.Implied),		#$d2
	("DCP",   AddrMode.IndirectY),		#$d3
	("NOOP",  AddrMode.ZeroPageX),		#$d4
	("CMP",   AddrMode.ZeroPageX),		#$d5
	("DEC",   AddrMode.ZeroPageX),		#$d6
	("DCP",   AddrMode.ZeroPageX),		#$d7
	("CLD",   AddrMode.Implied),		#$d8
	("CMP",   AddrMode.AbsoluteY),		#$d9
	("NOOP",  AddrMode.Implied),		#$da
	("DCP",   AddrMode.AbsoluteY),		#$db
	("NOOP",  AddrMode.AbsoluteX),		#$dc
	("CMP",   AddrMode.AbsoluteX),		#$dd
	("DEC",   AddrMode.AbsoluteX),		#$de
	("DCP",   AddrMode.AbsoluteX),		#$df
	("CPX",   AddrMode.Immediate),		#$e0
	("SBC",   AddrMode.IndirectX),		#$e1
	("NOOP",  AddrMode.Immediate),		#$e2
	("ISB",   AddrMode.IndirectX),		#$e3
	("CPX",   AddrMode.ZeroPage),		#$e4
	("SBC",   AddrMode.ZeroPage),		#$e5
	("INC",   AddrMode.ZeroPage),		#$e6
	("ISB",   AddrMode.ZeroPage),		#$e7
	("INX",   AddrMode.Implied),		#$e8
	("SBC",   AddrMode.Immediate),		#$e9
	("NOP",   AddrMode.Implied),		#$ea
	("USBC",  AddrMode.Immediate),		#$eb
	("CPX",   AddrMode.Absolute),		#$ec
	("SBC",   AddrMode.Absolute),		#$ed
	("INC",   AddrMode.Absolute),		#$ee
	("ISB",   AddrMode.Absolute),		#$ef
	("BEQ",   AddrMode.Relative),		#$f0
	("SBC",   AddrMode.IndirectY),		#$f1
	("JAM",   AddrMode.Implied),		#$f2
	("ISB",   AddrMode.IndirectY),		#$f3
	("NOOP",  AddrMode.ZeroPageX),		#$f4
	("SBC",   AddrMode.ZeroPageX),		#$f5
	("INC",   AddrMode.ZeroPageX),		#$f6
	("ISB",   AddrMode.ZeroPageX),		#$f7
	("SED",   AddrMode.Implied),		#$f8
	("SBC",   AddrMode.AbsoluteY),		#$f9
	("NOOP",  AddrMode.Implied),		#$fa
	("ISB",   AddrMode.AbsoluteY),		#$fb
	("NOOP",  AddrMode.AbsoluteX),		#$fc
	("SBC",   AddrMode.AbsoluteX),		#$fd
	("INC",   AddrMode.AbsoluteX),		#$fe
	("ISB",   AddrMode.Absolute)		#$ff
	]

def read_word(b, i):
	return b[i]+b[i+1]*256

def get_operand(b, i, mode):
	sz = mode[0]
	fmt = mode[1]
	if sz==0:
		return fmt
	elif sz==1:
		return fmt.format("${:02x}".format(b[i]))
	elif sz==2:
		return fmt.format("${:04x}".format(read_word(b, i)))
	else:
		raise IndexError("Illegal operand size.")

try:
	f = open("5000-8fff.bin", "rb")
	b = f.read()

	addr = 0x1b44;
	mnm = menumonics[b[addr]]
	md = modes[mnm[1]]
	addr += 1
	print(mnm[0]+" "+get_operand(b, addr, md))
	addr += md[0]

finally:
	f.close()
