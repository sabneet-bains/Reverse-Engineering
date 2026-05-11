"""Instruction metadata tables shared by the encoder and decoder."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InstructionSpec:
    """Static encoding metadata for one supported instruction mnemonic."""
    mnemonic: str
    kind: str
    opcode: int
    funct: int | None = None
    rt_code: int | None = None
    fmt: int | None = None
    rs_code: int | None = None


# R-type / SPECIAL: register-register arithmetic, shifts, HI/LO, traps.
R_SPECS = {
    "add": InstructionSpec("add", "r3", 0x00, 0x20),
    "addu": InstructionSpec("addu", "r3", 0x00, 0x21),
    "sub": InstructionSpec("sub", "r3", 0x00, 0x22),
    "subu": InstructionSpec("subu", "r3", 0x00, 0x23),
    "and": InstructionSpec("and", "r3", 0x00, 0x24),
    "or": InstructionSpec("or", "r3", 0x00, 0x25),
    "xor": InstructionSpec("xor", "r3", 0x00, 0x26),
    "nor": InstructionSpec("nor", "r3", 0x00, 0x27),
    "slt": InstructionSpec("slt", "r3", 0x00, 0x2A),
    "sltu": InstructionSpec("sltu", "r3", 0x00, 0x2B),
    "dadd": InstructionSpec("dadd", "r3", 0x00, 0x2C),
    "daddu": InstructionSpec("daddu", "r3", 0x00, 0x2D),
    "dsub": InstructionSpec("dsub", "r3", 0x00, 0x2E),
    "dsubu": InstructionSpec("dsubu", "r3", 0x00, 0x2F),
    "sll": InstructionSpec("sll", "shift", 0x00, 0x00),
    "srl": InstructionSpec("srl", "shift", 0x00, 0x02),
    "sra": InstructionSpec("sra", "shift", 0x00, 0x03),
    "dsll": InstructionSpec("dsll", "shift", 0x00, 0x38),
    "dsrl": InstructionSpec("dsrl", "shift", 0x00, 0x3A),
    "dsra": InstructionSpec("dsra", "shift", 0x00, 0x3B),
    "dsll32": InstructionSpec("dsll32", "shift", 0x00, 0x3C),
    "dsrl32": InstructionSpec("dsrl32", "shift", 0x00, 0x3E),
    "dsra32": InstructionSpec("dsra32", "shift", 0x00, 0x3F),
    "sllv": InstructionSpec("sllv", "shiftv", 0x00, 0x04),
    "srlv": InstructionSpec("srlv", "shiftv", 0x00, 0x06),
    "srav": InstructionSpec("srav", "shiftv", 0x00, 0x07),
    "dsllv": InstructionSpec("dsllv", "shiftv", 0x00, 0x14),
    "dsrlv": InstructionSpec("dsrlv", "shiftv", 0x00, 0x16),
    "dsrav": InstructionSpec("dsrav", "shiftv", 0x00, 0x17),
    "jr": InstructionSpec("jr", "rs", 0x00, 0x08),
    "jalr": InstructionSpec("jalr", "jalr", 0x00, 0x09),
    "mfhi": InstructionSpec("mfhi", "rd", 0x00, 0x10),
    "mthi": InstructionSpec("mthi", "rs", 0x00, 0x11),
    "mflo": InstructionSpec("mflo", "rd", 0x00, 0x12),
    "mtlo": InstructionSpec("mtlo", "rs", 0x00, 0x13),
    "mult": InstructionSpec("mult", "rs_rt", 0x00, 0x18),
    "multu": InstructionSpec("multu", "rs_rt", 0x00, 0x19),
    "div": InstructionSpec("div", "rs_rt", 0x00, 0x1A),
    "divu": InstructionSpec("divu", "rs_rt", 0x00, 0x1B),
    "dmult": InstructionSpec("dmult", "rs_rt", 0x00, 0x1C),
    "dmultu": InstructionSpec("dmultu", "rs_rt", 0x00, 0x1D),
    "ddiv": InstructionSpec("ddiv", "rs_rt", 0x00, 0x1E),
    "ddivu": InstructionSpec("ddivu", "rs_rt", 0x00, 0x1F),
    "syscall": InstructionSpec("syscall", "code20", 0x00, 0x0C),
    "break": InstructionSpec("break", "code20", 0x00, 0x0D),
    "tge": InstructionSpec("tge", "trap_r", 0x00, 0x30),
    "tgeu": InstructionSpec("tgeu", "trap_r", 0x00, 0x31),
    "tlt": InstructionSpec("tlt", "trap_r", 0x00, 0x32),
    "tltu": InstructionSpec("tltu", "trap_r", 0x00, 0x33),
    "teq": InstructionSpec("teq", "trap_r", 0x00, 0x34),
    "tne": InstructionSpec("tne", "trap_r", 0x00, 0x36),
}

# I-type / REGIMM: immediates, branches, load/store, trap immediates.
I_SPECS = {
    "addi": InstructionSpec("addi", "i_rt_rs_imm", 0x08),
    "addiu": InstructionSpec("addiu", "i_rt_rs_imm", 0x09),
    "slti": InstructionSpec("slti", "i_rt_rs_imm", 0x0A),
    "sltiu": InstructionSpec("sltiu", "i_rt_rs_imm", 0x0B),
    "andi": InstructionSpec("andi", "i_rt_rs_imm", 0x0C),
    "ori": InstructionSpec("ori", "i_rt_rs_imm", 0x0D),
    "xori": InstructionSpec("xori", "i_rt_rs_imm", 0x0E),
    "daddi": InstructionSpec("daddi", "i_rt_rs_imm", 0x18),
    "daddiu": InstructionSpec("daddiu", "i_rt_rs_imm", 0x19),
    "lui": InstructionSpec("lui", "lui", 0x0F),
    "beq": InstructionSpec("beq", "branch2", 0x04),
    "bne": InstructionSpec("bne", "branch2", 0x05),
    "blez": InstructionSpec("blez", "branch1", 0x06),
    "bgtz": InstructionSpec("bgtz", "branch1", 0x07),
    "bltz": InstructionSpec("bltz", "regimm", 0x01, rt_code=0x00),
    "bgez": InstructionSpec("bgez", "regimm", 0x01, rt_code=0x01),
    "bltzal": InstructionSpec("bltzal", "regimm", 0x01, rt_code=0x10),
    "bgezal": InstructionSpec("bgezal", "regimm", 0x01, rt_code=0x11),
    "lb": InstructionSpec("lb", "mem", 0x20),
    "lh": InstructionSpec("lh", "mem", 0x21),
    "lwl": InstructionSpec("lwl", "mem", 0x22),
    "lw": InstructionSpec("lw", "mem", 0x23),
    "lbu": InstructionSpec("lbu", "mem", 0x24),
    "lhu": InstructionSpec("lhu", "mem", 0x25),
    "lwr": InstructionSpec("lwr", "mem", 0x26),
    "lwu": InstructionSpec("lwu", "mem", 0x27),
    "ldl": InstructionSpec("ldl", "mem", 0x1A),
    "ldr": InstructionSpec("ldr", "mem", 0x1B),
    "ld": InstructionSpec("ld", "mem", 0x37),
    "sb": InstructionSpec("sb", "mem", 0x28),
    "sh": InstructionSpec("sh", "mem", 0x29),
    "swl": InstructionSpec("swl", "mem", 0x2A),
    "sw": InstructionSpec("sw", "mem", 0x2B),
    "swr": InstructionSpec("swr", "mem", 0x2E),
    "sdl": InstructionSpec("sdl", "mem", 0x2C),
    "sdr": InstructionSpec("sdr", "mem", 0x2D),
    "sd": InstructionSpec("sd", "mem", 0x3F),
    "teqi": InstructionSpec("teqi", "trap_i", 0x01, rt_code=0x0C),
    "tnei": InstructionSpec("tnei", "trap_i", 0x01, rt_code=0x0E),
}

# J-type: absolute jump target field.
J_SPECS = {
    "j": InstructionSpec("j", "jump", 0x02),
    "jal": InstructionSpec("jal", "jump", 0x03),
}

# COP1 / FPU: representative single/double arithmetic and GPR-FPR moves.
FPU_SPECS = {
    "add.s": InstructionSpec("add.s", "fpu3", 0x11, funct=0x00, fmt=0x10),
    "sub.s": InstructionSpec("sub.s", "fpu3", 0x11, funct=0x01, fmt=0x10),
    "mul.s": InstructionSpec("mul.s", "fpu3", 0x11, funct=0x02, fmt=0x10),
    "div.s": InstructionSpec("div.s", "fpu3", 0x11, funct=0x03, fmt=0x10),
    "add.d": InstructionSpec("add.d", "fpu3", 0x11, funct=0x00, fmt=0x11),
    "sub.d": InstructionSpec("sub.d", "fpu3", 0x11, funct=0x01, fmt=0x11),
    "mul.d": InstructionSpec("mul.d", "fpu3", 0x11, funct=0x02, fmt=0x11),
    "div.d": InstructionSpec("div.d", "fpu3", 0x11, funct=0x03, fmt=0x11),
    "mfc1": InstructionSpec("mfc1", "cop1_move", 0x11, rs_code=0x00),
    "mtc1": InstructionSpec("mtc1", "cop1_move", 0x11, rs_code=0x04),
}

# COP0: representative system-control moves and exception return.
COP0_SPECS = {
    "mfc0": InstructionSpec("mfc0", "cop0_move", 0x10, rs_code=0x00),
    "mtc0": InstructionSpec("mtc0", "cop0_move", 0x10, rs_code=0x04),
    "eret": InstructionSpec("eret", "eret", 0x10, funct=0x18, rs_code=0x10),
}

# Shared lookup tables keep the encoder and decoder using the same facts.
ALL_SPECS = {}
for group in (R_SPECS, I_SPECS, J_SPECS, FPU_SPECS, COP0_SPECS):
    ALL_SPECS.update(group)

SPECIAL_BY_FUNCT = {
    instruction_spec.funct: instruction_spec
    for instruction_spec in R_SPECS.values()
    if instruction_spec.funct is not None
}
I_BY_OPCODE = {
    instruction_spec.opcode: instruction_spec
    for instruction_spec in I_SPECS.values()
    if instruction_spec.kind != "regimm"
}
REGIMM_BY_RT = {
    instruction_spec.rt_code: instruction_spec
    for instruction_spec in I_SPECS.values()
    if instruction_spec.kind in {"regimm", "trap_i"}
}
J_BY_OPCODE = {instruction_spec.opcode: instruction_spec for instruction_spec in J_SPECS.values()}
FPU_BY_FMT_FUNCT = {
    (instruction_spec.fmt, instruction_spec.funct): instruction_spec
    for instruction_spec in FPU_SPECS.values()
    if instruction_spec.kind == "fpu3"
}
FPU_MOVE_BY_RS = {
    instruction_spec.rs_code: instruction_spec
    for instruction_spec in FPU_SPECS.values()
    if instruction_spec.kind == "cop1_move"
}
COP0_MOVE_BY_RS = {
    instruction_spec.rs_code: instruction_spec
    for instruction_spec in COP0_SPECS.values()
    if instruction_spec.kind == "cop0_move"
}
