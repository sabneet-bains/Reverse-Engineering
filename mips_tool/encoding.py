"""Shared machine-word packing and bitfield result structures."""

from dataclasses import dataclass

from .parser import sign_extend
from .registers import gpr_name


@dataclass(frozen=True, slots=True)
class Field:
    """A named bitfield inside a 32-bit instruction word."""
    name: str
    high: int
    low: int
    value: int
    meaning: str = ""

    @property
    def width(self) -> int:
        return self.high - self.low + 1

    @property
    def bits(self) -> str:
        return format(self.value & ((1 << self.width) - 1), f"0{self.width}b")


@dataclass(frozen=True, slots=True)
class EncodedInstruction:
    """Machine word plus canonical assembly and field metadata."""
    word: int
    assembly: str
    fields: tuple[Field, ...]
    source: str | None = None
    expanded_from: str | None = None

    @property
    def binary(self) -> str:
        return format(self.word, "032b")

    @property
    def hex(self) -> str:
        return f"0x{self.word:08X}"


def pack_r(opcode: int, rs: int, rt: int, rd: int, shamt: int, funct: int) -> int:
    """Pack an R-type instruction word."""
    return (opcode << 26) | (rs << 21) | (rt << 16) | (rd << 11) | (shamt << 6) | funct


def pack_i(opcode: int, rs: int, rt: int, immediate: int) -> int:
    """Pack an I-type instruction word."""
    return (opcode << 26) | (rs << 21) | (rt << 16) | (immediate & 0xFFFF)


def pack_j(opcode: int, address: int) -> int:
    """Pack a J-type instruction word."""
    return (opcode << 26) | (address & 0x03FFFFFF)


def r_fields(mnemonic: str, rs: int, rt: int, rd: int, shamt: int, funct: int) -> tuple[Field, ...]:
    return (
        Field("opcode", 31, 26, 0, "SPECIAL"),
        Field("rs", 25, 21, rs, gpr_name(rs)),
        Field("rt", 20, 16, rt, gpr_name(rt)),
        Field("rd", 15, 11, rd, gpr_name(rd)),
        Field("shamt", 10, 6, shamt, str(shamt)),
        Field("funct", 5, 0, funct, mnemonic),
    )


def i_fields(mnemonic: str, opcode: int, rs: int, rt: int, immediate: int) -> tuple[Field, ...]:
    return (
        Field("opcode", 31, 26, opcode, mnemonic),
        Field("rs", 25, 21, rs, gpr_name(rs)),
        Field("rt", 20, 16, rt, gpr_name(rt)),
        Field("immediate", 15, 0, immediate & 0xFFFF, str(sign_extend(immediate, 16))),
    )


def j_fields(mnemonic: str, opcode: int, address: int) -> tuple[Field, ...]:
    return (
        Field("opcode", 31, 26, opcode, mnemonic),
        Field("address", 25, 0, address, hex(address)),
    )
