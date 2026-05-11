# Pseudo-instructions expand to real MIPS instructions
start:
    li $t0, 0x12345678
    move $t1, $t0
    clear $t2
    b start
