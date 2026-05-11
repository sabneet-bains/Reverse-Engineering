"""Pseudo-instruction expansion into real MIPS instructions."""

from .operands import Operands
from .parser import ParsedInstruction, parse_int

PSEUDO_INSTRUCTIONS = ("li", "move", "clear", "nop", "not", "b", "beqz", "bnez")


def expanded_length(parsed: ParsedInstruction) -> int:
    """Return the number of real instructions emitted by a parsed instruction."""
    if parsed.mnemonic == "li":
        operands = Operands(parsed).expect(2)
        immediate_value = parse_int(operands[1])
        return 1 if -(1 << 15) <= immediate_value <= (1 << 15) - 1 else 2
    return 1


def expand_pseudo(parsed: ParsedInstruction) -> list[ParsedInstruction]:
    """Expand supported pseudo-instructions into real MIPS instructions."""
    operands = Operands(parsed)
    if parsed.mnemonic == "move":
        rd, rs = operands.expect(2)
        return [_parsed("addu", rd, rs, "$zero")]
    if parsed.mnemonic == "clear":
        (rd,) = operands.expect(1)
        return [_parsed("addu", rd, "$zero", "$zero")]
    if parsed.mnemonic == "nop":
        operands.expect(0)
        return [_parsed("sll", "$zero", "$zero", "0")]
    if parsed.mnemonic == "not":
        rd, rs = operands.expect(2)
        return [_parsed("nor", rd, rs, "$zero")]
    if parsed.mnemonic == "b":
        (target,) = operands.expect(1)
        return [_parsed("beq", "$zero", "$zero", target)]
    if parsed.mnemonic == "beqz":
        rs, target = operands.expect(2)
        return [_parsed("beq", rs, "$zero", target)]
    if parsed.mnemonic == "bnez":
        rs, target = operands.expect(2)
        return [_parsed("bne", rs, "$zero", target)]
    if parsed.mnemonic == "li":
        rt, immediate_token = operands.expect(2)
        immediate_value = parse_int(immediate_token)
        if -(1 << 15) <= immediate_value <= (1 << 15) - 1:
            return [_parsed("addiu", rt, "$zero", str(immediate_value))]
        unsigned_value = immediate_value & 0xFFFFFFFF
        upper = (unsigned_value >> 16) & 0xFFFF
        lower = unsigned_value & 0xFFFF
        return [_parsed("lui", "$at", str(upper)), _parsed("ori", rt, "$at", str(lower))]
    return [parsed]


def _parsed(mnemonic: str, *operands: str) -> ParsedInstruction:
    text = mnemonic if not operands else f"{mnemonic} {', '.join(operands)}"
    return ParsedInstruction(mnemonic, tuple(operands), text)
