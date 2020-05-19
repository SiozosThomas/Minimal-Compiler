import sys

class semi_code_output_file():

    def __init__(self):
        self.writer = open("semi_code.int", "w")

    def write_to_file(self, line):
        self.writer.write(str(line))

    def close_writer(self):
        self.writer.close()

class semi_code_c_file():

    def __init__(self):
        self.variables = []
        self.writer = open("semi_code.c", "w")

    def write_main(self):
        self.writer.write("int main()\n{\n")

    def close_main(self):
        self.writer.write("}\n")

    def add_variable(self, x):
        self.variables.append(x)

    def write_variables(self):
        self.writer.write("\tint ")
        if (len(self.variables) >= 1):
            self.writer.write(str(self.variables[0]))
            for i in range(1, len(self.variables)):
                self.writer.write(", " + str(self.variables[i]))
        self.writer.write(";\n\tL_1:\n")

    def fill_c_file(self, all_quads):
        self.write_main()
        self.write_variables()
        counter = 2
        for i in range(0, len(all_quads)):
            if all_quads[i][0] == ">" or all_quads[i][0] == ">="\
                    or all_quads[i][0] == "<" or all_quads[i][0] == "<="\
                    or all_quads[i][0] == "=" or all_quads[i][0] == "<>":
                self.writer.write("\tL_" + str(counter) + ": " +\
                            str(all_quads[i][1]) + str(all_quads[i][0]) +\
                            str(all_quads[i][2]) +\
                            " goto L_" + str(all_quads[i][3]) + ";\n")
                counter += 1
            if all_quads[i][0] == ":=":
                self.writer.write("\tL_" + str(counter) + ": " +\
                    str(all_quads[i][3]) + str(all_quads[i][0]) +\
                    str(all_quads[i][1]) + ";\n")
                counter += 1
            if all_quads[i][0] == "jump":
                self.writer.write("\tL_" + str(counter) + ": goto L_" +\
                    str(all_quads[i][3]) + ";\n")
            if all_quads[i][0] == "+" or all_quads[i][0] == "-"\
                    or all_quads[i][0] == "*" or all_quads[i][0] == "/":
                self.writer.write("\tL_" + str(counter) + ": " +\
                            str(all_quads[i][3]) + " = "  + str(all_quads[i][1])\
                            + str(all_quads[i][0]) + str(all_quads[i][2]) + ";\n")
                counter += 1
            if all_quads[i][0] == "out":
                self.writer.write("\tL_" + str(counter) + ": print(" +\
                    str(all_quads[i][1]) + ");\n")
                counter += 1
        self.writer.write("\tL_" + str(counter) +":" +" " + "{}\n")
        self.close_main()
        self.close_writer()

    def write_to_file(self, line):
        self.writer.write(str(line))

    def close_writer(self):
        self.writer.close()
