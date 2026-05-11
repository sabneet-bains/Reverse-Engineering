"""I-type and REGIMM operand-form encoders."""

from collections.abc import Callable

from .encoding import EncodedInstruction, i_fields, pack_i
from .operands import EncodeContext, Operands
from .parser import ParsedInstruction, parse_int, parse_memory_operand, require_range
from .registers import gpr_name, parse_gpr
from .tables import InstructionSpec

type EncodeHandler = Callable[[ParsedInstruction, InstructionSpec, EncodeContext], EncodedInstruction]


def _encode_i_rt_rs_imm(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    rt_token, rs_token, immediate_token = Operands(parsed).expect(3)
    rt, rs = parse_gpr(rt_token), parse_gpr(rs_token)
    immediate_value = parse_int(immediate_token)
    signed = instruction_spec.mnemonic not in {"andi", "ori", "xori"}
    immediate = require_range(immediate_value, 16, signed=signed, what="immediate")
    assembly = f"{instruction_spec.mnemonic} {gpr_name(rt)}, {gpr_name(rs)}, {immediate_value}"
    return _build_i_instruction(parsed, instruction_spec, rs, rt, immediate, assembly)


def _encode_lui(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    rt_token, immediate_token = Operands(parsed).expect(2)
    rt = parse_gpr(rt_token)
    immediate = require_range(parse_int(immediate_token), 16, signed=False, what="immediate")
    assembly = f"lui {gpr_name(rt)}, {immediate}"
    return _build_i_instruction(parsed, instruction_spec, 0, rt, immediate, assembly)


def _encode_mem(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    rt_token, memory_token = Operands(parsed).expect(2)
    rt = parse_gpr(rt_token)
    immediate, rs = parse_memory_operand(memory_token)
    assembly = f"{instruction_spec.mnemonic} {gpr_name(rt)}, {sign_value(immediate, 16)}({gpr_name(rs)})"
    return _build_i_instruction(parsed, instruction_spec, rs, rt, immediate, assembly)


def _encode_branch2(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    rs_token, rt_token, target_token = Operands(parsed).expect(3)
    rs, rt = parse_gpr(rs_token), parse_gpr(rt_token)
    immediate = _branch_offset(target_token, context.address, context.labels)
    assembly = f"{instruction_spec.mnemonic} {gpr_name(rs)}, {gpr_name(rt)}, {sign_value(immediate, 16)}"
    return _build_i_instruction(parsed, instruction_spec, rs, rt, immediate, assembly)


def _encode_branch1(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    rs_token, target_token = Operands(parsed).expect(2)
    rs = parse_gpr(rs_token)
    immediate = _branch_offset(target_token, context.address, context.labels)
    assembly = f"{instruction_spec.mnemonic} {gpr_name(rs)}, {sign_value(immediate, 16)}"
    return _build_i_instruction(parsed, instruction_spec, rs, 0, immediate, assembly)


def _encode_regimm(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    rs_token, target_token = Operands(parsed).expect(2)
    rs, rt = parse_gpr(rs_token), instruction_spec.rt_code or 0
    immediate = _branch_offset(target_token, context.address, context.labels)
    assembly = f"{instruction_spec.mnemonic} {gpr_name(rs)}, {sign_value(immediate, 16)}"
    return _build_i_instruction(parsed, instruction_spec, rs, rt, immediate, assembly)


def _encode_trap_i(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    rs_token, immediate_token = Operands(parsed).expect(2)
    rs, rt = parse_gpr(rs_token), instruction_spec.rt_code or 0
    immediate = require_range(parse_int(immediate_token), 16, signed=True, what="trap immediate")
    assembly = f"{instruction_spec.mnemonic} {gpr_name(rs)}, {sign_value(immediate, 16)}"
    return _build_i_instruction(parsed, instruction_spec, rs, rt, immediate, assembly)


def _build_i_instruction(
    parsed: ParsedInstruction,
    instruction_spec: InstructionSpec,
    rs: int,
    rt: int,
    immediate: int,
    assembly: str,
) -> EncodedInstruction:
    word = pack_i(instruction_spec.opcode, rs, rt, immediate)
    return EncodedInstruction(
        word,
        assembly,
        i_fields(instruction_spec.mnemonic, instruction_spec.opcode, rs, rt, immediate),
        source=parsed.text,
    )


def _branch_offset(token: str, address: int, labels: dict[str, int]) -> int:
    if token in labels:
        delta = (labels[token] - (address + 4)) // 4
        return require_range(delta, 16, signed=True, what="branch offset")
    return require_range(parse_int(token), 16, signed=True, what="branch offset")


def sign_value(value: int, bits: int) -> int:
    """Interpret `value` as a signed two's-complement integer of `bits` width."""
    sign = 1 << (bits - 1)
    value &= (1 << bits) - 1
    return value - (1 << bits) if value & sign else value


# Each form handler accepts the same shape so dispatch stays predictable.
I_ENCODERS: dict[str, EncodeHandler] = {
    "i_rt_rs_imm": _encode_i_rt_rs_imm,
    "lui": _encode_lui,
    "mem": _encode_mem,
    "branch2": _encode_branch2,
    "branch1": _encode_branch1,
    "regimm": _encode_regimm,
    "trap_i": _encode_trap_i,
}
