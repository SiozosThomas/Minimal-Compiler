import sys

class lex():

    def __init__(self):
        self.lines = 0
        self.columns = 0
        self.id = ""
        self.id_value = ""
        self.digit = ""
        self.file_lines = []
        self.num_of_lines = 0
        self.id_limit = 0

    def set_file_lines(self, filename):
        try:
            file = open(filename, "r")
        except FileNotFoundError:
            print("File doesn't exist...\n")
            sys.exit()
        self.file_lines = file.readlines()
        self.set_num_of_lines()

    def set_num_of_lines(self):
        self.num_of_lines=len(self.file_lines)

    def get_line(self):
        return self.lines + 1

    def get_id_value(self):
        return self.id_value

    def return_token(self):
        while self.check_line_limit():
            while self.check_column_limit():
                if self.is_letter():
                    self.id += self.file_lines[self.lines][self.columns]
                    self.id_limit += 1
                    self.columns += 1
                    self.find_id()
                    self.id_limit = 0
                    return self.check_commited_word()
                if self.is_digit():
                    self.digit += self.file_lines[self.lines][self.columns]
                    self.columns += 1
                    return self.find_digit()
                punctuation = self.is_punctuation()
                if punctuation != "not_punctuation" and\
                    punctuation != "line_comment" and\
                    punctuation != "block_comment":
                    self.columns += 1
                    return punctuation
                # elif ord(self.file_lines[self.lines][self.columns]) == 10: #/n
                #     break
                self.columns += 1
            self.lines += 1
            self.columns = 0

    def check_line_limit(self):
        if self.lines < self.num_of_lines:
            return True
        return False

    def check_column_limit(self):
        if self.columns < len(self.file_lines[self.lines]):
            return True
        return False

    def find_id(self):
        while self.check_column_limit():  #orio stiles
            if self.is_letter():
                self.id += self.file_lines[self.lines][self.columns]
                self.id_limit += 1
                self.check_id_limit()
                self.columns+=1
            elif self.is_digit():
                self.id += self.file_lines[self.lines][self.columns]
                self.id_limit += 1
                self.check_id_limit()
                self.columns+=1
            else:
                break

    def check_id_limit(self):
        if self.id_limit > 30:
            print("Line: " + str(self.lines) + ", id's length can't be more" +
                    " than 30\n")
            sys.exit()

    def find_digit(self):
        while self.check_column_limit():
            if self.is_digit():
                self.digit += self.file_lines[self.lines][self.columns]
            else:
                self.id_value = self.digit
                break
            if not self.check_digit_limit():
                print("Not valid number\n")
                sys.exit()
            self.columns+=1
        self.digit = ""
        return "constanttk"

    def check_digit_limit(self):
        if int(self.digit) < 32767 and int(self.digit) > -32767:
            return True
        return False

    def is_letter(self):
        if self.file_lines[self.lines][self.columns].isalpha():
            return True
        return False

    def is_digit(self):
        if ord(self.file_lines[self.lines][self.columns]) >= 48 and\
            ord(self.file_lines[self.lines][self.columns]) <= 57:
            return True
        return False

    def check_commited_word(self):
        self.id_value = self.id
        if self.id == "program":
            self.id = ""
            return "programtk"
        elif self.id == "declare":
            self.id = ""
            return "declaretk"
        elif self.id == "if":
            self.id = ""
            return "iftk"
        elif self.id == "else":
            self.id = ""
            return "elsetk"
        elif self.id == "then":
            self.id = ""
            return "thentk"
        elif self.id == "while":
            self.id=""
            return "whiletk"
        elif self.id == "forcase":
            self.id = ""
            return "forcasetk"
        elif self.id == "not":
            self.id = ""
            return "nottk"
        elif self.id == "function":
            self.id = ""
            return "functiontk"
        elif self.id == "input":
            self.id = ""
            return "inputtk"
        elif self.id == "doublewhile":
            self.id = ""
            return "doublewhiletk"
        elif self.id == "incase":
            self.id = ""
            return "incasetk"
        elif self.id ==  "and":
            self.id = ""
            return "andtk"
        elif self.id == "procedure":
            self.id = ""
            return "proceduretk"
        elif self.id == "print":
            self.id = ""
            return "printtk"
        elif self.id == "loop":
            self.id = ""
            return "looptk"
        elif self.id == "when":
            self.id = ""
            return "whentk"
        elif self.id == "or":
            self.id = ""
            return "ortk"
        elif self.id == "exit":
            self.id = ""
            return "exittk"
        elif self.id == "default":
            self.id = ""
            return "defaulttk"
        elif self.id == "return":
            self.id = ""
            return "returntk"
        elif self.id == "in":
            self.id = ""
            return "intk"
        elif self.id == "inout":
            self.id = ""
            return "inouttk"
        elif self.id == "call":
            self.id = ""
            return "calltk"
        self.id = ""
        return "idtk"

    def is_punctuation(self):
        if ord(self.file_lines[self.lines][self.columns]) == 43:
            self.id_value = "+"
            return "plustk"
        elif ord(self.file_lines[self.lines][self.columns]) == 45:
            self.id_value = "-"
            return "minustk"
        elif ord(self.file_lines[self.lines][self.columns]) == 42:
            self.id_value = "*"
            return "multiplytk"
        elif ord(self.file_lines[self.lines][self.columns]) == 47:
            if self.check_line_comment():
                print("Line comment\n")
                return "line_comment"
            if self.check_block_comment():
                print("Block comment\n")
                return "block_comment"
            self.id_value = "/"
            return "dividetk"
        elif ord(self.file_lines[self.lines][self.columns]) == 60:
            if self.check_greater_or_less_equal():
                self.id_value = "<="
                return "lessequaltk"
            if self.check_nottk():
                return "not"
                return "nottk"
            self.id_value = "<"
            return "lesstk"
        elif ord(self.file_lines[self.lines][self.columns]) == 62:
            if self.check_greater_or_less_equal():
                self.id_value = ">="
                return "greaterequaltk"
            return "greatertk"
        elif ord(self.file_lines[self.lines][self.columns]) == 61:
            self.id_value = "="
            return "equaltk"
        elif ord(self.file_lines[self.lines][self.columns]) == 59:
            self.id_value = ";"
            return "questiontk"
        elif ord(self.file_lines[self.lines][self.columns]) == 44:
            self.id_value = ","
            return "commatk"
        elif ord(self.file_lines[self.lines][self.columns]) == 58:
            if self.check_assigmenttk():
                self.id_value = ":="
                return "assignmenttk"
            self.id_value = ":"
            return "colontk"
        elif ord(self.file_lines[self.lines][self.columns]) == 40:
            self.id_value = "("
            return "left_round_brackettk"
        elif ord(self.file_lines[self.lines][self.columns]) == 41:
            self.id_value = ")"
            return "right_round_brackettk"
        elif ord(self.file_lines[self.lines][self.columns]) == 91:
            self.id_value = "["
            return "left_square_brackettk"
        elif ord(self.file_lines[self.lines][self.columns]) == 93:
            self.id_value = "]"
            return "right_square_brackettk"
        elif ord(self.file_lines[self.lines][self.columns]) == 123:
            self.id_value = "{"
            return "left_curly_brackettk"
        elif ord(self.file_lines[self.lines][self.columns]) == 125:
            self.id_value = "}"
            return "right_curly_brackettk"
        return "not_punctuation"

    def check_assigmenttk(self):
        self.columns += 1
        if self.check_column_limit():
            if ord(self.file_lines[self.lines][self.columns]) == 61:
                return True
        self.columns -= 1
        return False

    def check_greater_or_less_equal(self):
        self.columns += 1
        if self.check_column_limit():
            if ord(self.file_lines[self.lines][self.columns]) == 61:
                return True
        self.columns -= 1
        return False

    def check_nottk(self):
        self.columns += 1
        if self.check_column_limit():
            if ord(self.file_lines[self.lines][self.columns]) == 62:
                return True
        self.columns -= 1
        return False

    def check_line_comment(self):
        self.columns += 1
        if self.check_column_limit():
            if ord(self.file_lines[self.lines][self.columns]) == 47:
                while self.check_column_limit():
                    self.columns += 1
                return True
        self.columns -= 1
        return False

    def check_block_comment(self):
        self.columns += 1
        if self.check_column_limit():
            if ord(self.file_lines[self.lines][self.columns]) == 42:
                while self.check_line_limit():
                    self.columns += 1
                    while self.check_column_limit():
                        if ord(self.file_lines[self.lines][self.columns]) == 42:
                            self.columns += 1
                            if self.check_column_limit():
                                if ord(self.file_lines[self.lines]\
                                            [self.columns]) == 47:
                                    return True
                                else:
                                    self.columns -= 1
                        self.columns += 1
                    self.columns = -1
                    self.lines += 1
        return False
