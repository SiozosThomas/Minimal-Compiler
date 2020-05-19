from lex import lex
from semi_code import semi_code
from operation import operation
from symbol_table import symbol_table
from semi_code_output_file import semi_code_output_file, semi_code_c_file
from final_code import read_semi_code
import sys

class yac():

    def __init__(self):
        self.lex = ""
        self.token = ""
        self.semi_code = semi_code()
        self.op = operation()
        self.left = ""
        self.rel = ""
        self.right = ""
        self.symbol_table_list = []
        self.nesting_level = 0
        self.function_call = ""
        self.function_name_for_table = ""
        self.function_open = 0
        self.not_boolean = False
        self.writer = semi_code_output_file()
        self.writer_to_c = semi_code_c_file()
        self.functions_name = []
        self.read_semi_code = None
        self.pars_call = []

    def set_file(self, file):
        self.lex = lex()
        self.lex.set_file_lines(file)

    def set_first_token(self):
        self.token = self.lex.return_token()

    def get_function(self, x):
        for function in self.symbol_table_list:
            if function.get_function_name() == x:
                return function
        print("Error: Not valid function name: " + str(x))
        sys.exit()
        return None

    def program(self):
        if self.token == "programtk":
            self.token = self.lex.return_token()
            id = self.lex.get_id_value()
            self.functions_name.append(id)
            if self.token == "idtk":
                function = symbol_table(self.nesting_level)
                self.function_name_for_table = self.lex.get_id_value()
                function.set_function_name(self.lex.get_id_value())
                self.symbol_table_list.append(function)
                self.token = self.lex.return_token()
                if self.token == "left_curly_brackettk":
                    self.token = self.lex.return_token()
                    self.block()
                    self.semi_code.gen_quad("halt", "_", "_", "_")
                    self.semi_code.next_quad()
                    self.semi_code.gen_quad("end_block", id, "_", "_")
                    self.semi_code.next_quad()
                    self.semi_code.print_all_quads(self.writer)
                    for i in range(0, self.semi_code.get_temp_var() + 1):
                        self.writer_to_c.add_variable("T_" + str(i))
                    for function in self.symbol_table_list:
                        function.print_function()
                    self.writer_to_c.fill_c_file(self.semi_code.get_all_quads())
                    self.read_semi_code = read_semi_code(self.semi_code.\
                                        get_all_quads(), self.symbol_table_list)
                    self.read_semi_code.read_quads()
                    if self.token == "right_curly_brackettk":
                        print("Your program is compiled succesfully!\n")
                        sys.exit()
                    else:
                        print("Line: " + str(self.lex.get_line()) +
                                "\nSyntax Error: Expected '}' after block\n")
                        sys.exit()
                else:
                    print("Line: " + str(self.lex.get_line()) +
                                "\nSyntax Error: Expected '}' before block\n")
                    sys.exit()
            else:
                print("Line: " + str(self.lex.get_line()) + " Expected id\n")
                sys.exit()

    def block(self):
        self.declarations()
        self.subprograms()
        self.semi_code.gen_quad("begin_block", self.functions_name[-1], "_", "_")
        self.semi_code.next_quad()
        self.statements()

    def declarations(self):
        while self.token == "declaretk":
            self.token = self.lex.return_token()
            self.varlist()
            if self.token == "questiontk":
                self.token = self.lex.return_token()
            else:
                print("Line: " + str(self.lex.get_line()) +
                        "\nSyntax Error: Expected ';' after declaration\n")
                sys.exit()

    def varlist(self):
        if self.token == "idtk":
            function = self.get_function(self.function_name_for_table)
            function.add_variable(self.lex.get_id_value())
            function.set_entity(self.lex.get_id_value())
            self.writer_to_c.add_variable(self.lex.get_id_value())
            self.token = self.lex.return_token()
            while self.token == "commatk":
                self.token = self.lex.return_token()
                if self.token == "idtk":
                    function.add_variable(self.lex.get_id_value())
                    function.set_entity(self.lex.get_id_value())
                    self.writer_to_c.add_variable(self.lex.get_id_value())
                    self.token = self.lex.return_token()
                else:
                    print("Line: " + str(self.lex.get_line()) +
                            "\nSyntax Error: Expected id after comma\n")

    def subprograms(self):
        while self.token == "functiontk" or self.token == "proceduretk":
            self.token = self.lex.return_token()
            self.subprogram()

    def subprogram(self):
        if self.token == "idtk":
            function = self.get_function(self.function_name_for_table)
            function.add_function(self.function_name_for_table)
            name = self.lex.get_id_value()
            if self.check_if_func_exits(name):
                print("Line: " + str(self.lex.get_line()) +
                            "\nCan't have function with same name\n")
                sys.exit()
            self.functions_name.append(name)
            self.function_name_for_table = name
            self.nesting_level += 1
            function = symbol_table(self.nesting_level)
            function.set_parent(self.symbol_table_list[-1].get_function_name())
            function.set_function_name(name)
            self.symbol_table_list.append(function)
            self.token = self.lex.return_token()
            self.funcbody()
            function.set_frame_length()
            function = self.get_function(self.get_function(self.function_name_for_table).\
                                get_parent())
            function.set_entity_function(self.get_function(self.function_name_for_table).\
                            get_function_as_entity())
            self.nesting_level -= 1
            self.functions_name.pop()
            self.function_name_for_table = self.get_function(self.function_name_for_table).get_parent()
            self.semi_code.gen_quad("end_block", name, "_", "_")
            self.semi_code.next_quad()
        else:
            print("Line: " + str(self.lex.get_line()) +
                        " Expected id for subprogram\n")
            sys.exit()

    def funcbody(self):
        self.formalpars()
        if self.token == "left_curly_brackettk":
            self.token = self.lex.return_token()
            self.block()
            if self.token == "right_curly_brackettk":
                self.token = self.lex.return_token()
            else:
                print("Line: " + str(self.lex.get_line()) +
                        "\nSyntax Error: Expected '}' after block\n")
                sys.exit()
        else:
            print("Line: " + str(self.lex.get_line()) +
                        "\nSyntax Error: Expected '{' after block\n")
            sys.exit()

    def formalpars(self):
        if self.token == "left_round_brackettk":
            self.token = self.lex.return_token()
            self.formalparlist()
            if self.token == "right_round_brackettk":
                self.token = self.lex.return_token()
            else:
                print("Line: " + str(self.lex.get_line()) +
                        "\nSyntax Error: Expected ')' after formalparlist\n")
                sys.exit()
        else:
            print("Line: " + str(self.lex.get_line()) +
                    "\nSyntax Error: Expected '(' before formalparlist\n")
            sys.exit()

    def formalparlist(self):
        self.formalparitem()
        while self.token == "commatk":
            self.token = self.lex.return_token()
            self.formalparitem()

    def formalparitem(self):
        function = self.get_function(self.function_name_for_table)
        if self.token == "intk":
            function.add_par_type("in")
            self.token = self.lex.return_token()
            if self.token == "idtk":
                function.add_variable(self.lex.get_id_value())
                function.set_entity(self.lex.get_id_value())
                self.token = self.lex.return_token()
            else:
                print("Line: " + str(self.lex.get_line()) +
                            " Expected id after in\n")
        elif self.token == "inouttk":
            function.add_par_type("io")
            self.token = self.lex.return_token()
            if self.token == "idtk":
                function.add_variable(self.lex.get_id_value())
                function.set_entity(self.lex.get_id_value())
                self.token = self.lex.return_token()
            else:
                print("Line: " + str(self.lex.get_line()) +
                            " Expected id after inout\n")
                sys.exit()

    def statements(self):
        self.statement()
        if self.token == "left_curly_brackettk":
            self.token = self.lex.return_token()
            self.statement()
            while self.token == "questiontk":
                self.token = self.lex.return_token()
                self.statement()
            if self.token == "right_curly_brackettk":
                self.token = self.lex.return_token()
            else:
                print("Line: " + str(self.lex.get_line()) +
                        "\nSyntax Error: Expected '}' after statement\n")
                sys.exit()

    def statement(self):
        if self.token == "idtk":
            self.left = self.lex.get_id_value()
            self.token = self.lex.return_token()
            self.assignment_stat()
        elif self.token == "iftk":
            self.token = self.lex.return_token()
            self.if_stat()
        elif self.token == "whiletk":
            self.token = self.lex.return_token()
            self.while_stat()
        elif self.token == "forcasetk":
            self.token = self.lex.return_token()
            self.forcase_stat()
        elif self.token == "returntk":
            self.token = self.lex.return_token()
            self.return_stat()
        elif self.token == "calltk":
            self.token = self.lex.return_token()
            self.call_stat()
        elif self.token == "printtk":
            self.token = self.lex.return_token()
            self.print_stat()
        elif self.token == "inputtk":
            self.token = self.lex.return_token()
            self.input_stat()

    def assignment_stat(self):
        if self.token == "assignmenttk":
            self.rel = self.lex.get_id_value()
            self.token = self.lex.return_token()
            self.expression()
            self.op.create_quads(self.semi_code, self.op.get_values(),\
                            self.get_function(self.function_name_for_table))
            self.semi_code.gen_quad(self.rel, self.op.get_last(), "_", self.left)
            self.op.clear_values()
        else:
            print("Line: " + str(self.lex.get_line()) +
                    " Expected id assignment\n")
            sys.exit()

    def if_stat(self):
        if self.token == "left_round_brackettk":
            self.token = self.lex.return_token()
            self.semi_code.set_b_quad(self.semi_code.get_label())
            self.condition()
            if self.token == "right_round_brackettk":
                self.token = self.lex.return_token()
                if self.token == "thentk":
                    self.token = self.lex.return_token()
                    self.semi_code.gen_quad("jump", "_", "_", "_")
                    self.semi_code.next_quad()
                    self.semi_code.back_path(self.semi_code.get_label(), "not_jump")
                    self.statements()
                    self.semi_code.back_path(self.semi_code.get_label(), "jump")
                    self.elsepart()
                else:
                    print("Line: " + str(self.lex.get_line()) +
                            "\nSyntax Error: Expected then after ')'\n")
                    sys.exit()
            else:
                print("Line: " + str(self.lex.get_line()) +
                            "\nSyntax Error: Expected ')' after condition\n")
                sys.exit()
        else:
            print("Line: " + str(self.lex.get_line()) +
                    "\nSyntax Error: Expected '(' after if\n")
            sys.exit()

    def elsepart(self):
        if self.token == "elsetk":
            self.token = self.lex.return_token()
            self.statements()


    def while_stat(self):
        if self.token == "left_round_brackettk":
            self.token = self.lex.return_token()
            self.semi_code.set_b_quad(self.semi_code.get_label())
            self.condition()
            self.semi_code.gen_quad("jump", "_", "_", "_")
            self.semi_code.next_quad()
            if self.token == "right_round_brackettk":
                self.semi_code.back_path(self.semi_code.get_label(), "not_jump")
                self.token = self.lex.return_token()
                self.statements()
                self.semi_code.gen_quad("jump", "_", "_", self.semi_code.get_b_quad())
                self.semi_code.next_quad()
                self.semi_code.back_path(self.semi_code.get_label(), "jump")
            else:
                print("Line: " + str(self.lex.get_line()) +
                        "\nSyntax Error: Expected ')' after condition\n")
                sys.exit()
        else:
            print("Line: " + str(self.lex.get_line()) +
                    "\nSyntax Error: Expected '(' after while\n")
            sys.exit()

    def forcase_stat(self):
        self.semi_code.set_b_quad(self.semi_code.get_label())
        self.when_stat()
        if self.token == "defaulttk":
            self.token = self.lex.return_token()
            if self.token == "colontk":
                self.token = self.lex.return_token()
                self.statements()
            else:
                print("Line: " + str(self.lex.get_line()) +
                        "\nSyntax Error: Expected ':' after default\n")
                sys.exit()
        else:
            print("Line: " + str(self.lex.get_line()) +
                    " Expected default for forcase\n")
            sys.exit()

    def when_stat(self):
        while self.token == "whentk":
            self.token = self.lex.return_token()
            if self.token == "left_round_brackettk":
                self.token = self.lex.return_token()
                self.condition()
                if self.token == "right_round_brackettk":
                    self.token = self.lex.return_token()
                    if self.token == "colontk":
                        self.token = self.lex.return_token()
                        self.semi_code.gen_quad("jump", "_", "_", "_")
                        self.semi_code.next_quad()
                        self.semi_code.back_path(self.semi_code.get_label(), "not_jump")
                        self.statements()
                        self.semi_code.back_path(self.semi_code.get_label(), "jump")
                    else:
                        print("Line: " + str(self.lex.get_line()) +
                            "\nSyntax Error: Expected ':' after condition\n")
                        sys.exit()
                else:
                    print("Line: " + str(self.lex.get_line()) +
                            "\nSyntax Error: Expected ')' for condition\n")
                    sys.exit()
            else:
                print("Line: " + str(self.lex.get_line()) +
                        "\nSyntax Error: Expected '(' after when\n")
                sys.exit()

    def return_stat(self):
        self.expression()
        self.op.create_quads(self.semi_code, self.op.get_values(),\
                self.get_function(self.function_name_for_table))
        self.semi_code.gen_quad("retv", self.op.get_last(), "_", "_")
        self.semi_code.next_quad()
        self.op.clear_values()

    def call_stat(self):
        if self.token == "idtk":
            name = self.lex.get_id_value()
            self.token = self.lex.return_token()
            self.op.clear_values()
            if self.token == "left_round_brackettk":
                self.token = self.lex.return_token()
                self.actualpars()
                self.semi_code.gen_quad("call", name, "_", "_")
                self.semi_code.next_quad()
            else:
                print("Line: " + str(self.lex.get_line()) +
                            "\nSyntax Error: Expected '(' before in or inout\n")
                sys.exit()
        else:
            print("Line: " + str(self.lex.get_line()) +
                        " Expected id for call\n")
            sys.exit()

    def print_stat(self):
        if self.token == "left_round_brackettk":
            self.op.clear_values()
            self.token = self.lex.return_token()
            self.expression()
            self.op.create_quads(self.semi_code, self.op.get_values(),\
                        self.get_function(self.function_name_for_table))
            self.semi_code.gen_quad("out", self.op.get_last(), "_", "_")
            self.semi_code.next_quad()
            if self.token == "right_round_brackettk":
                self.token = self.lex.return_token()
            else:
                print("Line: " + str(self.lex.get_line()) +
                        "\nSyntax Error: Expected ')' after expression\n")
                sys.exit()
        else:
            print("Line: " + str(self.lex.get_line()) +
                    "\nSyntax Error: Expected '(' after print\n")
            sys.exit()

    def input_stat(self):
        if self.token == "left_round_brackettk":
            self.token = self.lex.return_token()
            if self.token == "idtk":
                self.semi_code.gen_quad("inp", self.lex.get_id_value(), "_", "_")
                self.semi_code.next_quad()
                self.token = self.lex.return_token()
                if self.token == "right_round_brackettk":
                    self.token = self.lex.return_token()
                else:
                    print("Line: " + str(self.lex.get_line()) +
                            "\nSyntax Error: Expected ')' after id\n")
                    sys.exit()
            else:
                print("Line: " + str(self.lex.get_line()) +
                        " Expected id for input\n")
                sys.exit()
        else:
            print("Line: " + str(self.lex.get_line()) +
                    "\nSyntax Error: Expected '(' after input\n")
            sys.exit()

    def actualpars(self):
        self.actualparlist()
        if self.token == "right_round_brackettk":
            self.token = self.lex.return_token()
        else:
            print("Line: " + str(self.lex.get_line()) +
                    "\nSyntax Error: Expected ')' after expression or id\n")
            sys.exit()

    def actualparlist(self):
        self.actualparitem()
        while self.token == "commatk":
            self.token = self.lex.return_token()
            self.actualparitem()

    def actualparitem(self):
        if self.token == "intk":
            self.pars_call.append("in")
            self.token = self.lex.return_token()
            self.op.clear_values()
            self.expression()
            self.op.create_quads(self.semi_code, self.op.get_values(),\
                        self.get_function(self.function_name_for_table))
            self.semi_code.gen_quad("par", "_", self.op.get_last() ,"CV")
            self.semi_code.next_quad()
            self.op.clear_values()
        elif self.token == "inouttk":
            self.pars_call.append("inout")
            self.token = self.lex.return_token()
            if self.token == "idtk":
                self.semi_code.gen_quad("par", "_",
                        self.lex.get_id_value(), "REF")
                self.semi_code.next_quad()
                self.token = self.lex.return_token()
            else:
                print("Line: " + str(self.lex.get_line()) +
                        " Expected id after inout\n")
                sys.exit()

    def condition(self):
        self.boolterm()
        while self.token == "ortk":
            self.logical = "or"
            self.token = self.lex.return_token()
            self.boolterm()
        self.not_boolean = False

    def boolterm(self):
        self.boolfactor()
        while self.token == "andtk":
            self.logical = "and"
            self.semi_code.gen_quad("jump", "_", "_", "_")
            self.semi_code.next_quad()
            self.token = self.lex.return_token()
            self.semi_code.back_path(self.semi_code.get_label(), "not_jump")  #
            self.boolfactor()

    def boolfactor(self):
        if self.token == "nottk":
            self.not_boolean = True
            self.token = self.lex.return_token()
            if self.token == "left_square_brackettk":
                self.token = self.lex.return_token()
                self.condition()
                if self.token == "right_square_brackettk":
                    self.token = self.lex.return_token()
                else:
                    print("Line: " + str(self.lex.get_line()) +
                            "\nSyntax Error: Expected ']' after condition\n")
                    sys.exit()
            else:
                print("Line: " + str(self.lex.get_line()) +
                        "\nSyntax Error: Expected '[' before condition\n")
                sys.exit()
        elif self.token == "left_square_brackettk":
            self.token = self.lex.return_token()
            self.condition()
            if self.token == "right_square_brackettk":
                self.token = self.lex.return_token()
            else:
                print("Line: " + str(self.lex.get_line()) +
                        "\nSyntax Error: Expected ']' after condition\n")
                sys.exit()
        else:
            self.expression()
            self.op.create_quads(self.semi_code, self.op.get_values(),\
                            self.get_function(self.function_name_for_table))
            self.left = self.op.get_last()
            self.rel = self.lex.get_id_value()
            self.relational_oper()
            self.op.clear_values()
            self.expression()
            self.op.create_quads(self.semi_code, self.op.get_values(),\
                            self.get_function(self.function_name_for_table))
            if self.not_boolean == True:
                if self.rel == ">":
                    self.semi_code.gen_quad("<=", self.left, self.op.get_last(), "_")
                elif self.rel == "<":
                    self.semi_code.gen_quad(">=", self.left, self.op.get_last(), "_")
                elif self.rel == "=":
                    self.semi_code.gen_quad("<>", self.left, self.op.get_last(), "_")
                elif self.rel == "<>":
                    self.semi_code.gen_quad("=", self.left, self.op.get_last(), "_")
                elif self.rel == ">=":
                    self.semi_code.gen_quad("<", self.left, self.op.get_last(), "_")
                elif self.rel == "<=":
                    self.semi_code.gen_quad(">", self.left, self.op.get_last(), "_")
            else:
                self.semi_code.gen_quad(self.rel, self.left, self.op.get_last(), "_")
            self.semi_code.next_quad()
            self.op.clear_values()

    def expression(self):
        self.optional_sign()
        self.term()
        while self.token == "plustk" or self.token == "minustk":
            self.op.add(self.lex.get_id_value())
            self.token = self.lex.return_token()
            self.term()

    def optional_sign(self):
        self.add_oper()

    def term(self):
        self.op.add(self.lex.get_id_value())
        self.factor()
        while self.token == "multiplytk" or self.token == "dividetk":
            self.op.add(self.lex.get_id_value())
            self.token = self.lex.return_token()
            self.op.add(self.lex.get_id_value())
            self.factor()

    def factor(self):
        if self.token == "constanttk":
            self.token = self.lex.return_token()
        elif self.token == "left_round_brackettk":
            self.token = self.lex.return_token()
            self.expression()
            if self.token == "right_round_brackettk":
                self.op.add(self.lex.get_id_value())
                self.token = self.lex.return_token()
            else:
                print("Line: " + str(self.lex.get_line()) +
                        "\nSyntax Error: Expected ')' after expression\n")
                sys.exit()
        elif self.token == "idtk":
            if self.function_open == 0:
                self.function_call = self.lex.get_id_value()
            self.token = self.lex.return_token()
            self.idtail()
            if self.function_open == 1:
                self.function_open = 0
        else:
            print("Line: " + str(self.lex.get_line()) +
                    "\nError factor can't be null\n")
            sys.exit()

    def idtail(self):
        if self.token == "left_round_brackettk":
            self.function_open = 1
            if not self.check_if_func_exits(self.function_call):
                print("Line: " + str(self.lex.get_line()) +
                            "\nFunction "+ str(self.function_call) +
                            " doesn't exists\n")
                sys.exit()
            self.token = self.lex.return_token()
            self.op.clear_values()
            self.pars_call.clear()
            self.actualpars()
            if not self.check_pars():
                print("Line: " + str(self.lex.get_line()) +
                            "\nNot valid arguments\n")
                sys.exit()
            self.semi_code.gen_quad("par", "_", self.semi_code.new_temp(), "RET")
            self.semi_code.next_quad()
            self.semi_code.gen_quad("call", self.function_call, "_", "_")
            self.semi_code.next_quad()
            self.op.set_last(self.semi_code.get_temp())
            self.op.clear_values()

    def relational_oper(self):
        if self.token == "equaltk":
            self.token = self.lex.return_token()
        elif self.token == "lessequaltk":
            self.token = self.lex.return_token()
        elif self.token == "greaterequaltk":
            self.token = self.lex.return_token()
        elif self.token == "lesstk":
            self.token = self.lex.return_token()
        elif self.token == "greatertk":
            self.token = self.lex.return_token()
        elif self.token == "notequaltk":
            self.token = self.lex.return_token()
        else:
            print("Line: " + str(self.lex.get_line()) +
                    "\nSyntax Error: Expected relational oper\n")
            sys.exit()

    def add_oper(self):
        if self.token == "plustk":
            self.op.add(self.lex.get_id_value())
            self.token = self.lex.return_token()
        elif self.token == "minustk":
            self.op.add(self.lex.get_id_value())
            self.token = self.lex.return_token()

    def check_if_func_exits(self, name):
        for function in self.symbol_table_list:
            if function.get_function_name() == name:
                return True
        return False

    def check_pars(self):
        for function in self.symbol_table_list:
            if function.get_function_name() == self.function_call:
                if function.get_pars_type_as_list() == self.pars_call:
                    return True
        return False
