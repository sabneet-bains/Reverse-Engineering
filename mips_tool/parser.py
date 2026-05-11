"""Parsing helpers for MIPS assembly lines, operands, labels, and integers."""

import re
from dataclasses import dataclass

from .errors import OperandError, ParseError
from .registers import parse_gpr

COMMENT_RE = re.compile(r"(#|;).*$")
LABEL_RE = re.compile(r"^\s*([A-Za-z_.$][\w.$]*):")
MEMORY_RE = re.compile(r"^(.+?)\((\$[A-Za-z0-9]+)\)$")


@dataclass(frozen=True, slots=True)
class ParsedInstruction:
    """Mnemonic, operands, and original cleaned text for one instruction."""
    mnemonic: str
    operands: tuple[str, ...]
    text: str


@dataclass(frozen=True, slots=True)
class ParsedLine:
    """Parsed source line with an optional label and instruction."""
    label: str | None
    instruction: ParsedInstruction | None
    raw: str


def parse_int(token: str) -> int:
    """Parse a decimal, hexadecimal, binary, or underscored integer literal."""
    try:
        return int(token.replace("_", ""), 0)
    except ValueError as exc:
        raise OperandError(f"invalid integer literal: {token}") from exc


def require_range(value: int, bits: int, *, signed: bool, what: str) -> int:
    """Validate and mask an integer into a fixed-width field."""
    if signed:
        low = -(1 << (bits - 1))
        high = (1 << (bits - 1)) - 1
    else:
        low = 0
        high = (1 << bits) - 1
    if not low <= value <= high:
        kind = "signed" if signed else "unsigned"
        raise OperandError(f"{what} out of {kind} {bits}-bit range: {value}")
    return value & ((1 << bits) - 1)


def sign_extend(value: int, bits: int) -> int:
    """Sign-extend a fixed-width two's-complement value."""
    sign = 1 << (bits - 1)
    mask = (1 << bits) - 1
    value &= mask
    return value - (1 << bits) if value & sign else value


def clean_line(line: str) -> str:
    """Remove comments and surrounding whitespace from one source line."""
    return COMMENT_RE.sub("", line).strip()


def split_operands(text: str) -> tuple[str, ...]:
    """Split a comma-separated operand list."""
    if not text.strip():
        return ()
    return tuple(part.strip() for part in text.split(",") if part.strip())


def parse_instruction(text: str) -> ParsedInstruction:
    """Parse one instruction line into mnemonic and operand tokens."""
    text = clean_line(text)
    if not text:
        raise ParseError("empty instruction")
    pieces = text.split(None, 1)
    mnemonic = pieces[0].lower()
    operands = split_operands(pieces[1] if len(pieces) == 2 else "")
    return ParsedInstruction(mnemonic, operands, text)


def parse_program(text: str) -> list[ParsedLine]:
    """Parse a multiline assembly program with optional labels."""
    parsed: list[ParsedLine] = []
    for raw in text.splitlines():
        rest = clean_line(raw)
        if not rest:
            continue
        label = None
        match = LABEL_RE.match(rest)
        if match:
            label = match.group(1)
            rest = rest[match.end() :].strip()
        instruction = parse_instruction(rest) if rest else None
        parsed.append(ParsedLine(label, instruction, raw))
    return parsed


def parse_memory_operand(token: str) -> tuple[int, int]:
    """Parse `offset(base)` memory syntax into immediate and base register."""
    match = MEMORY_RE.match(token.replace(" ", ""))
    if not match:
        raise OperandError(f"expected memory operand offset(base), got: {token}")
    offset = require_range(parse_int(match.group(1)), 16, signed=True, what="memory offset")
    base = parse_gpr(match.group(2))
    return offset, base
