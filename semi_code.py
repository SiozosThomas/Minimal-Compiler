import sys

class semi_code():

    def __init__(self):
        self.all_quads = []
        self.quad = ["_" for i in range(0, 4)]
        self.label = 0
        self.temp = -1
        self.b_quad = 0
        self.function = None

    def get_all_quads(self):
        return self.all_quads

    def get_label(self):
        return self.label

    def get_b_quad(self):
        return self.b_quad;

    def next_quad(self):
        self.label += 1
        return self.label

    def gen_quad(self, op, x, y, z):
        self.quad[0], self.quad[1], self.quad[2], self.quad[3] = op, x, y, z
        self.all_quads.append(self.quad)
        self.empty_list()

    def new_temp(self):
        self.temp += 1
        self.function.add_variable("T_" + str(self.temp))
        self.function.set_entity("T_" + str(self.temp))
        return "T_" + str(self.temp)

    def get_temp(self):
        return "T_" + str(self.temp)

    def get_temp_var(self):
        return self.temp

    def empty_list(self):
        self.quad = ["_" for i in range(0, 4)]

    def set_b_quad(self, b_quad):
        self.b_quad = b_quad

    def back_path(self, z, jump_or_not):
        for i in range(self.b_quad, self.get_all_quad_size()):
            if (jump_or_not == "not_jump"):
                if (self.all_quads[i][1] != "_" and self.all_quads[i][2] != "_"):
                    if (self.all_quads[i][0] != "jump"):
                        if (self.all_quads[i][3] == "_"):
                            self.all_quads[i][3] = z
            elif (jump_or_not == "jump"):
                if (self.all_quads[i][0] == "jump" and self.all_quads[i][3] == "_"):
                    self.all_quads[i][3] = z

    def get_all_quad_size(self):
        return len(self.all_quads)

    def set_function(self, function):
        self.function = function

    def print_all_quads(self, writer):
        for i in range(0, self.get_all_quad_size()):
            writer.write_to_file(str(i+1) + " : ")
            for j in range(0, len(self.all_quads[i])):
                writer.write_to_file(str(self.all_quads[i][j]) + " ")
            writer.write_to_file('\n')
        writer.close_writer()
