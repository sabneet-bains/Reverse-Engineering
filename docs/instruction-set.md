# Instruction Inventory

Generated from `mips_tool.tables`; do not edit by hand.

Regenerate with:

```bash
python tools/generate_instruction_inventory.py > docs/instruction-set.md
```

| Count | Value |
|:--|--:|
| Real supported mnemonics | 105 |
| Pseudo-instructions | 8 |
| Total supported names | 113 |

| Group | Count | Role | Mnemonics |
|:--|--:|:--|:--|
| R-type / SPECIAL | 51 | Register arithmetic, shifts, HI/LO moves, multiply/divide, traps. | `add`, `addu`, `sub`, `subu`, `and`, `or`, `xor`, `nor`, `slt`, `sltu`, `dadd`, `daddu`, `dsub`, `dsubu`, `sll`, `srl`, `sra`, `dsll`, `dsrl`, `dsra`, `dsll32`, `dsrl32`, `dsra32`, `sllv`, `srlv`, `srav`, `dsllv`, `dsrlv`, `dsrav`, `jr`, `jalr`, `mfhi`, `mthi`, `mflo`, `mtlo`, `mult`, `multu`, `div`, `divu`, `dmult`, `dmultu`, `ddiv`, `ddivu`, `syscall`, `break`, `tge`, `tgeu`, `tlt`, `tltu`, `teq`, `tne` |
| I-type / REGIMM | 39 | Immediates, branches, load/store, and trap immediates. | `addi`, `addiu`, `slti`, `sltiu`, `andi`, `ori`, `xori`, `daddi`, `daddiu`, `lui`, `beq`, `bne`, `blez`, `bgtz`, `bltz`, `bgez`, `bltzal`, `bgezal`, `lb`, `lh`, `lwl`, `lw`, `lbu`, `lhu`, `lwr`, `lwu`, `ldl`, `ldr`, `ld`, `sb`, `sh`, `swl`, `sw`, `swr`, `sdl`, `sdr`, `sd`, `teqi`, `tnei` |
| J-type | 2 | Absolute jump target field. | `j`, `jal` |
| FPU / COP1 | 10 | Representative floating-point arithmetic and GPR-FPR moves. | `add.s`, `sub.s`, `mul.s`, `div.s`, `add.d`, `sub.d`, `mul.d`, `div.d`, `mfc1`, `mtc1` |
| COP0 | 3 | Representative system-control moves and exception return. | `mfc0`, `mtc0`, `eret` |
| Pseudo-instructions | 8 | Assembler conveniences expanded into real instructions. | `li`, `move`, `clear`, `nop`, `not`, `b`, `beqz`, `bnez` |
