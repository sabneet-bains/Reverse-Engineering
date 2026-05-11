# Guided tutorial program
start:
    addi $v0, $zero, 4
    lw $t1, 8($t2)
    beq $t1, $zero, done
    j 0x10
done:
    li $t0, 0x12345678
    ld $t2, 16($sp)
