import sys

class final_code():

    def __init__(self, symbol_table_list):
        self.symbol_table_list = symbol_table_list
        self.function = None
        self.case = ""
        self.offset = 0

    def write_final_code(self, result):
        f = open("final_code.asm", "w")
        f.write(result)
        f.close()

    def get_offset(self):
        return self.offset

    def set_function_name(self, function_name):
        self.current_function_name = function_name

    def gnvlcode(self, v):
        count = 0
        self.offset = self.search_in_function(v)
        result = ""
        while self.offset == -1:
            self.current_function_name = self.function.get_parent()
            if self.current_function_name == "":
                count = -1
                break
            if count == 0:
                result += ("\tlw $t0, -4($sp)\n")
            else:
                result += ("\tlw $t0, -4($t0)\n")
            count += 1
            self.offset = self.search_in_function(v)
        if count == 0:
            result += ("\tlw $t0, -4($sp)\n")
        if count == -1:
            print("Variable with name: " +str(v) + ", hasn't declared...")
            sys.exit()
        else:
            result += ("\taddi $t0, $t0, -" + str(self.offset) + "\n")
        return result

    def loadvr(self, v, r):
        function = self.get_function()
        flag = False
        result = ""
        if v.isdigit():
            self.case = "constant"
            result += ("\tli " + str(r) + "," + str(v) + "\n")
            flag = True
        elif self.is_global(v):
            index = self.symbol_table_list[0].get_variables().index(v)
            self.offset = 12 + index * 4
            result += ("\tlw " + str(r) + ",-" + str(self.offset) + "($s0)\n")
            flag = True
        elif self.is_local(v, function):
            index = function.get_variables().index(v)
            self.offset = 12 + (index) * 4
            if index < len(function.get_pars_type()):
                if self.is_inout(v, function, index):
                    result += ("\tlw $t0, -" + str(self.offset) + "($sp)\n")
                    result += ("\tlw " + str(r) + ", ($t0)\n")
                    flag = True
            else:
                result += ("\tlw " + str(r) + ", -" + str(self.offset) + "($sp)\n")
                flag = True
        if flag == False:
            result += self.gnvlcode(v)
            self.case = "parent"
            if v in self.function.get_variables():
                index = self.function.get_variables().index(v)
                if index < len(self.function.get_pars_type()):
                    self.case = "parent_ref"
                    if self.function.get_pars_type()[index] == "inout":
                        self.offset = 12 + (index) * 4
                        result += ("\tlw $t0, ($t0)\n")
            #print("sw " + str(r) + ", ($t0)")
        return result

    def is_global(self, v):
        if v in self.symbol_table_list[0].get_variables():
            self.case = "global"
            return True
        return False

    def is_local(self, v, function):
        if v in function.get_variables():
            self.case = "local"
            return True
        return False

    def is_inout(self, v, function, index):
        if function.get_pars_type()[index] == "inout":
            self.case = "local_ref"
            return True
        return False

    def storev(self, r, v):
        function = self.get_function()
        result = ""
        if self.case == "global":
            index = self.symbol_table_list[0].get_variables().index(v)
            self.offset = 12 + index * 4
            result += ("\tsw " + str(r) + ", -" + str(self.offset) + "($s0)\n")
        elif self.case == "local" or self.case == "constant":
            index = function.get_variables().index(v)
            self.offset = 12 + (index) * 4
            result += ("\tsw " + str(r) + ",-" + str(self.offset) + "($sp)\n")
        elif self.case == "local_ref":
            index = function.get_variables().index(v)
            self.offset = 12 + (index) * 4
            result += ("\tlw $t0, -" + str(self.offset) + "($sp)\n")
            result += ("\tsw " + str(r) + ",($t0)\n")
        elif self.case == "parent":
            result += self.gnvlcode(v)
            result += ("\tsw " + str(r) + ",($t0)\n")
        elif self.case == "parent_ref":
            result += self.gnvlcode(v)
            result += ("\tlw $t0,($t0)\n")
            result += ("\tsw " + str(r) + ",($t0)\n")
        return result

    def get_function(self):
        for function in self.symbol_table_list:
            if function.get_function_name() == self.current_function_name:
                return function
        print("Can't find function with name: " + str(self.current_function_name))
        sys.exit()

    def get_function_x(self, function_x):
        for function in self.symbol_table_list:
            if function.get_function_name() == function_x:
                return function
        print("Can't find function with name: " + str(self.function_x))
        sys.exit()

    def search_in_function(self, v):
        self.function = self.get_function()
        function_vars = self.function.get_variables()
        for i in range(0, len(function_vars)):
            if function_vars[i] == v:
                return 4 * (i + 3)
        return -1

class read_semi_code():

    def __init__(self, all_quads, symbol_table_list):
        self.all_quads = all_quads
        self.symbol_table_list = symbol_table_list
        self.final_code = final_code(self.symbol_table_list)
        self.label = 0
        self.function_begin = {}

    def write_result(self, result):
        self.final_code.write_final_code(result)

    def read_quads(self):
        pars = []
        result = ""
        result += ("L" + str(self.label) + ":\n\tj Lmain\n")
        self.label += 1
        for quad in self.all_quads:
            if not self.is_main_name(quad[1]) and not quad[0] == "par"\
                and not quad[0] == "call":
                result += ("L" + str(self.label) + ":\n")
            if self.is_begin_block_label(quad[0]):
                self.function_begin[quad[1]] = "L" + str(self.label)
                if self.is_main_name(quad[1]):
                    result += self.write_lmain()
                else:
                    result += ("\tsw $ra, -0($sp)\n")
                self.final_code.set_function_name(quad[1])
            elif self.is_end_block_label(quad[0]):
                if not self.is_main_name(quad[1]):
                    result += ("\tlw $ra, -0($sp)\n")
                    result += ("\tjr $ra\n")
                else:
                    result += ("L" + str(self.label) + ":\n")
            elif self.is_return_label(quad[0]):
                result += self.final_code.loadvr(quad[1], "$t1")
                result += ("\tlw $t1,-8($sp)\n")
                result += ("\tsw $t1,($t0)\n")
            elif self.is_in_label(quad[0]):
                result += ("\tli $v0, 5\n")
                result += ("\tsyscall\n")
                result += self.final_code.storev("$v0", quad[1])
            elif self.is_out_label(quad[0]):
                result += ("\tli $v0, 1\n")
                result += self.final_code.loadvr(quad[1], "$a0")
                result += ("\tsyscall\n")
            elif self.is_relop(quad[0]):
                result += self.final_code.loadvr(quad[1], "$t1")
                result += self.final_code.loadvr(quad[2], "$t2")
                result += ("\t" + str(self.get_relop(quad[0])) +\
                                " $t1, $t2, L" +str(quad[3])  + "\n")
            elif self.is_op(quad[0]):
                result += self.final_code.loadvr(quad[1], "$t1")
                result += self.final_code.loadvr(quad[2], "$t2")
                result += ("\t" + str(self.get_op(quad[0])) + " $t1, $t1, $t2\n")
                result += self.final_code.storev("$t1", quad[3])
            elif self.is_assign_label(quad[0]):
                result += self.final_code.loadvr(quad[1], "$t1")
                result += self.final_code.storev("$t1", quad[3])
            elif self.is_par_label(quad[0]):
                pars.append("L" + str(self.label) + ":")
                function = self.final_code.get_function()
                if self.is_cv(quad[3]):
                    pars.append(self.final_code.loadvr(quad[2], "$t0"))
                    index = function.get_variables().index(quad[2])
                    offset = 12 + 4 * index
                    pars.append("\tsw $t0, -" + str(offset) + "($fp)")
                elif self.is_ref(quad[3]):
                    if quad[2] in function.get_variables():
                        flag, offset = self.find_if_par_is_inout(quad[2],\
                                                                    function)
                        if flag == True:#Anafora idio vathos
                            pars.append("\tlw $t0,-" + str(offset) + "($sp)")
                            pars.append("\tsw $t0,-" + str(offset) + "($fp)")
                        if flag == False:#Topikh h me timh, idio vathos
                            pars.append("\taddi $t0,$sp,-" + str(offset))
                            pars.append("\tsw $t0,-" + str(offset) + "($fp)")
                    else: #allo vathos
                        pars.append(self.final_code.gnvlcode(quad[2]))
                        function = self.final_code.get_function()
                        if quad[2] in function.get_variables():
                            flag, offset = self.find_if_par_is_inout(quad[2],\
                                                                    function)
                            if flag == True:#Anafora allo vathos
                                pars.append("\tlw $t0,($t0)")
                                pars.append("\tsw $t0,-" + str(self.final_code.\
                                                    get_offset()) + "($fp)")
                            if flag == False:#Topikh h me timh, allo vathos
                                pars.append("\tsw $t0,-" + str(self.final_code.\
                                                    get_offset()) + "($fp)")
                else:
                    index = function.get_variables().index(quad[2])
                    offset = 12 + 4 * index
                    pars.append("\taddi $t0, $sp, -" + str(offset))
                    pars.append("\tsw $t0,-8($fp)")
            elif self.is_call_label(quad[0]):
                function = self.final_code.get_function()
                call_function = self.final_code.get_function_x(quad[1])
                count = 0
                for par in pars:
                    result += (str(par) + "\n")
                    if count == 0: result += ("\taddi $fp, $sp, " +\
                                        str(call_function.get_offset()) + "\n")
                    count += 1
                pars = []
                result += ("L" + str(self.label) + ":\n")
                if function.get_nesting_level() == call_function.get_nesting_level():
                    result += ("\tlw $t0,-4($sp)\n")
                    result += ("\tsw $t0,-4($fp)\n")
                else:
                    result += ("\tsw $sp,-4($fp)\n")
                result += ("\taddi $sp, $sp, " + str(call_function.get_offset())\
                                                                        + "\n")
                result += ("\tjal " + self.find_function_label\
                                    (call_function.get_function_name()) + "\n")
                result += ("\taddi $sp, $sp, -" + str(call_function.get_offset())\
                                                                        + "\n")
            elif quad[0] == "jump":
                result += ("\tj L" + str(quad[3]) + "\n")
            self.label += 1
        self.write_result(result)

    def is_main_name(self, function_name):
        if function_name == self.symbol_table_list[0].get_function_name():
            return True
        return False

    def is_begin_block_label(self, x):
        if x == "begin_block":
            return True
        return False

    def is_end_block_label(self, x):
        if x == "end_block":
            return True
        return False

    def is_return_label(self, x):
        if x == "retv":
            return True
        return False

    def is_in_label(self, x):
        if x == "in":
            return True
        return False

    def is_out_label(self, x):
        if x == "out":
            return True
        return False

    def is_assign_label(self, x):
        if x == ":=":
            return True
        return False

    def is_par_label(self, x):
        if x == "par":
            return True
        return False

    def is_call_label(self, x):
        if x == "call":
            return True
        return False

    def is_cv(self, x):
        if x == "CV":
            return True
        return False

    def is_ref(self, x):
        if x == "REF":
            return True
        return False

    def is_relop(self, x):
        if x == ">" or x == ">=" or x == "<" or\
                        x == "<=" or x == "<>" or x == "=":
            return True
        return False

    def get_relop(self, x):
        if x == ">":
            return "bgt"
        elif x == ">=":
            return "bge"
        elif x == "<":
            return "blt"
        elif x == "<=":
            return "ble"
        elif x == "<>":
            return "bne"
        elif x == "=":
            return "beq"
        print("Label: " + str(self.label) + ", not valid relop...")
        sys.exit()

    def is_op(self, x):
        if x == "+" or x == "-" or x == "*" or x == "/":
            return True
        return False

    def get_op(self, x):
        if x == "+":
            return "add"
        elif x == "-":
            return "sub"
        elif x == "*":
            return "mul"
        elif x == "/":
            return "div"
        print("Label: " + str(self.label) + ", not valid op")
        sys.exit()

    def find_function_label(self, x):
        for key, value in self.function_begin.items():
            if key == x:
                return value
        print("Can't find function: " + x)
        sys.exit()

    def find_if_par_is_inout(self, par, function):
        index = function.get_variables().index(par)
        offset = 12 + 4 * index
        if index < len(function.get_pars_type_as_list()):
            if function.get_pars_type_as_list()[index] == "io": #Me anafora
                return True, offset
        return False, offset

    def write_lmain(self):
        result = ("Lmain:\n")
        result += self.write_next_lmain_label()
        return result

    def write_next_lmain_label(self):
        result = ("L" + str(self.label) + ":\n")
        result += ("\taddi $sp, $sp," + str(self.symbol_table_list[0].\
                                                        get_offset()) + "\n")
        result += ("\tmove $s0, $sp\n")
        return result
