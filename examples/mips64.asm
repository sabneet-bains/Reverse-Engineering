# Representative MIPS64 integer example
    daddiu $t0, $zero, 42
    ld $t1, 16($sp)
    daddu $t2, $t0, $t1
    sd $t2, 24($sp)
    dsll $t3, $t2, 2
