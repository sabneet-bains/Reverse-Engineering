# list of instructions
instructions = ['00000001101011100101100000100100', '10001101010010010000000000001000', '00001000000000010010001101000101', '00000010101010010101100000100010', '00000011111000000000000000001000', '00110101111100001011111011101111', '10101110100011010000000000100000', '00000010110011010101000000100000']

# MIPS format dictionary
MIPS_FORMAT = {
    'Mnemonic': ['add','addi','addiu','addu','and','andi','beq','blez','bne','bgtz','div','divu','j','jal','jr','lb','lbu','lhu','lui','lw','mfhi','mthi','mflo','mtlo','mfc0','mult','multu','nor','xor','or','ori','sb','sh','slt','slti','sltiu','sltu','sll','srl','sra','sub','subu','sw'],
    
    'Type': ['R','I','I','R','R','I','I','I','I','I','R','R','J','J','R','I','I','I','I','I','R','R','R','R','R','R','R','R','R','R','I','I','I','R','I','I','R','R','R','R','R','R','I'],
    
    'Opcode': ['000000','001000','001001','000000','000000','001100','000100','000110','000101','000111','000000','000000','000010','000011','000000','100000','100100','100101','001111','100011','000000','000000','000000','000000','010000','000000','000000','000000','000000','000000','001101','101000','101001','000000','001010','001011','000000','000000','000000','000000','000000','000000','101011'],
    
    'Funct': ['100000','NA','NA','100001','100100','NA','NA','NA','NA','NA','011010','011011','NA','NA','001000','NA','NA','NA','NA','NA','010000','010001','010010','010011','NA','011000','011001','100111','100110','100101','NA','NA','NA','101010','NA','NA','101011','000000','000010','000011','100010','100011','NA']}

# MIPS Registers dictionary
MIPS_REGISTERS = {'00000': '$zero', '00001': '$at', '00010': '$v0', '00011': '$v1', '00100': '$a0', '00101': '$a1', '00110': '$a2', '00111': '$a3', '01000': '$t0', '01001': '$t1', '01010': '$t2', '01011': '$t3', '01100': '$t4', '01101': '$t5', '01110': '$t6', '01111': '$t7', '10000': '$s0', '10001': '$s1', '10010': '$s2', '10011': '$s3', '10100': '$s4', '10101': '$s5', '10110': '$s6', '10111': '$s7', '11000': '$t8', '11001': '$t9', '11010': '$k0', '11011': '$k1', '11100': '$gp',
'11101': '$sp', '11110': '$fp', '11111': '$ra'}

# Loop over all of the instructions
for i in range (len(instructions)):

    # get opcode
    opcode = instructions[i][0:6]

    # check if the given opcode actually exists in the dictionary
    if(opcode in MIPS_FORMAT['Opcode']):

        # Logic in case, the instruction is a R-type
        if(opcode == '000000'):
            func_code = instructions[i][26:32]
            index = MIPS_FORMAT['Funct'].index(func_code)

            if(func_code in MIPS_FORMAT['Funct']):

                rs_register = instructions[i][6:11]
                rt_register = instructions[i][11:16]
                rd_register = instructions[i][16:21]

                print('________________________________________\n| Disassembled MIPS ' + MIPS_FORMAT['Type'][index] + '-type Instruction:  \n| ⦿  '+ MIPS_FORMAT['Mnemonic'][index] + ' ' + MIPS_REGISTERS[rd_register] + ', ' + MIPS_REGISTERS[rs_register] + ', ' + MIPS_REGISTERS[rt_register] + '\n↸---------------------------------\n')
        
        # when not a R-type
        else:
            index = MIPS_FORMAT['Opcode'].index(opcode)

            # Logic in case, the instruction is an I-type
            if(MIPS_FORMAT['Type'][index] == 'I'):
                immediate = instructions[i][16:32]
                rs_register = instructions[i][6:11]
                rt_register = instructions[i][11:16]

                print('________________________________________\n| Disassembled MIPS ' + MIPS_FORMAT['Type'][index] + '-type Instruction:  \n| ⦿  '+ MIPS_FORMAT['Mnemonic'][index] + ' ' + MIPS_REGISTERS[rt_register] + ', ' + MIPS_REGISTERS[rs_register] + ', ' + hex(int(immediate,2)) + '\n↸---------------------------------\n')
            
            # Logic in case, the instruction is a J-type
            elif(MIPS_FORMAT['Type'][index] == 'J'):
                immediate = instructions[i][6:32]

                print('________________________________________\n| Disassembled MIPS ' + MIPS_FORMAT['Type'][index] + '-type Instruction:  \n| ⦿  '+ MIPS_FORMAT['Mnemonic'][index] +  ' ' + hex(int(immediate,2)) + '\n↸---------------------------------\n')