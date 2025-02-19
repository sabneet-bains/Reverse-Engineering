#!/usr/bin/env python3
"""
MIPS Assembler

This script converts a list of MIPS assembly instructions into machine code (binary, decimal, and hexadecimal formats).
It supports a subset of instructions as defined in the MIPS_FORMAT and MIPS_REGISTERS dictionaries.
This version is designed for educational purposes and can be extended to support additional instructions.

Usage:
    python assembler.py

Author: Sabneet Bains
License: MIT
"""

from typing import List, Dict

# Sample instructions for demonstration purposes
instructions: List[List[str]] = [
    ['addi', '$v0', '$zero', '0'],
    ['lw', '$t9', '0', '$a0'],
    ['addi', '$v0', '$v0', '1'],
    ['sw', '$t9', '$0', '$a1'],
    ['addi', '$a0', '$a0', '4'],
    ['addi', '$a1', '$a1', '4']
]

# MIPS instruction format definitions
MIPS_FORMAT: Dict[str, List[str]] = {
    'Mnemonic': ['add', 'addi', 'addiu', 'addu', 'and', 'andi', 'beq', 'blez', 'bne', 'bgtz', 'div', 'divu', 'j', 'jal', 'jr', 'lb', 'lbu', 'lhu', 'lui', 'lw', 'mfhi', 'mthi', 'mflo', 'mtlo', 'mfc0', 'mult', 'multu', 'nor', 'xor', 'or', 'ori', 'sb', 'sh', 'slt', 'slti', 'sltiu', 'sltu', 'sll', 'srl', 'sra', 'sub', 'subu', 'sw'],
    'Type':     ['R',   'I',    'I',     'R',    'R',   'I',    'I',   'I',   'I',   'I',    'R',   'R',   'J',  'J',  'R',  'I',   'I',   'I',   'I',   'I',   'R',   'R',   'R',   'R',   'R',   'R',    'R',    'R',    'R',   'R',   'I',   'I',   'I',   'R',   'I',   'I',   'R',   'R',   'R',   'R',   'R',   'R',   'I'],
    'Opcode':   ['000000','001000','001001','000000','000000','001100','000100','000110','000101','000111','000000','000000','000010','000011','000000','100000','100100','100101','001111','100011','000000','000000','000000','000000','010000','000000','000000','000000','000000','000000','001101','101000','101001','000000','001010','001011','000000','000000','000000','000000','000000','000000','101011'],
    'Funct':    ['100000','NA',   'NA',   '100001','100100','NA',   'NA',  'NA',  'NA',  'NA',   '011010','011011','NA','NA','001000','NA','NA','NA','NA','NA','010000','010001','010010','010011','NA','011000','011001','100111','100110','100101','NA','NA','NA','101010','NA','NA','101011','000000','000010','000011','100010','100011','NA']
}

# Register mapping: maps register names to 5-bit binary strings
MIPS_REGISTERS: Dict[str, str] = {
    '$0': '00000', '$zero': '00000', '$at': '00001', '$v0': '00010', '$v1': '00011',
    '$a0': '00100', '$a1': '00101', '$a2': '00110', '$a3': '00111',
    '$t0': '01000', '$t1': '01001', '$t2': '01010', '$t3': '01011', '$t4': '01100',
    '$t5': '01101', '$t6': '01110', '$t7': '01111',
    '$s0': '10000', '$s1': '10001', '$s2': '10010', '$s3': '10011', '$s4': '10100',
    '$s5': '10101', '$s6': '10110', '$s7': '10111',
    '$t8': '11000', '$t9': '11001', '$k0': '11010', '$k1': '11011',
    '$gp': '11100', '$sp': '11101', '$fp': '11110', '$ra': '11111'
}


def pad_binary(value: int, width: int) -> str:
    """Return the binary representation of an integer, padded with zeros to the specified width."""
    return format(value & ((1 << width) - 1), f'0{width}b')


def assemble_R_type(tokens: List[str], index: int) -> None:
    """
    Assemble an R-type instruction.
    Expects tokens in the order: [mnemonic, rd, rs, rt]
    """
    opcode = MIPS_FORMAT['Opcode'][index]
    rd = tokens[1]
    rs = tokens[2]
    rt = tokens[3]
    shamt = '00000'
    func_code = MIPS_FORMAT['Funct'][index]

    try:
        rs_bin = MIPS_REGISTERS[rs]
        rt_bin = MIPS_REGISTERS[rt]
        rd_bin = MIPS_REGISTERS[rd]
    except KeyError as e:
        raise ValueError(f"Unknown register: {e}")

    machine_code_bin = opcode + rs_bin + rt_bin + rd_bin + shamt + func_code
    machine_code_dec = (
        int(opcode, 2),
        int(rs_bin, 2),
        int(rt_bin, 2),
        int(rd_bin, 2),
        int(shamt, 2),
        int(func_code, 2)
    )
    machine_code_hex = hex(int(machine_code_bin, 2))

    print('______________________________________')
    print(f"| Assembled MIPS R-type Machine Code |")
    print(f"\n⦿  decimal: {machine_code_dec}")
    print(f"⦿  binary: {opcode} {rs_bin} {rt_bin} {rd_bin} {shamt} {func_code}")
    print(f"⦿  hexadecimal: {machine_code_hex}")


def assemble_I_type(tokens: List[str], index: int) -> None:
    """
    Assemble an I-type instruction.
    Expects tokens in the order: [mnemonic, rt, rs, immediate]
    """
    opcode = MIPS_FORMAT['Opcode'][index]

    # Determine if the tokens are registers or numeric literals
    rs_token = tokens[2]
    rt_token = tokens[1]
    imm_token = tokens[3]

    rs_bin = MIPS_REGISTERS.get(rs_token) if '$' in rs_token else pad_binary(int(rs_token, 16), 5)
    rt_bin = MIPS_REGISTERS.get(rt_token) if '$' in rt_token else pad_binary(int(rt_token, 16), 5)
    immediate = int(imm_token, 16) if ('$' not in imm_token) else int(imm_token)
    immediate_bin = pad_binary(immediate, 16)

    machine_code_bin = opcode + rs_bin + rt_bin + immediate_bin
    machine_code_dec = (int(opcode, 2), int(rs_bin, 2), int(rt_bin, 2), int(immediate_bin, 2))
    machine_code_hex = hex(int(machine_code_bin, 2))

    print('______________________________________')
    print(f"| Assembled MIPS I-type Machine Code |")
    print(f"\n⦿  decimal: {machine_code_dec}")
    print(f"⦿  binary: {opcode} {rs_bin} {rt_bin} {immediate_bin}")
    print(f"⦿  hexadecimal: {machine_code_hex}")


def assemble_J_type(tokens: List[str], index: int) -> None:
    """
    Assemble a J-type instruction.
    Expects tokens in the order: [mnemonic, immediate]
    """
    opcode = MIPS_FORMAT['Opcode'][index]
    imm_token = tokens[1]
    immediate = int(imm_token, 16) if ('$' not in imm_token) else int(imm_token)
    immediate_bin = pad_binary(immediate, 26)

    machine_code_bin = opcode + immediate_bin
    machine_code_dec = (int(opcode, 2), int(immediate_bin, 2))
    machine_code_hex = hex(int(machine_code_bin, 2))

    print('______________________________________')
    print(f"| Assembled MIPS J-type Machine Code |")
    print(f"\n⦿  decimal: {machine_code_dec}")
    print(f"⦿  binary: {opcode} {immediate_bin}")
    print(f"⦿  hexadecimal: {machine_code_hex}")


def assemble_instructions(instr_list: List[List[str]]) -> None:
    """
    Process and assemble a list of MIPS instructions.
    Each instruction is a list of tokens.
    """
    for tokens in instr_list:
        mnemonic = tokens[0]
        if mnemonic in MIPS_FORMAT['Mnemonic']:
            index = MIPS_FORMAT['Mnemonic'].index(mnemonic)
            inst_type = MIPS_FORMAT['Type'][index]

            if inst_type == 'R':
                assemble_R_type(tokens, index)
            elif inst_type == 'I':
                assemble_I_type(tokens, index)
            elif inst_type == 'J':
                assemble_J_type(tokens, index)
            else:
                print(f"Unsupported instruction type: {inst_type}")
        else:
            print(f"Mnemonic {mnemonic} not recognized.")


def main() -> None:
    try:
        assemble_instructions(instructions)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
