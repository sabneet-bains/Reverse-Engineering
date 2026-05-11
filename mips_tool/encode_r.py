"""R-type operand-form encoders."""

from collections.abc import Callable

from .encoding import EncodedInstruction, pack_r, r_fields
from .errors import OperandError
from .operands import EncodeContext, Operands
from .parser import ParsedInstruction, parse_int, require_range
from .registers import gpr_name, parse_gpr
from .tables import InstructionSpec

type EncodeHandler = Callable[[ParsedInstruction, InstructionSpec, EncodeContext], EncodedInstruction]


def _encode_r3(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    rd_token, rs_token, rt_token = Operands(parsed).expect(3)
    rd, rs, rt = parse_gpr(rd_token), parse_gpr(rs_token), parse_gpr(rt_token)
    assembly = f"{instruction_spec.mnemonic} {gpr_name(rd)}, {gpr_name(rs)}, {gpr_name(rt)}"
    return _build_r_instruction(parsed, instruction_spec, rs, rt, rd, 0, assembly)


def _encode_shift(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    rd_token, rt_token, shamt_token = Operands(parsed).expect(3)
    rd, rt = parse_gpr(rd_token), parse_gpr(rt_token)
    shamt = require_range(parse_int(shamt_token), 5, signed=False, what="shift amount")
    assembly = f"{instruction_spec.mnemonic} {gpr_name(rd)}, {gpr_name(rt)}, {shamt}"
    return _build_r_instruction(parsed, instruction_spec, 0, rt, rd, shamt, assembly)


def _encode_shiftv(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    rd_token, rt_token, rs_token = Operands(parsed).expect(3)
    rd, rt, rs = parse_gpr(rd_token), parse_gpr(rt_token), parse_gpr(rs_token)
    assembly = f"{instruction_spec.mnemonic} {gpr_name(rd)}, {gpr_name(rt)}, {gpr_name(rs)}"
    return _build_r_instruction(parsed, instruction_spec, rs, rt, rd, 0, assembly)


def _encode_rs(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    (rs_token,) = Operands(parsed).expect(1)
    rs = parse_gpr(rs_token)
    return _build_r_instruction(parsed, instruction_spec, rs, 0, 0, 0, f"{instruction_spec.mnemonic} {gpr_name(rs)}")


def _encode_rd(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    (rd_token,) = Operands(parsed).expect(1)
    rd = parse_gpr(rd_token)
    return _build_r_instruction(parsed, instruction_spec, 0, 0, rd, 0, f"{instruction_spec.mnemonic} {gpr_name(rd)}")


def _encode_rs_rt(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    rs_token, rt_token = Operands(parsed).expect(2)
    rs, rt = parse_gpr(rs_token), parse_gpr(rt_token)
    assembly = f"{instruction_spec.mnemonic} {gpr_name(rs)}, {gpr_name(rt)}"
    return _build_r_instruction(parsed, instruction_spec, rs, rt, 0, 0, assembly)


def _encode_jalr(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    operands = Operands(parsed).values
    if len(operands) == 1:
        rd, rs = 31, parse_gpr(operands[0])
    elif len(operands) == 2:
        rd, rs = parse_gpr(operands[0]), parse_gpr(operands[1])
    else:
        raise OperandError("jalr expects rs or rd, rs")
    assembly = f"{instruction_spec.mnemonic} {gpr_name(rd)}, {gpr_name(rs)}"
    return _build_r_instruction(parsed, instruction_spec, rs, 0, rd, 0, assembly)


def _encode_code20(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    operands = Operands(parsed).values
    if len(operands) > 1:
        raise OperandError(f"{instruction_spec.mnemonic} expects zero or one code operand")
    code = require_range(parse_int(operands[0]), 20, signed=False, what="code") if operands else 0
    rs, rt, rd, shamt = (code >> 15) & 0x1F, (code >> 10) & 0x1F, (code >> 5) & 0x1F, code & 0x1F
    assembly = instruction_spec.mnemonic if not operands else f"{instruction_spec.mnemonic} {code}"
    return _build_r_instruction(parsed, instruction_spec, rs, rt, rd, shamt, assembly)


def _encode_trap_r(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    operands = Operands(parsed).values
    if len(operands) not in {2, 3}:
        raise OperandError(f"{instruction_spec.mnemonic} expects rs, rt[, code]")
    rs, rt = parse_gpr(operands[0]), parse_gpr(operands[1])
    code = require_range(parse_int(operands[2]), 10, signed=False, what="trap code") if len(operands) == 3 else 0
    rd, shamt = (code >> 5) & 0x1F, code & 0x1F
    assembly = f"{instruction_spec.mnemonic} {gpr_name(rs)}, {gpr_name(rt)}" + (f", {code}" if code else "")
    return _build_r_instruction(parsed, instruction_spec, rs, rt, rd, shamt, assembly)


def _build_r_instruction(
    parsed: ParsedInstruction,
    instruction_spec: InstructionSpec,
    rs: int,
    rt: int,
    rd: int,
    shamt: int,
    assembly: str,
) -> EncodedInstruction:
    funct = instruction_spec.funct or 0
    word = pack_r(instruction_spec.opcode, rs, rt, rd, shamt, funct)
    return EncodedInstruction(word, assembly, r_fields(instruction_spec.mnemonic, rs, rt, rd, shamt, funct), source=parsed.text)


# Each form handler accepts the same shape even when a form does not need labels.
R_ENCODERS: dict[str, EncodeHandler] = {
    "r3": _encode_r3,
    "shift": _encode_shift,
    "shiftv": _encode_shiftv,
    "rs": _encode_rs,
    "rd": _encode_rd,
    "rs_rt": _encode_rs_rt,
    "jalr": _encode_jalr,
    "code20": _encode_code20,
    "trap_r": _encode_trap_r,
}
