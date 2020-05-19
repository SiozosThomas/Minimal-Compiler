import sys

class operation(): #krataei tis pra3eis ta +,-klp

    def __init__(self):
        self.values = []    #gia oles tis times(metavlhtes - arithmous)
        self.last = ""      #O teleutaios xarakthras(T_0 h metavlhth)
        self.last_rel = ""  #To teleutaio relational oper

    def get_values(self):
        return self.values

    def get_last(self):
        return self.last

    def set_last(self, last):
        self.last = last

    def add(self, x):
        self.values.append(x)

    def get_last_value(self):
        if len(self.values) >= 1:
            return self.values[len(self.values) - 1]

    def create_quads(self, semi_code, values, function):
        semi_code.set_function(function)
        last = ""       #Gia thn anadromh
        i = 0           #counter
        while i < len(values):
            if values[i].isalpha() or values[i].isdigit():
                self.last = values[i]
                last = values[i]
            if values[i] == "(":    #a + (a + b)
                nested = []         #lista san to values alla gia na nested (auta mesa sti parenthesdi)
                i += 1              #Diavasame to '(' opote den to theloume allo
                while i < len(values) and values[i] != ")":
                    nested.append(values[i])
                    i += 1
                nested_last = self.create_quads(semi_code, nested, function)
                semi_code.gen_quad(self.last_rel, last, nested_last,
                                    semi_code.new_temp())
                semi_code.next_quad()
                last = semi_code.get_temp()
                self.last = semi_code.get_temp()
            elif values[i] == "+" or "-" or "*" or "/":
                if i >= 1 and i <= len(values) - 2:
                    if values[i + 1] != "(":
                        semi_code.gen_quad(values[i], values[i - 1],
                                    values[i + 1], semi_code.new_temp())
                        semi_code.next_quad()
                        last = semi_code.get_temp()
                        self.last = semi_code.get_temp()
                        i += 1
                    elif values[i + 1] == "(":  #a + (b + a)
                        self.last_rel = values[i]
            i += 1
        return last

    def print_values(self):
        print(self.values)

    def clear_values(self):
        self.values = []
