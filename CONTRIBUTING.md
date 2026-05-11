# Contributing

This project favors small, testable changes that keep the instruction path easy
to inspect.

## Local Checks

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m mypy mips_tool tools
python -m compileall mips_tool tests tools
python -m pytest
python -m build
```

## Adding Instructions

Instruction changes should follow the same path the tool uses:

```text
tables.py -> encode/decode form -> vector test -> generated inventory
```

1. Add the instruction metadata in `mips_tool/tables.py`.
2. Reuse an existing operand form where possible; add a new form only when the
   instruction truly needs different packing or rendering.
3. Add at least one positive vector in `tests/test_instruction_vectors.py`.
4. Add a clear failure test when the new operand form introduces new validation.
5. Regenerate the inventory:

```bash
python tools/generate_instruction_inventory.py > docs/instruction-set.md
```

Unsupported instructions should fail clearly. Do not add partial behavior that
looks valid but silently encodes the wrong word.
