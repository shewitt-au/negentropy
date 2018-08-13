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
    AddrMode.Implied        : ModeInfo(0, False, "",  ""    ),
    AddrMode.Accumulator    : ModeInfo(0, False, "A", ""    ),
    AddrMode.Immediate      : ModeInfo(1, False, "#", ""    ),
    AddrMode.ZeroPage       : ModeInfo(1, True,  "",   ""   ),
    AddrMode.ZeroPageX      : ModeInfo(1, True,  "",   ",X" ),
    AddrMode.ZeroPageY      : ModeInfo(1, True,  "",   ",Y" ),
    AddrMode.Absolute       : ModeInfo(2, True,  "",   ""   ),
    AddrMode.AbsoluteX      : ModeInfo(2, True,  "",   ",X" ),
    AddrMode.AbsoluteY      : ModeInfo(2, True,  "",   ",Y" ),
    AddrMode.AbsIndirect    : ModeInfo(2, True,  "(", ")"   ),
    AddrMode.IndirectX      : ModeInfo(1, True,  "(",  ",X)"),
    AddrMode.IndirectY      : ModeInfo(1, True,  "(",  "),Y"),
    AddrMode.Relative       : ModeInfo(1, True,  "",   ""   )
    }

OpcodeInfo = namedtuple("OpcodeInfo", "mnemonic, mode, flow_transfer")
opcode_to_mnemonic_and_mode = [
    OpcodeInfo("BRK",   AddrMode.Implied,       False),     #$00
    OpcodeInfo("ORA",   AddrMode.IndirectX,     False),     #$01
    OpcodeInfo("JAM",   AddrMode.Implied,       False),     #$02
    OpcodeInfo("SLO",   AddrMode.IndirectX,     False),     #$03
    OpcodeInfo("NOOP",  AddrMode.ZeroPage,      False),     #$04
    OpcodeInfo("ORA",   AddrMode.ZeroPage,      False),     #$05
    OpcodeInfo("ASL",   AddrMode.ZeroPage,      False),     #$06
    OpcodeInfo("SLO",   AddrMode.ZeroPage,      False),     #$07
    OpcodeInfo("PHP",   AddrMode.Implied,       False),     #$08
    OpcodeInfo("ORA",   AddrMode.Immediate,     False),     #$09
    OpcodeInfo("ASL",   AddrMode.Accumulator,   False),     #$0a
    OpcodeInfo("ANC",   AddrMode.Immediate,     False),     #$0b
    OpcodeInfo("NOOP",  AddrMode.Absolute,      False),     #$0c
    OpcodeInfo("ORA",   AddrMode.Absolute,      False),     #$0d
    OpcodeInfo("ASL",   AddrMode.Absolute,      False),     #$0e
    OpcodeInfo("SLO",   AddrMode.Absolute,      False),     #$0f
    OpcodeInfo("BPL",   AddrMode.Relative,      True ),     #$10
    OpcodeInfo("ORA",   AddrMode.IndirectY,     False),     #$11
    OpcodeInfo("JAM",   AddrMode.Implied,       False),     #$12
    OpcodeInfo("SLO",   AddrMode.IndirectY,     False),     #$13
    OpcodeInfo("NOOP",  AddrMode.ZeroPageX,     False),     #$14
    OpcodeInfo("ORA",   AddrMode.ZeroPageX,     False),     #$15
    OpcodeInfo("ASL",   AddrMode.ZeroPageX,     False),     #$16
    OpcodeInfo("SLO",   AddrMode.ZeroPageX,     False),     #$17
    OpcodeInfo("CLC",   AddrMode.Implied,       False),     #$18
    OpcodeInfo("ORA",   AddrMode.AbsoluteY,     False),     #$19
    OpcodeInfo("NOOP",  AddrMode.Implied,       False),     #$1a
    OpcodeInfo("SLO",   AddrMode.AbsoluteY,     False),     #$1b
    OpcodeInfo("NOOP",  AddrMode.AbsoluteX,     False),     #$1c
    OpcodeInfo("ORA",   AddrMode.AbsoluteX,     False),     #$1d
    OpcodeInfo("ASL",   AddrMode.AbsoluteX,     False),     #$1e
    OpcodeInfo("SLO",   AddrMode.AbsoluteX,     False),     #$1f
    OpcodeInfo("JSR",   AddrMode.Absolute,      True ),     #$20
    OpcodeInfo("AND",   AddrMode.IndirectX,     False),     #$21
    OpcodeInfo("JAM",   AddrMode.Implied,       False),     #$22
    OpcodeInfo("RLA",   AddrMode.IndirectX,     False),     #$23
    OpcodeInfo("BIT",   AddrMode.ZeroPage,      False),     #$24
    OpcodeInfo("AND",   AddrMode.ZeroPage,      False),     #$25
    OpcodeInfo("ROL",   AddrMode.ZeroPage,      False),     #$26
    OpcodeInfo("RLA",   AddrMode.ZeroPage,      False),     #$27
    OpcodeInfo("PLP",   AddrMode.Implied,       False),     #$28
    OpcodeInfo("AND",   AddrMode.Immediate,     False),     #$29
    OpcodeInfo("ROL",   AddrMode.Accumulator,   False),     #$2a
    OpcodeInfo("ANC",   AddrMode.Immediate,     False),     #$2b
    OpcodeInfo("BIT",   AddrMode.Absolute,      False),     #$2c
    OpcodeInfo("AND",   AddrMode.Absolute,      False),     #$2d
    OpcodeInfo("ROL",   AddrMode.Absolute,      False),     #$2e
    OpcodeInfo("RLA",   AddrMode.Absolute,      False),     #$2f
    OpcodeInfo("BMI",   AddrMode.Relative,      True ),     #$30
    OpcodeInfo("AND",   AddrMode.IndirectY,     False),     #$31
    OpcodeInfo("JAM",   AddrMode.Implied,       False),     #$32
    OpcodeInfo("RLA",   AddrMode.IndirectY,     False),     #$33
    OpcodeInfo("NOOP",  AddrMode.ZeroPageX,     False),     #$34
    OpcodeInfo("AND",   AddrMode.ZeroPageX,     False),     #$35
    OpcodeInfo("ROL",   AddrMode.ZeroPageX,     False),     #$36
    OpcodeInfo("RLA",   AddrMode.ZeroPageX,     False),     #$37
    OpcodeInfo("SEC",   AddrMode.Implied,       False),     #$38
    OpcodeInfo("AND",   AddrMode.AbsoluteY,     False),     #$39
    OpcodeInfo("NOOP",  AddrMode.Implied,       False),     #$3a
    OpcodeInfo("RLA",   AddrMode.AbsoluteY,     False),     #$3b
    OpcodeInfo("NOOP",  AddrMode.AbsoluteX,     False),     #$3c
    OpcodeInfo("AND",   AddrMode.AbsoluteX,     False),     #$3d
    OpcodeInfo("ROL",   AddrMode.AbsoluteX,     False),     #$3e
    OpcodeInfo("RLA",   AddrMode.AbsoluteX,     False),     #$3f
    OpcodeInfo("RTI",   AddrMode.Implied,       False),     #$40
    OpcodeInfo("EOR",   AddrMode.IndirectX,     False),     #$41
    OpcodeInfo("JAM",   AddrMode.Implied,       False),     #$42
    OpcodeInfo("SRE",   AddrMode.IndirectX,     False),     #$43
    OpcodeInfo("NOOP",  AddrMode.ZeroPage,      False),     #$44
    OpcodeInfo("EOR",   AddrMode.ZeroPage,      False),     #$45
    OpcodeInfo("LSR",   AddrMode.ZeroPage,      False),     #$46
    OpcodeInfo("SRE",   AddrMode.ZeroPage,      False),     #$47
    OpcodeInfo("PHA",   AddrMode.Implied,       False),     #$48
    OpcodeInfo("EOR",   AddrMode.Immediate,     False),     #$49
    OpcodeInfo("LSR",   AddrMode.Accumulator,   False),     #$4a
    OpcodeInfo("ASR",   AddrMode.Immediate,     False),     #$4b
    OpcodeInfo("JMP",   AddrMode.Absolute,      True ),     #$4c
    OpcodeInfo("EOR",   AddrMode.Absolute,      False),     #$4d
    OpcodeInfo("LSR",   AddrMode.Absolute,      False),     #$4e
    OpcodeInfo("SRE",   AddrMode.Absolute,      False),     #$4f
    OpcodeInfo("BVC",   AddrMode.Relative,      True ),     #$50
    OpcodeInfo("EOR",   AddrMode.IndirectY,     False),     #$51
    OpcodeInfo("JAM",   AddrMode.Implied,       False),     #$52
    OpcodeInfo("SRE",   AddrMode.IndirectY,     False),     #$53
    OpcodeInfo("NOOP",  AddrMode.ZeroPageX,     False),     #$54
    OpcodeInfo("EOR",   AddrMode.ZeroPageX,     False),     #$55
    OpcodeInfo("LSR",   AddrMode.ZeroPageX,     False),     #$56
    OpcodeInfo("SRE",   AddrMode.ZeroPageX,     False),     #$57
    OpcodeInfo("CLI",   AddrMode.Implied,       False),     #$58
    OpcodeInfo("EOR",   AddrMode.AbsoluteY,     False),     #$59
    OpcodeInfo("NOOP",  AddrMode.Implied,       False),     #$5a
    OpcodeInfo("SRE",   AddrMode.AbsoluteY,     False),     #$5b
    OpcodeInfo("NOOP",  AddrMode.AbsoluteX,     False),     #$5c
    OpcodeInfo("EOR",   AddrMode.AbsoluteX,     False),     #$5d
    OpcodeInfo("LSR",   AddrMode.AbsoluteX,     False),     #$5e
    OpcodeInfo("SRE",   AddrMode.AbsoluteX,     False),     #$5f
    OpcodeInfo("RTS",   AddrMode.Implied,       False),     #$60
    OpcodeInfo("ADC",   AddrMode.IndirectX,     False),     #$61
    OpcodeInfo("JAM",   AddrMode.Implied,       False),     #$62
    OpcodeInfo("RRA",   AddrMode.IndirectX,     False),     #$63
    OpcodeInfo("NOOP",  AddrMode.ZeroPage,      False),     #$64
    OpcodeInfo("ADC",   AddrMode.ZeroPage,      False),     #$65
    OpcodeInfo("ROR",   AddrMode.ZeroPage,      False),     #$66
    OpcodeInfo("RRA",   AddrMode.ZeroPage,      False),     #$67
    OpcodeInfo("PLA",   AddrMode.Implied,       False),     #$68
    OpcodeInfo("ADC",   AddrMode.Immediate,     False),     #$69
    OpcodeInfo("ROR",   AddrMode.Accumulator,   False),     #$6a
    OpcodeInfo("ARR",   AddrMode.Immediate,     False),     #$6b
    OpcodeInfo("JMP",   AddrMode.AbsIndirect,   True ),     #$6c
    OpcodeInfo("ADC",   AddrMode.Absolute,      False),     #$6d
    OpcodeInfo("ROR",   AddrMode.Absolute,      False),     #$6e
    OpcodeInfo("RRA",   AddrMode.Absolute,      False),     #$6f
    OpcodeInfo("BVS",   AddrMode.Relative,      True ),     #$70
    OpcodeInfo("ADC",   AddrMode.IndirectY,     False),     #$71
    OpcodeInfo("JAM",   AddrMode.Implied,       False),     #$72
    OpcodeInfo("RRA",   AddrMode.IndirectY,     False),     #$73
    OpcodeInfo("NOOP",  AddrMode.ZeroPageX,     False),     #$74
    OpcodeInfo("ADC",   AddrMode.ZeroPageX,     False),     #$75
    OpcodeInfo("ROR",   AddrMode.ZeroPageX,     False),     #$76
    OpcodeInfo("RRA",   AddrMode.ZeroPageX,     False),     #$77
    OpcodeInfo("SEI",   AddrMode.Implied,       False),     #$78
    OpcodeInfo("ADC",   AddrMode.AbsoluteY,     False),     #$79
    OpcodeInfo("NOOP",  AddrMode.Implied,       False),     #$7a
    OpcodeInfo("RRA",   AddrMode.AbsoluteY,     False),     #$7b
    OpcodeInfo("NOOP",  AddrMode.AbsoluteX,     False),     #$7c
    OpcodeInfo("ADC",   AddrMode.AbsoluteX,     False),     #$7d
    OpcodeInfo("ROR",   AddrMode.AbsoluteX,     False),     #$7e
    OpcodeInfo("RRA",   AddrMode.AbsoluteX,     False),     #$7f
    OpcodeInfo("NOOP",  AddrMode.Immediate,     False),     #$80
    OpcodeInfo("STA",   AddrMode.IndirectX,     False),     #$81
    OpcodeInfo("NOOP",  AddrMode.Immediate,     False),     #$82
    OpcodeInfo("SAX",   AddrMode.IndirectX,     False),     #$83
    OpcodeInfo("STY",   AddrMode.ZeroPage,      False),     #$84
    OpcodeInfo("STA",   AddrMode.ZeroPage,      False),     #$85
    OpcodeInfo("STX",   AddrMode.ZeroPage,      False),     #$86
    OpcodeInfo("SAX",   AddrMode.ZeroPage,      False),     #$87
    OpcodeInfo("DEY",   AddrMode.Implied,       False),     #$88
    OpcodeInfo("NOOP",  AddrMode.Immediate,     False),     #$89
    OpcodeInfo("TXA",   AddrMode.Implied,       False),     #$8a
    OpcodeInfo("ANE",   AddrMode.Immediate,     False),     #$8b
    OpcodeInfo("STY",   AddrMode.Absolute,      False),     #$8c
    OpcodeInfo("STA",   AddrMode.Absolute,      False),     #$8d
    OpcodeInfo("STX",   AddrMode.Absolute,      False),     #$8e
    OpcodeInfo("SAX",   AddrMode.Absolute,      False),     #$8f
    OpcodeInfo("BCC",   AddrMode.Relative,      True ),     #$90
    OpcodeInfo("STA",   AddrMode.IndirectY,     False),     #$91
    OpcodeInfo("JAM",   AddrMode.Implied,       False),     #$92
    OpcodeInfo("SHA",   AddrMode.IndirectY,     False),     #$93
    OpcodeInfo("STY",   AddrMode.ZeroPageX,     False),     #$94
    OpcodeInfo("STA",   AddrMode.ZeroPageX,     False),     #$95
    OpcodeInfo("STX",   AddrMode.ZeroPageY,     False),     #$96
    OpcodeInfo("SAX",   AddrMode.ZeroPageY,     False),     #$97
    OpcodeInfo("TYA",   AddrMode.Implied,       False),     #$98
    OpcodeInfo("STA",   AddrMode.AbsoluteY,     False),     #$99
    OpcodeInfo("TXS",   AddrMode.Implied,       False),     #$9a
    OpcodeInfo("SHS",   AddrMode.AbsoluteY,     False),     #$9b
    OpcodeInfo("SHY",   AddrMode.AbsoluteX,     False),     #$9c
    OpcodeInfo("STA",   AddrMode.AbsoluteX,     False),     #$9d
    OpcodeInfo("SHX",   AddrMode.AbsoluteY,     False),     #$9e
    OpcodeInfo("SHA",   AddrMode.AbsoluteY,     False),     #$9f
    OpcodeInfo("LDY",   AddrMode.Immediate,     False),     #$a0
    OpcodeInfo("LDA",   AddrMode.IndirectX,     False),     #$a1
    OpcodeInfo("LDX",   AddrMode.Immediate,     False),     #$a2
    OpcodeInfo("LAX",   AddrMode.IndirectX,     False),     #$a3
    OpcodeInfo("LDY",   AddrMode.ZeroPage,      False),     #$a4
    OpcodeInfo("LDA",   AddrMode.ZeroPage,      False),     #$a5
    OpcodeInfo("LDX",   AddrMode.ZeroPage,      False),     #$a6
    OpcodeInfo("LAX",   AddrMode.ZeroPage,      False),     #$a7
    OpcodeInfo("TAY",   AddrMode.Implied,       False),     #$a8
    OpcodeInfo("LDA",   AddrMode.Immediate,     False),     #$a9
    OpcodeInfo("TAX",   AddrMode.Implied,       False),     #$aa
    OpcodeInfo("LXA",   AddrMode.Immediate,     False),     #$ab
    OpcodeInfo("LDY",   AddrMode.Absolute,      False),     #$ac
    OpcodeInfo("LDA",   AddrMode.Absolute,      False),     #$ad
    OpcodeInfo("LDX",   AddrMode.Absolute,      False),     #$ae
    OpcodeInfo("LAX",   AddrMode.Absolute,      False),     #$af
    OpcodeInfo("BCS",   AddrMode.Relative,      True ),     #$b0
    OpcodeInfo("LDA",   AddrMode.IndirectY,     False),     #$b1
    OpcodeInfo("JAM",   AddrMode.Implied,       False),     #$b2
    OpcodeInfo("LAX",   AddrMode.IndirectY,     False),     #$b3
    OpcodeInfo("LDY",   AddrMode.ZeroPageX,     False),     #$b4
    OpcodeInfo("LDA",   AddrMode.ZeroPageX,     False),     #$b5
    OpcodeInfo("LDX",   AddrMode.ZeroPageY,     False),     #$b6
    OpcodeInfo("LAX",   AddrMode.ZeroPageY,     False),     #$b7
    OpcodeInfo("CLV",   AddrMode.Implied,       False),     #$b8
    OpcodeInfo("LDA",   AddrMode.AbsoluteY,     False),     #$b9
    OpcodeInfo("TSX",   AddrMode.Implied,       False),     #$ba
    OpcodeInfo("LAS",   AddrMode.AbsoluteY,     False),     #$bb
    OpcodeInfo("LDY",   AddrMode.AbsoluteX,     False),     #$bc
    OpcodeInfo("LDA",   AddrMode.AbsoluteX,     False),     #$bd
    OpcodeInfo("LDX",   AddrMode.AbsoluteY,     False),     #$be
    OpcodeInfo("LAX",   AddrMode.AbsoluteY,     False),     #$bf
    OpcodeInfo("CPY",   AddrMode.Immediate,     False),     #$c0
    OpcodeInfo("CMP",   AddrMode.IndirectX,     False),     #$c1
    OpcodeInfo("NOOP",  AddrMode.Immediate,     False),     #$c2
    OpcodeInfo("DCP",   AddrMode.IndirectX,     False),     #$c3
    OpcodeInfo("CPY",   AddrMode.ZeroPage,      False),     #$c4
    OpcodeInfo("CMP",   AddrMode.ZeroPage,      False),     #$c5
    OpcodeInfo("DEC",   AddrMode.ZeroPage,      False),     #$c6
    OpcodeInfo("DCP",   AddrMode.ZeroPage,      False),     #$c7
    OpcodeInfo("INY",   AddrMode.Implied,       False),     #$c8
    OpcodeInfo("CMP",   AddrMode.Immediate,     False),     #$c9
    OpcodeInfo("DEX",   AddrMode.Implied,       False),     #$ca
    OpcodeInfo("SBX",   AddrMode.Immediate,     False),     #$cb
    OpcodeInfo("CPY",   AddrMode.Absolute,      False),     #$cc
    OpcodeInfo("CMP",   AddrMode.Absolute,      False),     #$cd
    OpcodeInfo("DEC",   AddrMode.Absolute,      False),     #$ce
    OpcodeInfo("DCP",   AddrMode.Absolute,      False),     #$cf
    OpcodeInfo("BNE",   AddrMode.Relative,      True ),     #$d0
    OpcodeInfo("CMP",   AddrMode.IndirectY,     False),     #$d1
    OpcodeInfo("JAM",   AddrMode.Implied,       False),     #$d2
    OpcodeInfo("DCP",   AddrMode.IndirectY,     False),     #$d3
    OpcodeInfo("NOOP",  AddrMode.ZeroPageX,     False),     #$d4
    OpcodeInfo("CMP",   AddrMode.ZeroPageX,     False),     #$d5
    OpcodeInfo("DEC",   AddrMode.ZeroPageX,     False),     #$d6
    OpcodeInfo("DCP",   AddrMode.ZeroPageX,     False),     #$d7
    OpcodeInfo("CLD",   AddrMode.Implied,       False),     #$d8
    OpcodeInfo("CMP",   AddrMode.AbsoluteY,     False),     #$d9
    OpcodeInfo("NOOP",  AddrMode.Implied,       False),     #$da
    OpcodeInfo("DCP",   AddrMode.AbsoluteY,     False),     #$db
    OpcodeInfo("NOOP",  AddrMode.AbsoluteX,     False),     #$dc
    OpcodeInfo("CMP",   AddrMode.AbsoluteX,     False),     #$dd
    OpcodeInfo("DEC",   AddrMode.AbsoluteX,     False),     #$de
    OpcodeInfo("DCP",   AddrMode.AbsoluteX,     False),     #$df
    OpcodeInfo("CPX",   AddrMode.Immediate,     False),     #$e0
    OpcodeInfo("SBC",   AddrMode.IndirectX,     False),     #$e1
    OpcodeInfo("NOOP",  AddrMode.Immediate,     False),     #$e2
    OpcodeInfo("ISB",   AddrMode.IndirectX,     False),     #$e3
    OpcodeInfo("CPX",   AddrMode.ZeroPage,      False),     #$e4
    OpcodeInfo("SBC",   AddrMode.ZeroPage,      False),     #$e5
    OpcodeInfo("INC",   AddrMode.ZeroPage,      False),     #$e6
    OpcodeInfo("ISB",   AddrMode.ZeroPage,      False),     #$e7
    OpcodeInfo("INX",   AddrMode.Implied,       False),     #$e8
    OpcodeInfo("SBC",   AddrMode.Immediate,     False),     #$e9
    OpcodeInfo("NOP",   AddrMode.Implied,       False),     #$ea
    OpcodeInfo("USBC",  AddrMode.Immediate,     False),     #$eb
    OpcodeInfo("CPX",   AddrMode.Absolute,      False),     #$ec
    OpcodeInfo("SBC",   AddrMode.Absolute,      False),     #$ed
    OpcodeInfo("INC",   AddrMode.Absolute,      False),     #$ee
    OpcodeInfo("ISB",   AddrMode.Absolute,      False),     #$ef
    OpcodeInfo("BEQ",   AddrMode.Relative,      True ),     #$f0
    OpcodeInfo("SBC",   AddrMode.IndirectY,     False),     #$f1
    OpcodeInfo("JAM",   AddrMode.Implied,       False),     #$f2
    OpcodeInfo("ISB",   AddrMode.IndirectY,     False),     #$f3
    OpcodeInfo("NOOP",  AddrMode.ZeroPageX,     False),     #$f4
    OpcodeInfo("SBC",   AddrMode.ZeroPageX,     False),     #$f5
    OpcodeInfo("INC",   AddrMode.ZeroPageX,     False),     #$f6
    OpcodeInfo("ISB",   AddrMode.ZeroPageX,     False),     #$f7
    OpcodeInfo("SED",   AddrMode.Implied,       False),     #$f8
    OpcodeInfo("SBC",   AddrMode.AbsoluteY,     False),     #$f9
    OpcodeInfo("NOOP",  AddrMode.Implied,       False),     #$fa
    OpcodeInfo("ISB",   AddrMode.AbsoluteY,     False),     #$fb
    OpcodeInfo("NOOP",  AddrMode.AbsoluteX,     False),     #$fc
    OpcodeInfo("SBC",   AddrMode.AbsoluteX,     False),     #$fd
    OpcodeInfo("INC",   AddrMode.AbsoluteX,     False),     #$fe
    OpcodeInfo("ISB",   AddrMode.Absolute,      False)      #$ff
    ]

def s8_to_int(x):
    return (x^0x80)-0x80;

InstructionInfo = namedtuple("InstructionInfo", "ivl, opcode, operand, target, op_info, mode_info")
def M6502Iterator(mem, ivl, hide_a=False):
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
            target = addr+s8_to_int(operand)+2
        elif mode_info.has_address:
            target = operand
        else:
            target = None

        # ACME assembler uses "ASL" instead of "ASL A"
        if hide_a and op_info.mode==AddrMode.Accumulator:
            mode_info = ModeInfo(0, False, "", "")

        yield InstructionInfo(Interval(addr, addr+mode_info.operand_size), opcode, operand, target, op_info, mode_info)

        addr += mode_info.operand_size+1
