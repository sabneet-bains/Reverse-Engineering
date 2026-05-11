# Representative FPU and COP0 example
    mtc1 $t0, $f4
    add.s $f6, $f4, $f8
    mfc1 $t1, $f6
    mfc0 $t2, $status
    mtc0 $t2, $epc
    eret
