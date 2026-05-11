# Vector Provenance

The fixed instruction vectors in `tests/test_instruction_vectors.py` are grouped
around the field layouts described in the MIPS architecture programmer manuals:

- MIPS32 Architecture For Programmers, Volume II / Volume II-A: The MIPS32 Instruction Set.
- MIPS64 Architecture For Programmers, Volume II / Volume II-A: The MIPS64 Instruction Set.
- MIPS32 Instruction Set Quick Reference for compact opcode/funct cross-checks.

The tests are not a claim of exhaustive vendor-manual coverage. They are a
representative correctness net for the documented subset in `mips_tool.tables`.

Each vector checks the round trip:

```text
assembly -> expected hex word -> canonical disassembly
```

The covered families are:

| Family | Reference category | Examples |
|:--|:--|:--|
| R-type / SPECIAL | MIPS32 base integer encodings | `add`, `subu`, `sll`, `jr`, `syscall`, trap forms |
| I-type / REGIMM | MIPS32 immediate, branch, and load/store encodings | `addiu`, `andi`, `lui`, `beq`, `bltz`, load/store |
| J-type | MIPS32 jump encodings | `j`, `jal` |
| MIPS64 integer | MIPS64 integer and doubleword memory encodings | `daddu`, `dsll32`, `ddivu`, `sd` |
| COP1 / FPU | Representative COP1 floating-point encodings | `add.d`, `mtc1` |
| COP0 | Representative system-control encodings | `mfc0`, `eret` |

The suite also includes a table-consistency check that assembles one valid sample
for every real instruction form in `mips_tool.tables`, decodes the generated
word, and reassembles the canonical disassembly back to the same 32-bit value.
That catches drift between the shared instruction tables, encoder dispatch, and
decoder dispatch without claiming exhaustive ISA validation.

When adding a new instruction, add one positive vector and at least one failure
case if the operand form introduces new validation behavior.
