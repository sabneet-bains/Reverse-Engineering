# Changelog

All notable changes for this project are tracked here.

## 0.1.0 - MIPS32/64 Educational Toolkit

### What Became Possible

- Added a package-based MIPS32/64 encoder, decoder, bitfield explainer, and guided walkthrough CLI.
- Added a library API for assembling, decoding, explaining, and walking through instructions.
- Added a documented supported subset for MIPS32 integer, representative MIPS64 integer, COP0, COP1/FPU, and pseudo-instructions.
- Added examples, expected outputs, tutorial docs, correctness notes, code tour, generated instruction inventory, and vector provenance notes.

### Verification

- Added pytest coverage for instruction vectors, parser/register behavior, decode failures, walkthrough output, examples, CLI behavior, benchmark smoke checks, and table consistency.
- Added Ruff, mypy, compile, package build, install, and CLI smoke checks through GitHub Actions.

### Intentional Limits

- Kept ARM/x86 as future comparison work only.
- Kept the project focused on a tested MIPS32/64 subset, not exhaustive vendor-manual coverage.
