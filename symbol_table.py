import sys

class symbol_table():

    def __init__(self, nesting_level):
        self.nesting_level = nesting_level
        self.offset = 12
        self.entities = []
        self.pars_type = []
        self.variables = []
        self.functions = []
        self.parent = ""
        self.var_w_offset = {}

    def add_var_w_offset(self, key, value):
        self.var_w_offset[key] = value

    def get_var_w_offset(self):
        return self.var_w_offset

    def get_x_in_var_w_offset(self, x):
        return self.var_w_offset.get(str(x))

    def get_nesting_level(self):
        return self.nesting_level

    def set_parent(self, x):
        self.parent = x

    def get_parent(self):
        return self.parent

    def get_offset(self):
        return self.offset

    def increase_offset(self):
        self.offset += 4

    def set_frame_length(self):
        self.frame_length = self.offset

    def add_variable(self, x):
        self.variables.append(x)

    def get_variables(self):
        return self.variables

    def add_function(self, x):
        self.functions.append(x)

    def get_functions(self):
        return self.functions

    def set_function_name(self, name):
        self.function_name = name

    def get_function_name(self):
        return self.function_name

    def add_par_type(self, x):
        self.pars_type.append(x)

    def get_pars_type_as_list(self):
        return self.pars_type

    def get_pars_type(self):
        pars_string = ""
        count = 0
        for pars in self.pars_type:
            if count == 0:
                pars_string += str(pars)
            else:
                pars_string += ", " + str(pars)
            count += 1
        return pars_string

    def get_function_as_entity(self):
        return self.function_name + ", "  + self.get_pars_type() + ", "\
                        + str(self.frame_length)

    def set_entity(self, x):
        self.add_var_w_offset(str(self.get_offset), x)
        entity = str(x) + " : " + str(self.get_offset())
        self.increase_offset()
        self.entities.append(entity)

    def set_entity_function(self, x):
        entity = str(x)
        self.entities.append(entity)

    def print_function(self):
        count = 0
        entities = ""
        for entity in self.entities:
            if count == 0:
                entities += str(entity)
            else:
                entities += str(", ") + str(entity)
            count += 1
        print("\n----" + str(self.function_name) + "----\n")
        print("Father: " + str(self.parent))
        print("Level: " + str(self.nesting_level))
        print(entities)
