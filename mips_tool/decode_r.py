"""R-type and SPECIAL instruction decoders."""

from collections.abc import Callable

from .encoding import EncodedInstruction, r_fields
from .errors import UnsupportedInstructionError
from .registers import gpr_name
from .tables import SPECIAL_BY_FUNCT, InstructionSpec
from .word import InstructionWord

type SpecialDecoder = Callable[[InstructionWord, InstructionSpec], str]


def decode_special(instruction_word: InstructionWord) -> EncodedInstruction:
    instruction_spec = SPECIAL_BY_FUNCT.get(instruction_word.funct)
    if instruction_spec is None:
        raise UnsupportedInstructionError(f"unsupported SPECIAL funct: 0b{instruction_word.funct:06b}")

    handler = SPECIAL_DECODERS.get(instruction_spec.kind)
    if handler is None:
        raise UnsupportedInstructionError(f"unsupported SPECIAL form: {instruction_spec.kind}")

    assembly = handler(instruction_word, instruction_spec)
    fields = r_fields(
        instruction_spec.mnemonic,
        instruction_word.rs,
        instruction_word.rt,
        instruction_word.rd,
        instruction_word.shamt,
        instruction_word.funct,
    )
    return EncodedInstruction(instruction_word.value, assembly, fields)


def _decode_r3(instruction_word: InstructionWord, instruction_spec: InstructionSpec) -> str:
    return (
        f"{instruction_spec.mnemonic} "
        f"{gpr_name(instruction_word.rd)}, {gpr_name(instruction_word.rs)}, {gpr_name(instruction_word.rt)}"
    )


def _decode_shift(instruction_word: InstructionWord, instruction_spec: InstructionSpec) -> str:
    return f"{instruction_spec.mnemonic} {gpr_name(instruction_word.rd)}, {gpr_name(instruction_word.rt)}, {instruction_word.shamt}"


def _decode_shiftv(instruction_word: InstructionWord, instruction_spec: InstructionSpec) -> str:
    return (
        f"{instruction_spec.mnemonic} "
        f"{gpr_name(instruction_word.rd)}, {gpr_name(instruction_word.rt)}, {gpr_name(instruction_word.rs)}"
    )


def _decode_rs(instruction_word: InstructionWord, instruction_spec: InstructionSpec) -> str:
    return f"{instruction_spec.mnemonic} {gpr_name(instruction_word.rs)}"


def _decode_rd(instruction_word: InstructionWord, instruction_spec: InstructionSpec) -> str:
    return f"{instruction_spec.mnemonic} {gpr_name(instruction_word.rd)}"


def _decode_rs_rt(instruction_word: InstructionWord, instruction_spec: InstructionSpec) -> str:
    return f"{instruction_spec.mnemonic} {gpr_name(instruction_word.rs)}, {gpr_name(instruction_word.rt)}"


def _decode_jalr(instruction_word: InstructionWord, instruction_spec: InstructionSpec) -> str:
    return f"{instruction_spec.mnemonic} {gpr_name(instruction_word.rd)}, {gpr_name(instruction_word.rs)}"


def _decode_code20(instruction_word: InstructionWord, instruction_spec: InstructionSpec) -> str:
    code_operand = (
        (instruction_word.rs << 15)
        | (instruction_word.rt << 10)
        | (instruction_word.rd << 5)
        | instruction_word.shamt
    )
    return instruction_spec.mnemonic if code_operand == 0 else f"{instruction_spec.mnemonic} {code_operand}"


def _decode_trap_r(instruction_word: InstructionWord, instruction_spec: InstructionSpec) -> str:
    trap_code = (instruction_word.rd << 5) | instruction_word.shamt
    assembly = f"{instruction_spec.mnemonic} {gpr_name(instruction_word.rs)}, {gpr_name(instruction_word.rt)}"
    return assembly + (f", {trap_code}" if trap_code else "")


# Render handlers mirror the encoder forms one-to-one where possible.
SPECIAL_DECODERS: dict[str, SpecialDecoder] = {
    "r3": _decode_r3,
    "shift": _decode_shift,
    "shiftv": _decode_shiftv,
    "rs": _decode_rs,
    "rd": _decode_rd,
    "rs_rt": _decode_rs_rt,
    "jalr": _decode_jalr,
    "code20": _decode_code20,
    "trap_r": _decode_trap_r,
}
