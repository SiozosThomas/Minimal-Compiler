import sys
from yac import yac

yac_ob = yac()
input_file = input("Give a file: ")
yac_ob.set_file(input_file)
yac_ob.set_first_token()
yac_ob.program()
