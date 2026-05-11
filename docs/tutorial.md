# Syntax to Bitfields Tutorial

This tutorial follows real CLI output and the same code paths used by the tests.
Every example is one 32-bit MIPS instruction unless a pseudo-instruction expands
into multiple real instructions.

## `addi`: Immediate Arithmetic

```bash
python -m mips_tool walkthrough 'addi $v0, $zero, 4'
```

The instruction is I-type:

```text
opcode  rs     rt     immediate
001000  00000  00010  0000000000000100
```

`rs` is `$zero`, `rt` is `$v0`, and the immediate field stores `4`.

## `lw`: Memory Operand

```bash
python -m mips_tool walkthrough 'lw $t1, 8($t2)'
```

MIPS load/store syntax uses `offset(base)`. The base register becomes `rs`,
the loaded register becomes `rt`, and the offset becomes the immediate field.

## `beq`: Branch Offset

```asm
start:
    addi $t0, $zero, 1
    beq $t0, $zero, done
done:
    jr $ra
```

Branches encode a signed word offset from the instruction after the branch.
The assembler uses a two-pass walk so labels are known before branch fields are packed.

## `j`: Jump Address

```bash
python -m mips_tool walkthrough 'j 0x10'
```

J-type instructions keep the opcode and a 26-bit address field:

```text
opcode  address
000010  00000000000000000000010000
```

## `li`: Pseudo-Instruction Expansion

```bash
python -m mips_tool walkthrough 'li $t0, 0x12345678'
```

The pseudo-instruction expands into real MIPS instructions:

```text
lui $at, 4660
ori $t0, $at, 22136
```

The walkthrough shows each real instruction separately so the expansion stays visible.

## `ld`: MIPS64 Memory Example

```bash
python -m mips_tool explain 'ld $t0, 16($sp)'
```

`ld` uses the same I-type memory shape as other load/store instructions, with a
different opcode for the doubleword operation.
