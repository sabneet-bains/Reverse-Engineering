"""High-level assembly flow: parse text, resolve labels, and encode words."""

from .encode_forms import encode_by_category
from .encoding import EncodedInstruction
from .errors import OperandError, UnsupportedInstructionError
from .operands import EncodeContext
from .parser import ParsedInstruction, parse_instruction, parse_program
from .pseudo import expand_pseudo, expanded_length
from .tables import ALL_SPECS


def assemble_instruction(text: str, *, address: int = 0, labels: dict[str, int] | None = None) -> list[EncodedInstruction]:
    """Assemble one instruction or pseudo-instruction into encoded words."""
    parsed_instruction = parse_instruction(text)
    return _assemble_parsed(parsed_instruction, EncodeContext(address=address, labels=labels or {}))


def assemble_program(text: str, *, base_address: int = 0) -> list[EncodedInstruction]:
    """Assemble a multiline program, resolving labels with a simple two-pass walk."""
    parsed_lines = parse_program(text)

    # Pass 1: assign each label to the address of its real encoded instruction.
    labels: dict[str, int] = {}
    current_address = base_address
    for line in parsed_lines:
        if line.label:
            if line.label in labels:
                raise OperandError(f"duplicate label: {line.label}")
            labels[line.label] = current_address
        if line.instruction:
            current_address += 4 * expanded_length(line.instruction)

    # Pass 2: encode with the completed label table.
    encoded: list[EncodedInstruction] = []
    current_address = base_address
    for line in parsed_lines:
        if line.instruction:
            instructions = _assemble_parsed(line.instruction, EncodeContext(address=current_address, labels=labels))
            encoded.extend(instructions)
            current_address += 4 * len(instructions)
    return encoded


def _assemble_parsed(parsed: ParsedInstruction, context: EncodeContext) -> list[EncodedInstruction]:
    expanded_instructions = expand_pseudo(parsed)
    if expanded_instructions == [parsed]:
        return [_encode_real(parsed, context)]

    output: list[EncodedInstruction] = []
    current_address = context.address
    for expanded_instruction in expanded_instructions:
        encoded_instruction = _encode_real(expanded_instruction, EncodeContext(address=current_address, labels=context.labels))
        output.append(
            EncodedInstruction(
                encoded_instruction.word,
                encoded_instruction.assembly,
                encoded_instruction.fields,
                source=encoded_instruction.source,
                expanded_from=parsed.text,
            )
        )
        current_address += 4
    return output


def _encode_real(parsed: ParsedInstruction, context: EncodeContext) -> EncodedInstruction:
    instruction_spec = ALL_SPECS.get(parsed.mnemonic)
    if instruction_spec is None:
        raise UnsupportedInstructionError(f"unsupported instruction: {parsed.mnemonic}")
    return encode_by_category(parsed, instruction_spec, context)
