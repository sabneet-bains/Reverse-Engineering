"""FPU and COP0 instruction decoders."""

from .encoding import EncodedInstruction, Field
from .errors import UnsupportedInstructionError
from .registers import cop0_name, fpr_name, gpr_name
from .tables import COP0_MOVE_BY_RS, COP0_SPECS, FPU_BY_FMT_FUNCT, FPU_MOVE_BY_RS, InstructionSpec
from .word import InstructionWord


def decode_fpu(instruction_word: InstructionWord) -> EncodedInstruction:
    if instruction_word.rs in FPU_MOVE_BY_RS:
        return _decode_fpu_move(instruction_word, FPU_MOVE_BY_RS[instruction_word.rs])

    instruction_spec = FPU_BY_FMT_FUNCT.get((instruction_word.rs, instruction_word.funct))
    if instruction_spec is None:
        raise UnsupportedInstructionError("unsupported COP1 instruction")
    return _decode_fpu3(instruction_word, instruction_spec)


def decode_cop0(instruction_word: InstructionWord) -> EncodedInstruction:
    eret_spec = COP0_SPECS["eret"]
    if instruction_word.rs == eret_spec.rs_code and instruction_word.funct == eret_spec.funct:
        return _decode_eret(instruction_word)

    instruction_spec = COP0_MOVE_BY_RS.get(instruction_word.rs)
    if instruction_spec is None:
        raise UnsupportedInstructionError("unsupported COP0 instruction")
    return _decode_cop0_move(instruction_word, instruction_spec)


# COP1 arithmetic: render fmt/ft/fs/fd/funct back to canonical FPU assembly.
def _decode_fpu3(instruction_word: InstructionWord, instruction_spec: InstructionSpec) -> EncodedInstruction:
    fs = instruction_word.rd
    fd = instruction_word.shamt
    assembly = f"{instruction_spec.mnemonic} {fpr_name(fd)}, {fpr_name(fs)}, {fpr_name(instruction_word.rt)}"
    fields = (
        Field("opcode", 31, 26, 0x11, "COP1"),
        Field("fmt", 25, 21, instruction_word.rs, instruction_spec.mnemonic[-1]),
        Field("ft", 20, 16, instruction_word.rt, fpr_name(instruction_word.rt)),
        Field("fs", 15, 11, fs, fpr_name(fs)),
        Field("fd", 10, 6, fd, fpr_name(fd)),
        Field("funct", 5, 0, instruction_word.funct, instruction_spec.mnemonic),
    )
    return EncodedInstruction(instruction_word.value, assembly, fields)


# COP1 moves: render GPR <-> FPR transfer fields.
def _decode_fpu_move(instruction_word: InstructionWord, instruction_spec: InstructionSpec) -> EncodedInstruction:
    assembly = f"{instruction_spec.mnemonic} {gpr_name(instruction_word.rt)}, {fpr_name(instruction_word.rd)}"
    fields = (
        Field("opcode", 31, 26, 0x11, "COP1"),
        Field("rs", 25, 21, instruction_word.rs, instruction_spec.mnemonic),
        Field("rt", 20, 16, instruction_word.rt, gpr_name(instruction_word.rt)),
        Field("fs", 15, 11, instruction_word.rd, fpr_name(instruction_word.rd)),
        Field("zero", 10, 0, instruction_word.bits(10, 0), ""),
    )
    return EncodedInstruction(instruction_word.value, assembly, fields)


# COP0 system control: exception return has no operands.
def _decode_eret(instruction_word: InstructionWord) -> EncodedInstruction:
    fields = (
        Field("opcode", 31, 26, 0x10, "COP0"),
        Field("rs", 25, 21, instruction_word.rs, "CO"),
        Field("zero", 20, 6, 0, ""),
        Field("funct", 5, 0, instruction_word.funct, "eret"),
    )
    return EncodedInstruction(instruction_word.value, "eret", fields)


# COP0 moves: render GPR <-> system-control register fields.
def _decode_cop0_move(instruction_word: InstructionWord, instruction_spec: InstructionSpec) -> EncodedInstruction:
    assembly = f"{instruction_spec.mnemonic} {gpr_name(instruction_word.rt)}, {cop0_name(instruction_word.rd)}"
    fields = (
        Field("opcode", 31, 26, 0x10, "COP0"),
        Field("rs", 25, 21, instruction_word.rs, instruction_spec.mnemonic),
        Field("rt", 20, 16, instruction_word.rt, gpr_name(instruction_word.rt)),
        Field("rd", 15, 11, instruction_word.rd, cop0_name(instruction_word.rd)),
        Field("zero", 10, 0, instruction_word.bits(10, 0), ""),
    )
    return EncodedInstruction(instruction_word.value, assembly, fields)
