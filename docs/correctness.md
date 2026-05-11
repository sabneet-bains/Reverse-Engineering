# Correctness Notes

This project is a tested MIPS32/64 educational subset, not a full vendor-manual assembler.

## Scope Boundary

Supported instructions are listed in `docs/instruction-set.md`, generated from
`mips_tool.tables`. Unsupported mnemonics, malformed operands, out-of-range
immediates, and unknown machine words raise user-facing errors.

ARM and x86 are roadmap comparison targets only.

## Table-Driven Consistency

The encoder and decoder share instruction metadata from `tables.py`.
Each instruction records its mnemonic, opcode, operand form, and any required
function, register-selector, or format fields.

That shared table prevents a common teaching-tool bug: the assembler and
disassembler drifting into two separate sources of truth.

## Vector Strategy

The tests include fixed vectors for R-type, I-type, J-type, MIPS64, COP0, and COP1
forms. `docs/vector-provenance.md` records the source scope for these vectors.
The vectors assert both directions:

```text
assembly -> machine word -> canonical assembly
```

Negative tests cover unsupported mnemonics, malformed operands, bad registers,
out-of-range immediates, and unsupported decode words.

## Verification Commands

```bash
python -m ruff check .
python -m mypy mips_tool tools
python -m pytest
python -m compileall mips_tool tests tools
python tools/benchmark.py --quick
```

The benchmark is informational only. It is not a pass/fail performance gate.
