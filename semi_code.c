int main()
{
	int a, b, c, T_0, T_1, T_2, T_3, T_4, T_5;
	L_1:
	L_2: a>=b goto L_5;
	L_3: b>=c goto L_5;
	L_4: a<b goto L_5;
	L_5: goto L_7;
	L_5: T_0 = a+8;
	L_6: T_1 = 8+2;
	L_7: T_2 = 8-T_1;
	L_8: T_3 = 4+1;
	L_9: T_4 = T_2*T_3;
	L_10: print(T_4);
	L_11: a:=T_5;
	L_12: {}
}
