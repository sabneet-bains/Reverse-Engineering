instructions = [['addi', '$v0', '$zero', '0'], ['lw', '$t9', '0', '$a0'], ['addi', '$v0', '$v0', '1'], ['sw', '$t9', '$0', '$a1'], ['addi', '$a0', '$a0', '4'], ['addi', '$a1', '$a1', '4']]

MIPS_FORMAT = {
    'Mnemonic': ['add','addi','addiu','addu','and','andi','beq','blez','bne','bgtz','div','divu','j','jal','jr','lb','lbu','lhu','lui','lw','mfhi','mthi','mflo','mtlo','mfc0','mult','multu','nor','xor','or','ori','sb','sh','slt','slti','sltiu','sltu','sll','srl','sra','sub','subu','sw'],
    
    'Type': ['R','I','I','R','R','I','I','I','I','I','R','R','J','J','R','I','I','I','I','I','R','R','R','R','R','R','R','R','R','R','I','I','I','R','I','I','R','R','R','R','R','R','I'],
    
    'Opcode': ['000000','001000','001001','000000','000000','001100','000100','000110','000101','000111','000000','000000','000010','000011','000000','100000','100100','100101','001111','100011','000000','000000','000000','000000','010000','000000','000000','000000','000000','000000','001101','101000','101001','000000','001010','001011','000000','000000','000000','000000','000000','000000','101011'],
    
    'Funct': ['100000','NA','NA','100001','100100','NA','NA','NA','NA','NA','011010','011011','NA','NA','001000','NA','NA','NA','NA','NA','010000','010001','010010','010011','NA','011000','011001','100111','100110','100101','NA','NA','NA','101010','NA','NA','101011','000000','000010','000011','100010','100011','NA']}

MIPS_REGISTERS = {'$0': '00000', '$zero': '00000', '$at': '00001', '$v0': '00010', '$v1': '00011', '$a0': '00100', '$a1': '00101', '$a2': '00110', '$a3': '00111', '$t0': '01000', '$t1': '01001', '$t2': '01010', '$t3': '01011', '$t4': '01100', '$t5': '01101', '$t6': '01110', '$t7': '01111', '$s0': '10000', '$s1': '10001', '$s2': '10010', '$s3': '10011', '$s4': '10100', '$s5': '10101', '$s6': '10110', '$s7': '10111', '$t8': '11000', '$t9': '11001', '$k0': '11010', '$k1': '11011', '$gp': '11100','$sp': '11101', '$fp': '11110', '$ra': '11111'}

for i in range (len(instructions)):

    if (instructions[i][0] in MIPS_FORMAT['Mnemonic']):
        index = MIPS_FORMAT['Mnemonic'].index(instructions[i][0])

        if(MIPS_FORMAT['Type'][index] == 'R'):
            opcode = MIPS_FORMAT['Opcode'][index]
            rs_register = instructions[i][2]
            rt_register = instructions[i][3]
            rd_register = instructions[i][1]
            shamt = '00000'
            func_code = MIPS_FORMAT['Funct'][index]
            
            print('______________________________________\n| Assembled MIPS ' + MIPS_FORMAT['Type'][index] + '-type Machine Code | \n\n⦿  decimal:', int(opcode,2), int(MIPS_REGISTERS[rs_register],2), int(MIPS_REGISTERS[rt_register],2), int(MIPS_REGISTERS[rd_register],2), int(shamt,2), int(func_code,2), '\n⦿  binary:', opcode, MIPS_REGISTERS[rs_register], MIPS_REGISTERS[rt_register], MIPS_REGISTERS[rd_register], shamt, func_code, '\n⦿  hexadecimal:',hex(int(opcode + MIPS_REGISTERS[rs_register] + MIPS_REGISTERS[rt_register] + MIPS_REGISTERS[rd_register] + shamt + func_code,2)))

        elif(MIPS_FORMAT['Type'][index] == 'I'):
            opcode = MIPS_FORMAT['Opcode'][index]

            if ('$' not in instructions[i][2]):
                rs_register = bin(int(instructions[i][2],16))
                rs_register = rs_register.replace('0b', '')
            else:
                rs_register = MIPS_REGISTERS[instructions[i][2]]

            if len(rs_register) != 5:
                rs_register = '{:>05d}'.format(int(rs_register))

            if ('$' not in instructions[i][1]):
                rt_register = bin(int(instructions[i][1],16))
                rt_register = rt_register.replace('0b', '')
            else:
                rt_register = MIPS_REGISTERS[instructions[i][1]]

            if len(rt_register) != 5:
                rt_register = '{:>05d}'.format(int(rt_register))
            
            if ('$' not in instructions[i][3]):
                immediate = bin(int(instructions[i][3],16))
                immediate = immediate.replace('0b', '')
            else:
                immediate = MIPS_REGISTERS[instructions[i][3]]

            if len(immediate) != 16:
                immediate = '{:>016d}'.format(int(immediate))

            print('______________________________________\n| Assembled MIPS ' + MIPS_FORMAT['Type'][index] + '-type Machine Code | \n\n⦿  decimal:', int(opcode,2), int(rs_register,2), int(rt_register,2), int(immediate,2), '\n⦿  binary:', opcode, rs_register, rt_register, immediate, '\n⦿  hexadecimal:',hex(int(opcode + rs_register + rt_register + immediate,2)))

        elif(MIPS_FORMAT['Type'][index] == 'J'):
            opcode = MIPS_FORMAT['Opcode'][index]
            immediate = bin(int(instructions[i][1],16))
            immediate = immediate.replace('0b', '')

            if len(immediate) != 26:
                immediate = '{:>026d}'.format(int(immediate))

            print('______________________________________\n| Assembled MIPS ' + MIPS_FORMAT['Type'][index] + '-type Machine Code | \n\n⦿  decimal:', int(opcode,2), int(immediate,2), '\n⦿  binary:', opcode, immediate, '\n⦿  hexadecimal:',hex(int(opcode + immediate,2)))