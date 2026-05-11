"""User-facing exception types for parse, operand, and support failures."""

class MipsError(ValueError):
    """Base error for user-facing assembler/disassembler failures."""


class ParseError(MipsError):
    """Raised when assembly text cannot be parsed."""


class UnsupportedInstructionError(MipsError):
    """Raised when a mnemonic or encoding is outside the supported subset."""


class OperandError(MipsError):
    """Raised when operands are malformed or do not match an instruction."""
