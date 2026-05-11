"""Command-line interface for assembling, disassembling, and explaining MIPS code."""

import argparse
import sys
from pathlib import Path

from .decoder import decode_instruction
from .encoder import assemble_instruction, assemble_program
from .encoding import EncodedInstruction
from .errors import MipsError
from .explain import explain_instruction
from .walkthrough import walkthrough_instruction


def main(argv: list[str] | None = None) -> int:
    """Run the MIPS tool command-line interface."""
    parser = argparse.ArgumentParser(prog="mips-tool", description="MIPS32/64 encoder, decoder, and bitfield explainer")
    subparsers = parser.add_subparsers(dest="command", required=True)

    assemble = subparsers.add_parser("assemble", help="assemble one instruction or a .asm file")
    assemble.add_argument("input", help="assembly instruction text or file path")
    assemble.add_argument("--base", default="0", help="base address for label resolution")
    assemble.add_argument("--format", choices=["binary", "hex", "both"], default="both")

    disassemble = subparsers.add_parser("disassemble", help="disassemble one 32-bit word")
    disassemble.add_argument("word", help="32-bit binary string or integer literal")

    explain = subparsers.add_parser("explain", help="show instruction bitfields")
    explain.add_argument("input", help="assembly instruction or 32-bit word")

    walkthrough = subparsers.add_parser("walkthrough", help="show a step-by-step encoding walkthrough")
    walkthrough.add_argument("input", help="assembly instruction or 32-bit word")

    parsed_args = parser.parse_args(argv)
    try:
        if parsed_args.command == "assemble":
            encoded_instructions = _assemble_input(parsed_args.input, int(parsed_args.base, 0))
            for encoded_instruction in encoded_instructions:
                if encoded_instruction.expanded_from:
                    print(f"{encoded_instruction.expanded_from} -> {encoded_instruction.assembly}")
                elif encoded_instruction.source and encoded_instruction.source != encoded_instruction.assembly:
                    print(encoded_instruction.assembly)
                if parsed_args.format in {"binary", "both"}:
                    print(encoded_instruction.binary)
                if parsed_args.format in {"hex", "both"}:
                    print(encoded_instruction.hex)
        elif parsed_args.command == "disassemble":
            print(decode_instruction(parsed_args.word).assembly)
        elif parsed_args.command == "explain":
            print(explain_instruction(parsed_args.input))
        elif parsed_args.command == "walkthrough":
            print(walkthrough_instruction(parsed_args.input))
        return 0
    except MipsError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


def _assemble_input(input_text_or_path: str, base_address: int) -> list[EncodedInstruction]:
    path = Path(input_text_or_path)
    if path.exists() and path.is_file():
        return assemble_program(path.read_text(encoding="utf-8"), base_address=base_address)
    if "\n" in input_text_or_path:
        return assemble_program(input_text_or_path, base_address=base_address)
    return assemble_instruction(input_text_or_path, address=base_address)


if __name__ == "__main__":
    raise SystemExit(main())
