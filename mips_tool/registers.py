"""Register name tables and parsers for GPR, FPR, and COP0 operands."""

from .errors import OperandError

GPR_NAMES = {
    0: "$zero",
    1: "$at",
    2: "$v0",
    3: "$v1",
    4: "$a0",
    5: "$a1",
    6: "$a2",
    7: "$a3",
    8: "$t0",
    9: "$t1",
    10: "$t2",
    11: "$t3",
    12: "$t4",
    13: "$t5",
    14: "$t6",
    15: "$t7",
    16: "$s0",
    17: "$s1",
    18: "$s2",
    19: "$s3",
    20: "$s4",
    21: "$s5",
    22: "$s6",
    23: "$s7",
    24: "$t8",
    25: "$t9",
    26: "$k0",
    27: "$k1",
    28: "$gp",
    29: "$sp",
    30: "$fp",
    31: "$ra",
}

GPR_ALIASES = {name: value for value, name in GPR_NAMES.items()}
GPR_ALIASES.update({"$0": 0, "$s8": 30})
for i in range(32):
    GPR_ALIASES[f"${i}"] = i

COP0_NAMES = {
    0: "$index",
    1: "$random",
    8: "$badvaddr",
    9: "$count",
    10: "$entryhi",
    11: "$compare",
    12: "$status",
    13: "$cause",
    14: "$epc",
    15: "$prid",
}
COP0_ALIASES = {name: value for value, name in COP0_NAMES.items()}
for i in range(32):
    COP0_ALIASES[f"${i}"] = i


def parse_gpr(token: str) -> int:
    """Return the numeric general-purpose register index for a token."""
    value = GPR_ALIASES.get(token.lower())
    if value is None:
        raise OperandError(f"unknown general-purpose register: {token}")
    return value


def parse_fpr(token: str) -> int:
    """Return the numeric floating-point register index for a token."""
    token = token.lower()
    if not token.startswith("$f"):
        raise OperandError(f"unknown floating-point register: {token}")
    try:
        value = int(token[2:], 10)
    except ValueError as exc:
        raise OperandError(f"unknown floating-point register: {token}") from exc
    if not 0 <= value <= 31:
        raise OperandError(f"floating-point register out of range: {token}")
    return value


def parse_cop0(token: str) -> int:
    """Return the numeric COP0 register index for a token."""
    value = COP0_ALIASES.get(token.lower())
    if value is None:
        raise OperandError(f"unknown COP0 register: {token}")
    return value


def gpr_name(value: int) -> str:
    """Return the canonical general-purpose register name for an index."""
    return GPR_NAMES.get(value, f"${value}")


def fpr_name(value: int) -> str:
    """Return the canonical floating-point register name for an index."""
    return f"$f{value}"


def cop0_name(value: int) -> str:
    """Return the canonical COP0 register name for an index."""
    return COP0_NAMES.get(value, f"${value}")
