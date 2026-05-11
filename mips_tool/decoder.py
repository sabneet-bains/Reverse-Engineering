"""Decode 32-bit MIPS words into canonical assembly and bitfield metadata."""

from .decode_coprocessor import decode_cop0, decode_fpu
from .decode_i import decode_i, decode_jump, decode_regimm
from .decode_r import decode_special
from .encoding import EncodedInstruction
from .errors import UnsupportedInstructionError
from .tables import I_BY_OPCODE, J_BY_OPCODE
from .word import InstructionWord


def decode_instruction(word: int | str) -> EncodedInstruction:
    """Decode one 32-bit instruction word into canonical assembly and fields."""
    instruction_word = InstructionWord.parse(word)
    if instruction_word.opcode == 0x00:
        return decode_special(instruction_word)
    if instruction_word.opcode == 0x01:
        return decode_regimm(instruction_word)
    if instruction_word.opcode in J_BY_OPCODE:
        return decode_jump(instruction_word)
    if instruction_word.opcode == 0x10:
        return decode_cop0(instruction_word)
    if instruction_word.opcode == 0x11:
        return decode_fpu(instruction_word)
    if instruction_word.opcode in I_BY_OPCODE:
        return decode_i(instruction_word)
    raise UnsupportedInstructionError(f"unsupported opcode: 0b{instruction_word.opcode:06b}")


def parse_word(word: int | str) -> int:
    """Parse a binary, decimal, or hexadecimal instruction word into an integer."""
    return InstructionWord.parse(word).value
