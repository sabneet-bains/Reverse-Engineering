"""Stdlib-only benchmark for the public encode, decode, explain, and program paths."""

import argparse
import sys
import timeit
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PROGRAM = """
start:
    li $t0, 0x12345678
    addiu $t1, $zero, -1
    lw $t2, 8($sp)
    beq $t2, $zero, done
    daddu $t3, $t0, $t2
done:
    jr $ra
"""


def _rate(label: str, stmt: str, setup: str, iterations: int) -> str:
    elapsed = timeit.timeit(stmt, setup=setup, number=iterations)
    rate = iterations / elapsed if elapsed else float("inf")
    return f"{label:<18} {iterations:>8} ops  {elapsed:>8.4f}s  {rate:>12.0f} ops/s"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Benchmark MIPS tool encode/decode/explain paths")
    parser.add_argument("--quick", action="store_true", help="run fewer iterations for smoke checks")
    parsed_args = parser.parse_args(argv)

    iterations = 1_000 if parsed_args.quick else 50_000
    program_iterations = 100 if parsed_args.quick else 5_000
    setup = (
        "from __main__ import PROGRAM; "
        "from mips_tool.encoder import assemble_instruction, assemble_program; "
        "from mips_tool.decoder import decode_instruction; "
        "from mips_tool.explain import explain_instruction"
    )
    rows = [
        _rate("encode", "assemble_instruction('addi $v0, $zero, 4')", setup, iterations),
        _rate("decode", "decode_instruction('00100000000000100000000000000100')", setup, iterations),
        _rate("explain", "explain_instruction('ld $t0, 16($sp)')", setup, iterations),
        _rate("program", "assemble_program(PROGRAM)", setup, program_iterations),
    ]
    print("MIPS tool benchmark")
    print("-------------------")
    print("Informational only: no timing thresholds are used in tests.")
    print("\n".join(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
