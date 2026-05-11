"""Route parsed instructions to the right operand-form encoder."""

from collections.abc import Callable

from .encode_coprocessor import COP0_ENCODERS, FPU_ENCODERS
from .encode_i import I_ENCODERS
from .encode_r import R_ENCODERS
from .encoding import EncodedInstruction, j_fields, pack_j
from .errors import UnsupportedInstructionError
from .operands import EncodeContext, Operands
from .parser import ParsedInstruction, parse_int, require_range
from .tables import COP0_SPECS, FPU_SPECS, I_SPECS, J_SPECS, R_SPECS, InstructionSpec

type EncodeHandler = Callable[[ParsedInstruction, InstructionSpec, EncodeContext], EncodedInstruction]


def encode_by_category(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    """Encode one real instruction using its mnemonic category."""
    handler = CATEGORY_ENCODERS.get(parsed.mnemonic)
    if handler is None:
        raise UnsupportedInstructionError(f"unsupported instruction: {parsed.mnemonic}")
    return handler(parsed, instruction_spec, context)


def _encode_r(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    return _encode_by_form(parsed, instruction_spec, context, R_ENCODERS, "R-type")


def _encode_i(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    return _encode_by_form(parsed, instruction_spec, context, I_ENCODERS, "I-type")


def _encode_fpu(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    return _encode_by_form(parsed, instruction_spec, context, FPU_ENCODERS, "FPU")


def _encode_cop0(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    return _encode_by_form(parsed, instruction_spec, context, COP0_ENCODERS, "COP0")


def _encode_by_form(
    parsed: ParsedInstruction,
    instruction_spec: InstructionSpec,
    context: EncodeContext,
    encoders: dict[str, EncodeHandler],
    group_name: str,
) -> EncodedInstruction:
    handler = encoders.get(instruction_spec.kind)
    if handler is None:
        raise UnsupportedInstructionError(f"unsupported {group_name} form: {instruction_spec.kind}")
    return handler(parsed, instruction_spec, context)


def _encode_j(parsed: ParsedInstruction, instruction_spec: InstructionSpec, context: EncodeContext) -> EncodedInstruction:
    (target_token,) = Operands(parsed).expect(1)
    label_address = context.labels.get(target_token)
    address = (label_address >> 2) if label_address is not None else parse_int(target_token)
    address = require_range(address, 26, signed=False, what="jump address")
    word = pack_j(instruction_spec.opcode, address)
    assembly = f"{instruction_spec.mnemonic} {hex(address)}"
    fields = j_fields(instruction_spec.mnemonic, instruction_spec.opcode, address)
    return EncodedInstruction(word, assembly, fields, source=parsed.text)


# Uniform handler signatures keep each instruction family visually aligned.
CATEGORY_GROUPS = (
    (R_SPECS, _encode_r),
    (I_SPECS, _encode_i),
    (J_SPECS, _encode_j),
    (FPU_SPECS, _encode_fpu),
    (COP0_SPECS, _encode_cop0),
)
CATEGORY_ENCODERS: dict[str, EncodeHandler] = {
    mnemonic: handler
    for specs, handler in CATEGORY_GROUPS
    for mnemonic in specs
}
