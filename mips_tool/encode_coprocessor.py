"""FPU and COP0 operand-form encoders."""

from collections.abc import Callable

from .encoding import EncodedInstruction, Field
from .operands import EncodeContext, Operands
from .parser import ParsedInstruction
from .registers import cop0_name, fpr_name, gpr_name, parse_cop0, parse_fpr, parse_gpr
from .tables import InstructionSpec

type EncodeHandler = Callable[[ParsedInstruction, InstructionSpec, EncodeContext], EncodedInstruction]


# COP1 arithmetic: opcode, fmt, ft, fs, fd, funct.
def _encode_fpu3(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    fd_token, fs_token, ft_token = Operands(parsed).expect(3)
    fd, fs, ft = parse_fpr(fd_token), parse_fpr(fs_token), parse_fpr(ft_token)
    word = (instruction_spec.opcode << 26) | ((instruction_spec.fmt or 0) << 21) | (ft << 16) | (fs << 11) | (fd << 6) | (instruction_spec.funct or 0)
    assembly = f"{instruction_spec.mnemonic} {fpr_name(fd)}, {fpr_name(fs)}, {fpr_name(ft)}"
    fields = (
        Field("opcode", 31, 26, instruction_spec.opcode, "COP1"),
        Field("fmt", 25, 21, instruction_spec.fmt or 0, instruction_spec.mnemonic[-1]),
        Field("ft", 20, 16, ft, fpr_name(ft)),
        Field("fs", 15, 11, fs, fpr_name(fs)),
        Field("fd", 10, 6, fd, fpr_name(fd)),
        Field("funct", 5, 0, instruction_spec.funct or 0, instruction_spec.mnemonic),
    )
    return EncodedInstruction(word, assembly, fields, source=parsed.text)


# COP1 moves: transfer between a general-purpose register and an FPU register.
def _encode_cop1_move(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    rt_token, fs_token = Operands(parsed).expect(2)
    rt, fs = parse_gpr(rt_token), parse_fpr(fs_token)
    word = (instruction_spec.opcode << 26) | ((instruction_spec.rs_code or 0) << 21) | (rt << 16) | (fs << 11)
    assembly = f"{instruction_spec.mnemonic} {gpr_name(rt)}, {fpr_name(fs)}"
    fields = (
        Field("opcode", 31, 26, instruction_spec.opcode, "COP1"),
        Field("rs", 25, 21, instruction_spec.rs_code or 0, instruction_spec.mnemonic),
        Field("rt", 20, 16, rt, gpr_name(rt)),
        Field("fs", 15, 11, fs, fpr_name(fs)),
        Field("zero", 10, 0, 0, ""),
    )
    return EncodedInstruction(word, assembly, fields, source=parsed.text)


# COP0 system control: exception return has a fixed CO/funct pattern.
def _encode_eret(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    Operands(parsed).expect(0)
    word = (instruction_spec.opcode << 26) | ((instruction_spec.rs_code or 0) << 21) | (instruction_spec.funct or 0)
    fields = (
        Field("opcode", 31, 26, instruction_spec.opcode, "COP0"),
        Field("rs", 25, 21, instruction_spec.rs_code or 0, "CO"),
        Field("zero", 20, 6, 0, ""),
        Field("funct", 5, 0, instruction_spec.funct or 0, "eret"),
    )
    return EncodedInstruction(word, "eret", fields, source=parsed.text)


# COP0 moves: transfer between a general-purpose register and a COP0 register.
def _encode_cop0_move(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    rt_token, rd_token = Operands(parsed).expect(2)
    rt, rd = parse_gpr(rt_token), parse_cop0(rd_token)
    word = (instruction_spec.opcode << 26) | ((instruction_spec.rs_code or 0) << 21) | (rt << 16) | (rd << 11)
    assembly = f"{instruction_spec.mnemonic} {gpr_name(rt)}, {cop0_name(rd)}"
    fields = (
        Field("opcode", 31, 26, instruction_spec.opcode, "COP0"),
        Field("rs", 25, 21, instruction_spec.rs_code or 0, instruction_spec.mnemonic),
        Field("rt", 20, 16, rt, gpr_name(rt)),
        Field("rd", 15, 11, rd, cop0_name(rd)),
        Field("zero", 10, 0, 0, ""),
    )
    return EncodedInstruction(word, assembly, fields, source=parsed.text)


# Uniform handler maps keep COP1 and COP0 forms parallel to R/I forms.
FPU_ENCODERS: dict[str, EncodeHandler] = {
    "fpu3": _encode_fpu3,
    "cop1_move": _encode_cop1_move,
}

COP0_ENCODERS: dict[str, EncodeHandler] = {
    "cop0_move": _encode_cop0_move,
    "eret": _encode_eret,
}
