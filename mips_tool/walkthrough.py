"""Step-by-step instruction walkthroughs for visual learners."""

from .decoder import decode_instruction, parse_word
from .encoder import assemble_instruction
from .encoding import EncodedInstruction
from .errors import MipsError
from .parser import ParsedInstruction, parse_instruction
from .tables import ALL_SPECS


def walkthrough_instruction(value: str | int) -> str:
    """Render a deterministic syntax-to-bitfields walkthrough."""
    if isinstance(value, int):
        return _walkthrough_word(value)

    stripped_input = value.strip()
    try:
        instruction_word = parse_word(stripped_input)
    except MipsError:
        return _walkthrough_assembly(stripped_input)
    return _walkthrough_word(instruction_word)


def _walkthrough_word(instruction_word: int) -> str:
    decoded = decode_instruction(instruction_word)
    parsed = parse_instruction(decoded.assembly)
    return _render_one(decoded.assembly, parsed, decoded, source_kind="machine word")


def _walkthrough_assembly(text: str) -> str:
    parsed = parse_instruction(text)
    encoded_instructions = assemble_instruction(text)
    if len(encoded_instructions) == 1 and not encoded_instructions[0].expanded_from:
        return _render_one(text, parsed, encoded_instructions[0], source_kind="assembly")

    lines = [
        f"input:     {text}",
        "kind:      pseudo-instruction",
        "",
        "expansion:",
    ]
    for index, encoded_instruction in enumerate(encoded_instructions, start=1):
        lines.append(f"  {index}. {encoded_instruction.assembly}")
    for encoded_instruction in encoded_instructions:
        expanded = parse_instruction(encoded_instruction.assembly)
        lines.append("")
        lines.append(_render_one(encoded_instruction.assembly, expanded, encoded_instruction, source_kind="expanded"))
    return "\n".join(lines)


def _render_one(
    original_input: str,
    parsed: ParsedInstruction,
    encoded: EncodedInstruction,
    *,
    source_kind: str,
) -> str:
    instruction_spec = ALL_SPECS.get(parsed.mnemonic)
    form = instruction_spec.kind if instruction_spec else "decoded"

    # The table is the visual bridge from parsed syntax to packed machine fields.
    rows = [
        ("Field", "Bits", "Binary", "Meaning"),
        ("-----", "----", "------", "-------"),
    ]
    for field in encoded.fields:
        bits = f"{field.high}:{field.low}" if field.high != field.low else str(field.high)
        rows.append((field.name, bits, field.bits, field.meaning))
    widths = [max(len(row[column]) for row in rows) for column in range(4)]
    table = "\n".join(
        "  ".join(cell.ljust(widths[column]) for column, cell in enumerate(row)).rstrip()
        for row in rows
    )
    operands = ", ".join(parsed.operands) if parsed.operands else "(none)"
    header = [
        f"input:     {original_input}",
        f"kind:      {source_kind}",
        f"mnemonic:  {parsed.mnemonic}",
        f"operands:  {operands}",
        f"form:      {_format_name(encoded)} / {form}",
        f"table:     {_table_entry(instruction_spec)}",
        f"pack:      {_pack_step(encoded)}",
        f"assembly:  {encoded.assembly}",
        f"binary:    {encoded.binary}",
        f"hex:       {encoded.hex}",
        "",
        "bitfields:",
    ]
    return "\n".join(header + [table])


def _table_entry(instruction_spec) -> str:
    if instruction_spec is None:
        return "decoded word"
    parts = [
        f"opcode=0x{instruction_spec.opcode:02X}",
        f"kind={instruction_spec.kind}",
    ]
    if instruction_spec.funct is not None:
        parts.append(f"funct=0x{instruction_spec.funct:02X}")
    if instruction_spec.rt_code is not None:
        parts.append(f"rt_code=0x{instruction_spec.rt_code:02X}")
    if instruction_spec.fmt is not None:
        parts.append(f"fmt=0x{instruction_spec.fmt:02X}")
    if instruction_spec.rs_code is not None:
        parts.append(f"rs_code=0x{instruction_spec.rs_code:02X}")
    return ", ".join(parts)


def _pack_step(encoded: EncodedInstruction) -> str:
    names = tuple(field.name for field in encoded.fields)
    if names == ("opcode", "rs", "rt", "rd", "shamt", "funct"):
        return "pack_r(opcode, rs, rt, rd, shamt, funct)"
    if names == ("opcode", "rs", "rt", "immediate"):
        return "pack_i(opcode, rs, rt, immediate)"
    if names == ("opcode", "address"):
        return "pack_j(opcode, address)"
    return "specialized field packing"


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
