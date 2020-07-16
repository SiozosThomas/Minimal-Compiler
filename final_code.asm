L0:
	j Lmain
L1:
	sw $ra, -0($sp)
L2:
	lw $t1,-12($s0)
	lw $t2,-16($s0)
	blt $t1, $t2, L4
L3:
	j L6
L4:
	li $v0, 1
	lw $a0,-16($s0)
	syscall
L5:
	j L1
L6:
	lw $ra, -0($sp)
	jr $ra
Lmain:
L7:
	addi $sp, $sp,28
	move $s0, $sp
L8:
	li $t1,8
	sw $t1,-16($sp)
L9:
L10:
