from enum import Enum, unique, auto
from collections import namedtuple

from .interval import Interval
from . import errors

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

ModeInfo = namedtuple("ModeInfo", "operand_size, has_address, pre, post")
mode_to_operand_info = {
	AddrMode.Implied		: ModeInfo(0, False, "",  ""    ),
	AddrMode.Accumulator	: ModeInfo(0, False, "A", ""    ),
	AddrMode.Immediate		: ModeInfo(1, False, "#", ""    ),
	AddrMode.ZeroPage		: ModeInfo(1, True,  "",   ""   ),
	AddrMode.ZeroPageX		: ModeInfo(1, True,  "",   ",X" ),
	AddrMode.ZeroPageY		: ModeInfo(1, True,  "",   ",Y" ),
	AddrMode.Absolute		: ModeInfo(2, True,  "",   ""   ),
	AddrMode.AbsoluteX		: ModeInfo(2, True,  "",   ",X" ),
	AddrMode.AbsoluteY		: ModeInfo(2, True,  "",   ",Y" ),
	AddrMode.AbsIndirect	: ModeInfo(2, True,  "(", ")"   ),
	AddrMode.IndirectX		: ModeInfo(1, True,  "(",  ",X)"),
	AddrMode.IndirectY		: ModeInfo(1, True,  "(",  "),Y"),
	AddrMode.Relative		: ModeInfo(1, True,  "",   ""   )
	}

OpcodeInfo = namedtuple("OpcodeInfo", "mnemonic, mode")
opcode_to_mnemonic_and_mode = [
	OpcodeInfo("BRK",   AddrMode.Implied),		#$00
	OpcodeInfo("ORA",   AddrMode.IndirectX),	#$01
	OpcodeInfo("JAM",   AddrMode.Implied),		#$02
	OpcodeInfo("SLO",   AddrMode.IndirectX),	#$03
	OpcodeInfo("NOOP",  AddrMode.ZeroPage),		#$04
	OpcodeInfo("ORA",   AddrMode.ZeroPage),		#$05
	OpcodeInfo("ASL",   AddrMode.ZeroPage),		#$06
	OpcodeInfo("SLO",   AddrMode.ZeroPage),		#$07
	OpcodeInfo("PHP",   AddrMode.Implied),		#$08
	OpcodeInfo("ORA",   AddrMode.Immediate),	#$09
	OpcodeInfo("ASL",   AddrMode.Accumulator),	#$0a
	OpcodeInfo("ANC",   AddrMode.Immediate),	#$0b
	OpcodeInfo("NOOP",  AddrMode.Absolute),		#$0c
	OpcodeInfo("ORA",   AddrMode.Absolute),		#$0d
	OpcodeInfo("ASL",   AddrMode.Absolute),		#$0e
	OpcodeInfo("SLO",   AddrMode.Absolute),		#$0f
	OpcodeInfo("BPL",   AddrMode.Relative),		#$10
	OpcodeInfo("ORA",   AddrMode.IndirectY),	#$11
	OpcodeInfo("JAM",   AddrMode.Implied),		#$12
	OpcodeInfo("SLO",   AddrMode.IndirectY),	#$13
	OpcodeInfo("NOOP",  AddrMode.ZeroPageX),	#$14
	OpcodeInfo("ORA",   AddrMode.ZeroPageX),	#$15
	OpcodeInfo("ASL",   AddrMode.ZeroPageX),	#$16
	OpcodeInfo("SLO",   AddrMode.ZeroPageX),	#$17
	OpcodeInfo("CLC",   AddrMode.Implied),		#$18
	OpcodeInfo("ORA",   AddrMode.AbsoluteY),	#$19
	OpcodeInfo("NOOP",  AddrMode.Implied),		#$1a
	OpcodeInfo("SLO",   AddrMode.AbsoluteY),	#$1b
	OpcodeInfo("NOOP",  AddrMode.AbsoluteX),	#$1c
	OpcodeInfo("ORA",   AddrMode.AbsoluteX),	#$1d
	OpcodeInfo("ASL",   AddrMode.AbsoluteX),	#$1e
	OpcodeInfo("SLO",   AddrMode.AbsoluteX),	#$1f
	OpcodeInfo("JSR",   AddrMode.Absolute),		#$20
	OpcodeInfo("AND",   AddrMode.IndirectX),	#$21
	OpcodeInfo("JAM",   AddrMode.Implied),		#$22
	OpcodeInfo("RLA",   AddrMode.IndirectX),	#$23
	OpcodeInfo("BIT",   AddrMode.ZeroPage),		#$24
	OpcodeInfo("AND",   AddrMode.ZeroPage),		#$25
	OpcodeInfo("ROL",   AddrMode.ZeroPage),		#$26
	OpcodeInfo("RLA",   AddrMode.ZeroPage),		#$27
	OpcodeInfo("PLP",   AddrMode.Implied),		#$28
	OpcodeInfo("AND",   AddrMode.Immediate),	#$29
	OpcodeInfo("ROL",   AddrMode.Accumulator),	#$2a
	OpcodeInfo("ANC",   AddrMode.Immediate),	#$2b
	OpcodeInfo("BIT",   AddrMode.Absolute),		#$2c
	OpcodeInfo("AND",   AddrMode.Absolute),		#$2d
	OpcodeInfo("ROL",   AddrMode.Absolute),		#$2e
	OpcodeInfo("RLA",   AddrMode.Absolute),		#$2f
	OpcodeInfo("BMI",   AddrMode.Relative),		#$30
	OpcodeInfo("AND",   AddrMode.IndirectY),	#$31
	OpcodeInfo("JAM",   AddrMode.Implied),		#$32
	OpcodeInfo("RLA",   AddrMode.IndirectY),	#$33
	OpcodeInfo("NOOP",  AddrMode.ZeroPageX),	#$34
	OpcodeInfo("AND",   AddrMode.ZeroPageX),	#$35
	OpcodeInfo("ROL",   AddrMode.ZeroPageX),	#$36
	OpcodeInfo("RLA",   AddrMode.ZeroPageX),	#$37
	OpcodeInfo("SEC",   AddrMode.Implied),		#$38
	OpcodeInfo("AND",   AddrMode.AbsoluteY),	#$39
	OpcodeInfo("NOOP",  AddrMode.Implied),		#$3a
	OpcodeInfo("RLA",   AddrMode.AbsoluteY),	#$3b
	OpcodeInfo("NOOP",  AddrMode.AbsoluteX),	#$3c
	OpcodeInfo("AND",   AddrMode.AbsoluteX),	#$3d
	OpcodeInfo("ROL",   AddrMode.AbsoluteX),	#$3e
	OpcodeInfo("RLA",   AddrMode.AbsoluteX),	#$3f
	OpcodeInfo("RTI",   AddrMode.Implied),		#$40
	OpcodeInfo("EOR",   AddrMode.IndirectX),	#$41
	OpcodeInfo("JAM",   AddrMode.Implied),		#$42
	OpcodeInfo("SRE",   AddrMode.IndirectX),	#$43
	OpcodeInfo("NOOP",  AddrMode.ZeroPage),		#$44
	OpcodeInfo("EOR",   AddrMode.ZeroPage),		#$45
	OpcodeInfo("LSR",   AddrMode.ZeroPage),		#$46
	OpcodeInfo("SRE",   AddrMode.ZeroPage),		#$47
	OpcodeInfo("PHA",   AddrMode.Implied),		#$48
	OpcodeInfo("EOR",   AddrMode.Immediate),	#$49
	OpcodeInfo("LSR",   AddrMode.Accumulator),	#$4a
	OpcodeInfo("ASR",   AddrMode.Immediate),	#$4b
	OpcodeInfo("JMP",   AddrMode.Absolute),		#$4c
	OpcodeInfo("EOR",   AddrMode.Absolute),		#$4d
	OpcodeInfo("LSR",   AddrMode.Absolute),		#$4e
	OpcodeInfo("SRE",   AddrMode.Absolute),		#$4f
	OpcodeInfo("BVC",   AddrMode.Relative),		#$50
	OpcodeInfo("EOR",   AddrMode.IndirectY),	#$51
	OpcodeInfo("JAM",   AddrMode.Implied),		#$52
	OpcodeInfo("SRE",   AddrMode.IndirectY),	#$53
	OpcodeInfo("NOOP",  AddrMode.ZeroPageX),	#$54
	OpcodeInfo("EOR",   AddrMode.ZeroPageX),	#$55
	OpcodeInfo("LSR",   AddrMode.ZeroPageX),	#$56
	OpcodeInfo("SRE",   AddrMode.ZeroPageX),	#$57
	OpcodeInfo("CLI",   AddrMode.Implied),		#$58
	OpcodeInfo("EOR",   AddrMode.AbsoluteY),	#$59
	OpcodeInfo("NOOP",  AddrMode.Implied),		#$5a
	OpcodeInfo("SRE",   AddrMode.AbsoluteY),	#$5b
	OpcodeInfo("NOOP",  AddrMode.AbsoluteX),	#$5c
	OpcodeInfo("EOR",   AddrMode.AbsoluteX),	#$5d
	OpcodeInfo("LSR",   AddrMode.AbsoluteX),	#$5e
	OpcodeInfo("SRE",   AddrMode.AbsoluteX),	#$5f
	OpcodeInfo("RTS",   AddrMode.Implied),		#$60
	OpcodeInfo("ADC",   AddrMode.IndirectX),	#$61
	OpcodeInfo("JAM",   AddrMode.Implied),		#$62
	OpcodeInfo("RRA",   AddrMode.IndirectX),	#$63
	OpcodeInfo("NOOP",  AddrMode.ZeroPage),		#$64
	OpcodeInfo("ADC",   AddrMode.ZeroPage),		#$65
	OpcodeInfo("ROR",   AddrMode.ZeroPage),		#$66
	OpcodeInfo("RRA",   AddrMode.ZeroPage),		#$67
	OpcodeInfo("PLA",   AddrMode.Implied),		#$68
	OpcodeInfo("ADC",   AddrMode.Immediate),	#$69
	OpcodeInfo("ROR",   AddrMode.Accumulator),	#$6a
	OpcodeInfo("ARR",   AddrMode.Immediate),	#$6b
	OpcodeInfo("JMP",   AddrMode.AbsIndirect),	#$6c
	OpcodeInfo("ADC",   AddrMode.Absolute),		#$6d
	OpcodeInfo("ROR",   AddrMode.Absolute),		#$6e
	OpcodeInfo("RRA",   AddrMode.Absolute),		#$6f
	OpcodeInfo("BVS",   AddrMode.Relative),		#$70
	OpcodeInfo("ADC",   AddrMode.IndirectY),	#$71
	OpcodeInfo("JAM",   AddrMode.Implied),		#$72
	OpcodeInfo("RRA",   AddrMode.IndirectY),	#$73
	OpcodeInfo("NOOP",  AddrMode.ZeroPageX),	#$74
	OpcodeInfo("ADC",   AddrMode.ZeroPageX),	#$75
	OpcodeInfo("ROR",   AddrMode.ZeroPageX),	#$76
	OpcodeInfo("RRA",   AddrMode.ZeroPageX),	#$77
	OpcodeInfo("SEI",   AddrMode.Implied),		#$78
	OpcodeInfo("ADC",   AddrMode.AbsoluteY),	#$79
	OpcodeInfo("NOOP",  AddrMode.Implied),		#$7a
	OpcodeInfo("RRA",   AddrMode.AbsoluteY),	#$7b
	OpcodeInfo("NOOP",  AddrMode.AbsoluteX),	#$7c
	OpcodeInfo("ADC",   AddrMode.AbsoluteX),	#$7d
	OpcodeInfo("ROR",   AddrMode.AbsoluteX),	#$7e
	OpcodeInfo("RRA",   AddrMode.AbsoluteX),	#$7f
	OpcodeInfo("NOOP",  AddrMode.Immediate),	#$80
	OpcodeInfo("STA",   AddrMode.IndirectX),	#$81
	OpcodeInfo("NOOP",  AddrMode.Immediate),	#$82
	OpcodeInfo("SAX",   AddrMode.IndirectX),	#$83
	OpcodeInfo("STY",   AddrMode.ZeroPage),		#$84
	OpcodeInfo("STA",   AddrMode.ZeroPage),		#$85
	OpcodeInfo("STX",   AddrMode.ZeroPage),		#$86
	OpcodeInfo("SAX",   AddrMode.ZeroPage),		#$87
	OpcodeInfo("DEY",   AddrMode.Implied),		#$88
	OpcodeInfo("NOOP",  AddrMode.Immediate),	#$89
	OpcodeInfo("TXA",   AddrMode.Implied),		#$8a
	OpcodeInfo("ANE",   AddrMode.Immediate),	#$8b
	OpcodeInfo("STY",   AddrMode.Absolute),		#$8c
	OpcodeInfo("STA",   AddrMode.Absolute),		#$8d
	OpcodeInfo("STX",   AddrMode.Absolute),		#$8e
	OpcodeInfo("SAX",   AddrMode.Absolute),		#$8f
	OpcodeInfo("BCC",   AddrMode.Relative),		#$90
	OpcodeInfo("STA",   AddrMode.IndirectY),	#$91
	OpcodeInfo("JAM",   AddrMode.Implied),		#$92
	OpcodeInfo("SHA",   AddrMode.IndirectY),	#$93
	OpcodeInfo("STY",   AddrMode.ZeroPageX),	#$94
	OpcodeInfo("STA",   AddrMode.ZeroPageX),	#$95
	OpcodeInfo("STX",   AddrMode.ZeroPageY),	#$96
	OpcodeInfo("SAX",   AddrMode.ZeroPageY),	#$97
	OpcodeInfo("TYA",   AddrMode.Implied),		#$98
	OpcodeInfo("STA",   AddrMode.AbsoluteY),	#$99
	OpcodeInfo("TXS",   AddrMode.Implied),		#$9a
	OpcodeInfo("SHS",   AddrMode.AbsoluteY),	#$9b
	OpcodeInfo("SHY",   AddrMode.AbsoluteX),	#$9c
	OpcodeInfo("STA",   AddrMode.AbsoluteX),	#$9d
	OpcodeInfo("SHX",   AddrMode.AbsoluteY),	#$9e
	OpcodeInfo("SHA",   AddrMode.AbsoluteY),	#$9f
	OpcodeInfo("LDY",   AddrMode.Immediate),	#$a0
	OpcodeInfo("LDA",   AddrMode.IndirectX),	#$a1
	OpcodeInfo("LDX",   AddrMode.Immediate),	#$a2
	OpcodeInfo("LAX",   AddrMode.IndirectX),	#$a3
	OpcodeInfo("LDY",   AddrMode.ZeroPage),		#$a4
	OpcodeInfo("LDA",   AddrMode.ZeroPage),		#$a5
	OpcodeInfo("LDX",   AddrMode.ZeroPage),		#$a6
	OpcodeInfo("LAX",   AddrMode.ZeroPage),		#$a7
	OpcodeInfo("TAY",   AddrMode.Implied),		#$a8
	OpcodeInfo("LDA",   AddrMode.Immediate),	#$a9
	OpcodeInfo("TAX",   AddrMode.Implied),		#$aa
	OpcodeInfo("LXA",   AddrMode.Immediate),	#$ab
	OpcodeInfo("LDY",   AddrMode.Absolute),		#$ac
	OpcodeInfo("LDA",   AddrMode.Absolute),		#$ad
	OpcodeInfo("LDX",   AddrMode.Absolute),		#$ae
	OpcodeInfo("LAX",   AddrMode.Absolute),		#$af
	OpcodeInfo("BCS",   AddrMode.Relative),		#$b0
	OpcodeInfo("LDA",   AddrMode.IndirectY),	#$b1
	OpcodeInfo("JAM",   AddrMode.Implied),		#$b2
	OpcodeInfo("LAX",   AddrMode.IndirectY),	#$b3
	OpcodeInfo("LDY",   AddrMode.ZeroPageX),	#$b4
	OpcodeInfo("LDA",   AddrMode.ZeroPageX),	#$b5
	OpcodeInfo("LDX",   AddrMode.ZeroPageY),	#$b6
	OpcodeInfo("LAX",   AddrMode.ZeroPageY),	#$b7
	OpcodeInfo("CLV",   AddrMode.Implied),		#$b8
	OpcodeInfo("LDA",   AddrMode.AbsoluteY),	#$b9
	OpcodeInfo("TSX",   AddrMode.Implied),		#$ba
	OpcodeInfo("LAS",   AddrMode.AbsoluteY),	#$bb
	OpcodeInfo("LDY",   AddrMode.AbsoluteX),	#$bc
	OpcodeInfo("LDA",   AddrMode.AbsoluteX),	#$bd
	OpcodeInfo("LDX",   AddrMode.AbsoluteY),	#$be
	OpcodeInfo("LAX",   AddrMode.AbsoluteY),	#$bf
	OpcodeInfo("CPY",   AddrMode.Immediate),	#$c0
	OpcodeInfo("CMP",   AddrMode.IndirectX),	#$c1
	OpcodeInfo("NOOP",  AddrMode.Immediate),	#$c2
	OpcodeInfo("DCP",   AddrMode.IndirectX),	#$c3
	OpcodeInfo("CPY",   AddrMode.ZeroPage),		#$c4
	OpcodeInfo("CMP",   AddrMode.ZeroPage),		#$c5
	OpcodeInfo("DEC",   AddrMode.ZeroPage),		#$c6
	OpcodeInfo("DCP",   AddrMode.ZeroPage),		#$c7
	OpcodeInfo("INY",   AddrMode.Implied),		#$c8
	OpcodeInfo("CMP",   AddrMode.Immediate),	#$c9
	OpcodeInfo("DEX",   AddrMode.Implied),		#$ca
	OpcodeInfo("SBX",   AddrMode.Immediate),	#$cb
	OpcodeInfo("CPY",   AddrMode.Absolute),		#$cc
	OpcodeInfo("CMP",   AddrMode.Absolute),		#$cd
	OpcodeInfo("DEC",   AddrMode.Absolute),		#$ce
	OpcodeInfo("DCP",   AddrMode.Absolute),		#$cf
	OpcodeInfo("BNE",   AddrMode.Relative),		#$d0
	OpcodeInfo("CMP",   AddrMode.IndirectY),	#$d1
	OpcodeInfo("JAM",   AddrMode.Implied),		#$d2
	OpcodeInfo("DCP",   AddrMode.IndirectY),	#$d3
	OpcodeInfo("NOOP",  AddrMode.ZeroPageX),	#$d4
	OpcodeInfo("CMP",   AddrMode.ZeroPageX),	#$d5
	OpcodeInfo("DEC",   AddrMode.ZeroPageX),	#$d6
	OpcodeInfo("DCP",   AddrMode.ZeroPageX),	#$d7
	OpcodeInfo("CLD",   AddrMode.Implied),		#$d8
	OpcodeInfo("CMP",   AddrMode.AbsoluteY),	#$d9
	OpcodeInfo("NOOP",  AddrMode.Implied),		#$da
	OpcodeInfo("DCP",   AddrMode.AbsoluteY),	#$db
	OpcodeInfo("NOOP",  AddrMode.AbsoluteX),	#$dc
	OpcodeInfo("CMP",   AddrMode.AbsoluteX),	#$dd
	OpcodeInfo("DEC",   AddrMode.AbsoluteX),	#$de
	OpcodeInfo("DCP",   AddrMode.AbsoluteX),	#$df
	OpcodeInfo("CPX",   AddrMode.Immediate),	#$e0
	OpcodeInfo("SBC",   AddrMode.IndirectX),	#$e1
	OpcodeInfo("NOOP",  AddrMode.Immediate),	#$e2
	OpcodeInfo("ISB",   AddrMode.IndirectX),	#$e3
	OpcodeInfo("CPX",   AddrMode.ZeroPage),		#$e4
	OpcodeInfo("SBC",   AddrMode.ZeroPage),		#$e5
	OpcodeInfo("INC",   AddrMode.ZeroPage),		#$e6
	OpcodeInfo("ISB",   AddrMode.ZeroPage),		#$e7
	OpcodeInfo("INX",   AddrMode.Implied),		#$e8
	OpcodeInfo("SBC",   AddrMode.Immediate),	#$e9
	OpcodeInfo("NOP",   AddrMode.Implied),		#$ea
	OpcodeInfo("USBC",  AddrMode.Immediate),	#$eb
	OpcodeInfo("CPX",   AddrMode.Absolute),		#$ec
	OpcodeInfo("SBC",   AddrMode.Absolute),		#$ed
	OpcodeInfo("INC",   AddrMode.Absolute),		#$ee
	OpcodeInfo("ISB",   AddrMode.Absolute),		#$ef
	OpcodeInfo("BEQ",   AddrMode.Relative),		#$f0
	OpcodeInfo("SBC",   AddrMode.IndirectY),	#$f1
	OpcodeInfo("JAM",   AddrMode.Implied),		#$f2
	OpcodeInfo("ISB",   AddrMode.IndirectY),	#$f3
	OpcodeInfo("NOOP",  AddrMode.ZeroPageX),	#$f4
	OpcodeInfo("SBC",   AddrMode.ZeroPageX),	#$f5
	OpcodeInfo("INC",   AddrMode.ZeroPageX),	#$f6
	OpcodeInfo("ISB",   AddrMode.ZeroPageX),	#$f7
	OpcodeInfo("SED",   AddrMode.Implied),		#$f8
	OpcodeInfo("SBC",   AddrMode.AbsoluteY),	#$f9
	OpcodeInfo("NOOP",  AddrMode.Implied),		#$fa
	OpcodeInfo("ISB",   AddrMode.AbsoluteY),	#$fb
	OpcodeInfo("NOOP",  AddrMode.AbsoluteX),	#$fc
	OpcodeInfo("SBC",   AddrMode.AbsoluteX),	#$fd
	OpcodeInfo("INC",   AddrMode.AbsoluteX),	#$fe
	OpcodeInfo("ISB",   AddrMode.Absolute)		#$ff
	]

def sign_extend(x):
	return (x^0x80)-0x80;

InstructionInfo = namedtuple("InstructionInfo", "ivl, opcode, operand, target, op_info, mode_info")
def M6502Iterator(mem, ivl):
	mem = mem.view(ivl)
	addr = ivl.first
	while addr<=ivl.last:
		opcode = mem.r8(addr)
		op_info = opcode_to_mnemonic_and_mode[opcode]
		mode_info = mode_to_operand_info[op_info.mode]

		try:
			if mode_info.operand_size == 0:
				operand = None
			elif mode_info.operand_size == 1:
				operand = mem.r8(addr+1)
			elif mode_info.operand_size == 2:
				operand = mem.r16(addr+1)
		except errors.MemoryException:
			return # there's some space left at the end of 'ivl'

		if op_info.mode == AddrMode.Relative:
			target = addr+sign_extend(operand)+2
		elif mode_info.has_address:
			target = operand
		else:
			target = None

		yield InstructionInfo(Interval(addr, addr+mode_info.operand_size), opcode, operand, target, op_info, mode_info)

		addr += mode_info.operand_size+1
