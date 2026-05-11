# Code Tour

The source is shaped around MIPS concepts rather than framework patterns.
Each file owns one small part of the syntax-to-bitfields path.

```text
source text
  -> parser/registers
  -> tables
  -> encoder/decoder forms
  -> encoding/word
  -> explain/walkthrough/cli
```

## Core Pipeline

| File | Owns | What to notice |
|:--|:--|:--|
| `mips_tool/tables.py` | Instruction metadata | One shared source for encoder and decoder behavior |
| `mips_tool/registers.py` | Register names and aliases | Numeric and symbolic registers resolve through simple maps |
| `mips_tool/parser.py` | Lines, labels, immediates, memory operands | Parsing is small and line-oriented, not a full macro assembler |
| `mips_tool/word.py` | Named bitfield view | A 32-bit word becomes `opcode`, `rs`, `rt`, `rd`, `shamt`, `funct`, `immediate`, `address` |
| `mips_tool/encoding.py` | Packing and field metadata | Encoded words carry binary, hex, canonical assembly, and fields |
| `mips_tool/encoder.py` | High-level assembly flow | Parse, resolve labels, expand pseudo-instructions, encode |
| `mips_tool/encode_r.py` | R-type encoders | Each operand form follows the same field-packing shape |
| `mips_tool/encode_i.py` | I-type and REGIMM encoders | Immediates, memory operands, and branches stay explicit |
| `mips_tool/encode_coprocessor.py` | COP1/COP0 encoders | Representative specialized formats stay separate from integer code |
| `mips_tool/decoder.py` | High-level opcode dispatch | The first six bits choose the decode family |
| `mips_tool/decode_r.py` | R-type renderers | Render handlers mirror R-type encoder forms |
| `mips_tool/decode_i.py` | I/J/REGIMM renderers | Branch, memory, and immediate formatting stays canonical |
| `mips_tool/decode_coprocessor.py` | COP1/COP0 decoders | Specialized decode fields stay visible |
| `mips_tool/explain.py` | Bitfield table output | Field metadata becomes deterministic CLI text |
| `mips_tool/walkthrough.py` | Guided instruction path | The same parser, tables, and fields become a visual walkthrough |
| `mips_tool/cli.py` | Command-line interface | Thin wrapper around the library API |

## Support Files

| File | Owns | What to notice |
|:--|:--|:--|
| `docs/instruction-set.md` | Generated scope inventory | Mirrors `tables.py`, so documentation does not drift |
| `tools/generate_instruction_inventory.py` | Inventory generation | Converts source tables into markdown |
| `tools/benchmark.py` | Informational timing | Exercises public encode/decode/explain paths without test thresholds |
| `tests/` | Behavior contract | Tests public behavior, examples, vectors, failures, and generated docs |

The simple-code signature is intentional: small files, direct names, visible data,
and repeated shapes that match the architecture.
