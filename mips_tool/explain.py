"""ASCII bitfield explanations for assembly instructions or machine words."""

from .decoder import decode_instruction, parse_word
from .encoder import assemble_instruction
from .encoding import EncodedInstruction
from .errors import MipsError


def explain_instruction(value: str | int) -> str:
    """Render a human-readable bitfield explanation for assembly or machine code."""
    if isinstance(value, str):
        stripped_input = value.strip()
        try:
            instruction_word = parse_word(stripped_input)
        except MipsError:
            encoded_instructions = assemble_instruction(stripped_input)
            if len(encoded_instructions) != 1:
                lines = [f"Pseudo-instruction: {stripped_input}"]
                for encoded_instruction in encoded_instructions:
                    lines.append(_render(encoded_instruction))
                return "\n\n".join(lines)
            encoded = encoded_instructions[0]
        else:
            encoded = decode_instruction(instruction_word)
    else:
        encoded = decode_instruction(value)
    return _render(encoded)


def _render(encoded: EncodedInstruction) -> str:
    rows = [
        ("Field", "Bits", "Value", "Meaning"),
        ("-----", "----", "-----", "-------"),
    ]
    for field in encoded.fields:
        bits = f"{field.high}:{field.low}" if field.high != field.low else str(field.high)
        rows.append((field.name, bits, field.bits, field.meaning))
    widths = [max(len(row[i]) for row in rows) for i in range(4)]
    table = "\n".join(
        "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip()
        for row in rows
    )
    header = [
        f"assembly: {encoded.assembly}",
        f"format:   {_format_name(encoded)}",
        f"layout:   {' '.join(field.name for field in encoded.fields)}",
        f"binary:   {encoded.binary}",
        f"hex:      {encoded.hex}",
    ]
    if encoded.expanded_from:
        header.insert(0, f"expanded: {encoded.expanded_from} -> {encoded.assembly}")
    return "\n".join(header + ["", table])


def _format_name(encoded: EncodedInstruction) -> str:
    names = tuple(field.name for field in encoded.fields)
    if names == ("opcode", "rs", "rt", "rd", "shamt", "funct"):
        return "R-type"
    if names == ("opcode", "rs", "rt", "immediate"):
        return "I-type"
    if names == ("opcode", "address"):
        return "J-type"
    if names and names[0] == "opcode":
        return "specialized"
    return "unknown"
