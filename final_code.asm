L0:
	j Lmain
L1:
	sw $ra, -0($sp)
L2:
	lw $t1,-12($s0)
	lw $t2,-16($s0)
	bge $t1, $t2, L5
L3:
	lw $t1,-16($s0)
	lw $t2,-20($s0)
	bge $t1, $t2, L5
L4:
	lw $t1,-12($s0)
	lw $t2,-16($s0)
	blt $t1, $t2, L5
L5:
	j L7
L6:
	lw $t1,-12($s0)
	li $t2,8
	add $t1, $t1, $t2
	sw $t1,-16($sp)
L7:
	lw $t0, -4($sp)
	addi $t0, $t0, -16
	lw $t1,-8($sp)
	sw $t1,($t0)
L8:
	lw $ra, -0($sp)
	jr $ra
Lmain:
L9:
	addi $sp, $sp,44
	move $s0, $sp
L10:
	li $t1,8
	li $t2,2
	add $t1, $t1, $t2
	sw $t1,-24($sp)
L11:
	li $t1,8
	lw $t2,-24($s0)
	sub $t1, $t1, $t2
	sw $t1, -28($s0)
L12:
	li $t1,4
	li $t2,1
	add $t1, $t1, $t2
	sw $t1,-32($sp)
L13:
	lw $t1,-28($s0)
	lw $t2,-32($s0)
	mul $t1, $t1, $t2
	sw $t1, -36($s0)
L14:
	li $v0, 1
	lw $a0,-36($s0)
	syscall
L15:
	addi $fp, $sp, 20
	lw $t0,-12($s0)

	sw $t0, -12($fp)
L16:
	addi $t0, $sp, -40
	sw $t0,-8($fp)
L17:
	sw $sp,-4($fp)
	addi $sp, $sp, 20
	jal L1
	addi $sp, $sp, -20
L18:
	lw $t1,-40($s0)
	sw $t1, -12($s0)
L19:
L20:
