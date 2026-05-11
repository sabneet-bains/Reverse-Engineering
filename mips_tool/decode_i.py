"""I-type, REGIMM, and J-type instruction decoders."""

from collections.abc import Callable

from .encoding import EncodedInstruction, i_fields, j_fields
from .errors import UnsupportedInstructionError
from .parser import sign_extend
from .registers import gpr_name
from .tables import I_BY_OPCODE, J_BY_OPCODE, REGIMM_BY_RT, InstructionSpec
from .word import InstructionWord

type IDecoder = Callable[[InstructionWord, InstructionSpec, int | None], str]


def decode_i(instruction_word: InstructionWord) -> EncodedInstruction:
    instruction_spec = I_BY_OPCODE[instruction_word.opcode]
    signed_immediate = sign_extend(instruction_word.immediate, 16)
    handler = I_DECODERS.get(instruction_spec.kind)
    if handler is None:
        raise UnsupportedInstructionError(f"unsupported I-type form: {instruction_spec.kind}")

    assembly = handler(instruction_word, instruction_spec, signed_immediate)
    fields = i_fields(
        instruction_spec.mnemonic,
        instruction_word.opcode,
        instruction_word.rs,
        instruction_word.rt,
        instruction_word.immediate,
    )
    return EncodedInstruction(instruction_word.value, assembly, fields)


def decode_regimm(instruction_word: InstructionWord) -> EncodedInstruction:
    instruction_spec = REGIMM_BY_RT.get(instruction_word.rt)
    if instruction_spec is None:
        raise UnsupportedInstructionError(f"unsupported REGIMM rt field: 0b{instruction_word.rt:05b}")

    signed_immediate = sign_extend(instruction_word.immediate, 16)
    assembly = f"{instruction_spec.mnemonic} {gpr_name(instruction_word.rs)}, {signed_immediate}"
    fields = i_fields(
        instruction_spec.mnemonic,
        instruction_word.opcode,
        instruction_word.rs,
        instruction_word.rt,
        instruction_word.immediate,
    )
    return EncodedInstruction(instruction_word.value, assembly, fields)


def decode_jump(instruction_word: InstructionWord) -> EncodedInstruction:
    instruction_spec = J_BY_OPCODE[instruction_word.opcode]
    assembly = f"{instruction_spec.mnemonic} {hex(instruction_word.address)}"
    fields = j_fields(instruction_spec.mnemonic, instruction_word.opcode, instruction_word.address)
    return EncodedInstruction(instruction_word.value, assembly, fields)


def _decode_i_rt_rs_imm(
    instruction_word: InstructionWord,
    instruction_spec: InstructionSpec,
    signed_immediate: int | None,
) -> str:
    immediate_display = instruction_word.immediate if instruction_spec.mnemonic in {"andi", "ori", "xori"} else signed_immediate
    return f"{instruction_spec.mnemonic} {gpr_name(instruction_word.rt)}, {gpr_name(instruction_word.rs)}, {immediate_display}"


def _decode_lui(
    instruction_word: InstructionWord,
    instruction_spec: InstructionSpec,
    signed_immediate: int | None,
) -> str:
    return f"{instruction_spec.mnemonic} {gpr_name(instruction_word.rt)}, {instruction_word.immediate}"


def _decode_mem(instruction_word: InstructionWord, instruction_spec: InstructionSpec, signed_immediate: int | None) -> str:
    return f"{instruction_spec.mnemonic} {gpr_name(instruction_word.rt)}, {signed_immediate}({gpr_name(instruction_word.rs)})"


def _decode_branch2(instruction_word: InstructionWord, instruction_spec: InstructionSpec, signed_immediate: int | None) -> str:
    return f"{instruction_spec.mnemonic} {gpr_name(instruction_word.rs)}, {gpr_name(instruction_word.rt)}, {signed_immediate}"


def _decode_branch1(instruction_word: InstructionWord, instruction_spec: InstructionSpec, signed_immediate: int | None) -> str:
    return f"{instruction_spec.mnemonic} {gpr_name(instruction_word.rs)}, {signed_immediate}"


# Render handlers mirror the encoder forms one-to-one where possible.
I_DECODERS: dict[str, IDecoder] = {
    "i_rt_rs_imm": _decode_i_rt_rs_imm,
    "lui": _decode_lui,
    "mem": _decode_mem,
    "branch2": _decode_branch2,
    "branch1": _decode_branch1,
}
