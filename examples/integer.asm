# MIPS32 integer and label example
main:
    addi $v0, $zero, 4
    add $t0, $t1, $t2
    beq $t0, $zero, done
    sw $t0, 8($sp)
done:
    jr $ra
