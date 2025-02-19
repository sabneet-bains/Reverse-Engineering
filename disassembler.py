#!/usr/bin/env python3
"""
MIPS Disassembler

This script converts a list of 32-bit machine code binary strings into human-readable MIPS assembly instructions.
It supports a subset of instructions (R-type, I-type, and J-type) based on the MIPS_FORMAT and MIPS_REGISTERS dictionaries.
This version is designed for educational purposes and can be extended to support additional instructions.

Usage:
    python disassembler.py

Author: Sabneet Bains
License: MIT
"""

from typing import List, Dict

# List of machine code instructions to disassemble
instructions: List[str] = [
    '00000001101011100101100000100100',  # R-type: add $t3, $t5, $t2 (example)
    '10001101010010010000000000001000',  # I-type: lw $t9, 0($a0)
    '00001000000000010010001101000101',  # J-type: j <address>
    '00000010101010010101100000100010',  # R-type: sub $t2, $t5, $t1 (example)
    '00000011111000000000000000001000',  # R-type: jr $ra (example)
    '00110101111100001011111011101111',  # I-type: ori $t7, $t7, <immediate> (example)
    '10101110100011010000000000100000',  # I-type: sw $t5, 32($a0) (example)
    '00000010110011010101000000100000'   # R-type: add $t2, $t6, $t5 (example)
]

# MIPS format dictionary
MIPS_FORMAT: Dict[str, List[str]] = {
    'Mnemonic': ['add','addi','addiu','addu','and','andi','beq','blez','bne','bgtz','div','divu',
                 'j','jal','jr','lb','lbu','lhu','lui','lw','mfhi','mthi','mflo','mtlo','mfc0',
                 'mult','multu','nor','xor','or','ori','sb','sh','slt','slti','sltiu','sltu',
                 'sll','srl','sra','sub','subu','sw'],
    'Type':     ['R','I','I','R','R','I','I','I','I','I','R','R','J','J','R','I','I','I','I','I',
                 'R','R','R','R','R','R','R','R','R','R','I','I','I','R','I','I','R','R','R','R','R','R','I'],
    'Opcode':   ['000000','001000','001001','000000','000000','001100','000100','000110','000101',
                 '000111','000000','000000','000010','000011','000000','100000','100100','100101',
                 '001111','100011','000000','000000','000000','000000','010000','000000','000000',
                 '000000','000000','000000','001101','101000','101001','000000','001010','001011',
                 '000000','000000','000000','000000','000000','000000','101011'],
    'Funct':    ['100000','NA','NA','100001','100100','NA','NA','NA','NA','NA','011010','011011',
                 'NA','NA','001000','NA','NA','NA','NA','NA','010000','010001','010010','010011',
                 'NA','011000','011001','100111','100110','100101','NA','NA','NA','101010','NA',
                 'NA','101011','000000','000010','000011','100010','100011','NA']
}

# MIPS Registers dictionary (binary to register name mapping)
MIPS_REGISTERS: Dict[str, str] = {
    '00000': '$zero', '00001': '$at', '00010': '$v0', '00011': '$v1',
    '00100': '$a0',   '00101': '$a1', '00110': '$a2', '00111': '$a3',
    '01000': '$t0',   '01001': '$t1', '01010': '$t2', '01011': '$t3',
    '01100': '$t4',   '01101': '$t5', '01110': '$t6', '01111': '$t7',
    '10000': '$s0',   '10001': '$s1', '10010': '$s2', '10011': '$s3',
    '10100': '$s4',   '10101': '$s5', '10110': '$s6', '10111': '$s7',
    '11000': '$t8',   '11001': '$t9', '11010': '$k0', '11011': '$k1',
    '11100': '$gp',   '11101': '$sp', '11110': '$fp', '11111': '$ra'
}


def disassemble_R_type(instr: str, index: int) -> str:
    """
    Disassemble an R-type instruction.
    
    Args:
        instr: A 32-bit binary string.
        index: Index in the MIPS_FORMAT lists corresponding to the instruction.
        
    Returns:
        A disassembled assembly instruction as a string.
    """
    rs_bin = instr[6:11]
    rt_bin = instr[11:16]
    rd_bin = instr[16:21]
    mnemonic = MIPS_FORMAT['Mnemonic'][index]
    # Construct the assembly string using register names
    assembly = f"{mnemonic} {MIPS_REGISTERS.get(rd_bin, 'unknown')}, {MIPS_REGISTERS.get(rs_bin, 'unknown')}, {MIPS_REGISTERS.get(rt_bin, 'unknown')}"
    return assembly


def disassemble_I_type(instr: str, index: int) -> str:
    """
    Disassemble an I-type instruction.
    
    Args:
        instr: A 32-bit binary string.
        index: Index in the MIPS_FORMAT lists corresponding to the instruction.
        
    Returns:
        A disassembled assembly instruction as a string.
    """
    rs_bin = instr[6:11]
    rt_bin = instr[11:16]
    immediate_bin = instr[16:32]
    mnemonic = MIPS_FORMAT['Mnemonic'][index]
    immediate = int(immediate_bin, 2)
    assembly = f"{mnemonic} {MIPS_REGISTERS.get(rt_bin, 'unknown')}, {MIPS_REGISTERS.get(rs_bin, 'unknown')}, {hex(immediate)}"
    return assembly


def disassemble_J_type(instr: str, index: int) -> str:
    """
    Disassemble a J-type instruction.
    
    Args:
        instr: A 32-bit binary string.
        index: Index in the MIPS_FORMAT lists corresponding to the instruction.
        
    Returns:
        A disassembled assembly instruction as a string.
    """
    immediate_bin = instr[6:32]
    mnemonic = MIPS_FORMAT['Mnemonic'][index]
    immediate = int(immediate_bin, 2)
    assembly = f"{mnemonic} {hex(immediate)}"
    return assembly


def disassemble_instruction(instr: str) -> None:
    """
    Disassembles a single 32-bit machine code instruction and prints the result.
    
    Args:
        instr: A 32-bit binary string.
    """
    opcode = instr[0:6]
    if opcode in MIPS_FORMAT['Opcode']:
        # R-type instructions have opcode '000000'
        if opcode == '000000':
            func_code = instr[26:32]
            if func_code in MIPS_FORMAT['Funct']:
                index = MIPS_FORMAT['Funct'].index(func_code)
                assembly = disassemble_R_type(instr, index)
                print('________________________________________')
                print(f"| Disassembled MIPS R-type Instruction:")
                print(f"| ⦿  {assembly}")
                print("↸----------------------------------------\n")
            else:
                print(f"Unsupported function code: {func_code}")
        else:
            index = MIPS_FORMAT['Opcode'].index(opcode)
            inst_type = MIPS_FORMAT['Type'][index]
            if inst_type == 'I':
                assembly = disassemble_I_type(instr, index)
                print('________________________________________')
                print(f"| Disassembled MIPS I-type Instruction:")
                print(f"| ⦿  {assembly}")
                print("↸----------------------------------------\n")
            elif inst_type == 'J':
                assembly = disassemble_J_type(instr, index)
                print('________________________________________')
                print(f"| Disassembled MIPS J-type Instruction:")
                print(f"| ⦿  {assembly}")
                print("↸----------------------------------------\n")
            else:
                print(f"Unsupported instruction type: {inst_type}")
    else:
        print(f"Opcode {opcode} not recognized.")


def main() -> None:
    for instr in instructions:
        try:
            disassemble_instruction(instr)
        except Exception as e:
            print(f"Error disassembling instruction {instr}: {e}")


if __name__ == "__main__":
    main()
