"""Small helpers for encoding context and consistent operand-count errors."""

from dataclasses import dataclass

from .errors import OperandError
from .parser import ParsedInstruction


@dataclass(frozen=True, slots=True)
class EncodeContext:
    """Address and label state needed while encoding an instruction."""

    address: int
    labels: dict[str, int]


@dataclass(frozen=True, slots=True)
class Operands:
    """Expose parsed operands and fail with one clear count-error shape."""

    instruction: ParsedInstruction

    @property
    def values(self) -> tuple[str, ...]:
        return self.instruction.operands

    def expect(self, count: int) -> tuple[str, ...]:
        if len(self.values) != count:
            raise OperandError(f"{self.instruction.mnemonic} expects {count} operand(s), got {len(self.values)}")
        return self.values
