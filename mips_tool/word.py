"""A named view over the fixed bitfields in a 32-bit MIPS instruction."""

from dataclasses import dataclass
from typing import Self

from .errors import OperandError


@dataclass(frozen=True, slots=True)
class InstructionWord:
    """Named view over the fixed bitfields in a 32-bit MIPS instruction."""

    value: int
    opcode: int
    rs: int
    rt: int
    rd: int
    shamt: int
    funct: int
    immediate: int
    address: int

    @classmethod
    def parse(cls, word: int | str) -> Self:
        if isinstance(word, int):
            value = word
        else:
            text = word.strip().replace("_", "")
            base = 2 if set(text) <= {"0", "1"} and len(text) == 32 else 0
            try:
                value = int(text, base)
            except ValueError as exc:
                raise OperandError(f"invalid instruction word: {word}") from exc
        if not 0 <= value <= 0xFFFFFFFF:
            raise OperandError(f"instruction word out of range: {word}")
        return cls(
            value=value,
            opcode=(value >> 26) & 0x3F,
            rs=(value >> 21) & 0x1F,
            rt=(value >> 16) & 0x1F,
            rd=(value >> 11) & 0x1F,
            shamt=(value >> 6) & 0x1F,
            funct=value & 0x3F,
            immediate=value & 0xFFFF,
            address=value & 0x03FFFFFF,
        )

    def bits(self, high: int, low: int) -> int:
        width = high - low + 1
        return (self.value >> low) & ((1 << width) - 1)
