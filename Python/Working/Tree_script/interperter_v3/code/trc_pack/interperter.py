class Stack():
    def __init__(self, size=100):
        self.stack_list = [None]*size
        self.num_items = 0
    
    def __str__(self):
        return f"{self.num_items} - {self.stack_list}"
    
    def push(self, item):
        self.stack_list[self.num_items] = item
        self.num_items += 1

    def pop(self):
        if self.num_items > 0:
            self.num_items -= 1
            output = self.stack_list[self.num_items]
            self.stack_list[self.num_items] = None
            return output
        else:
            return None

    def size(self):
        return self.num_items

def check_in_table(variable_table, possible_variable):
    output = None
    if variable_table.get(possible_variable) != None:
        # the table contains a variable with the name.
        output = variable_table.get(possible_variable)
    else:
        try:
            # is this variable just a plain number?
            output = int(possible_variable)
        except:
            # just treat it as a string
            output = possible_variable
    return output

def interpert(token_list):
    var_table = {"ANS": 0, "SIZE": 0}
    program_stack = Stack()
    line_pointer = 0
    while len(token_list) > line_pointer:
        line = token_list[line_pointer]
        token_pointer = 0
        for token in line:
            match token[0]:
                case "COMMAND":
                    # a zero parameter command
                    if token[1] in ["POP"]:
                        match token[1]:
                            case "POP": 
                                var_table["ANS"] = program_stack.pop()
                                var_table["SIZE"] = program_stack.size()
                    # one parameter command
                    elif token[1] in ["PRINT", "INPUT", "JUMP", "PUSH", "LIST", "LEN"]:
                        try:
                            parameter = line[token_pointer+1][1]
                        except:
                            raise ValueError(f"\nTRS: The command {token[1]} on line {line_pointer+1} needs a parameter")
                        match token[1]:
                            case "PRINT":
                                print(check_in_table(var_table, parameter))
                            case "INPUT":
                                var_name = parameter
                                var_value = input("?")
                                if var_value.isnumeric():
                                    var_value = int(var_value)
                                var_table[var_name] = var_value
                            case "JUMP":
                                # it needs to be -2 because of both zero indexing, and an off by one error
                                line_pointer = int(parameter)-2
                            case "PUSH":
                                program_stack.push(check_in_table(var_table, parameter))
                                var_table["SIZE"] = program_stack.size()
                            case "LIST":
                                var_table[parameter] = []
                            case "LEN":
                                possible_list = var_table.get(parameter)
                                if type(possible_list) == list:
                                    var_table["ANS"] = len(possible_list)
                                else:
                                    raise ValueError("\nTRS: The attempted list accessed on line {line_pointer+1}, under name {token[2]} is not a list.")
                    # commands with two parameters
                    elif token[1] in ["ADD", "SUB", "MUL", "DIV", "POW", "VAR", "JNZ", "READ"]:
                        try:
                            first_parameter = line[token_pointer+1][1]
                            second_parameter = line[token_pointer+2][1]
                        except:
                            raise ValueError(f"\nTRS: The command {token[1]} on line {line_pointer+1} needs a parameter")
                        match token[1]:
                            case "ADD" | "SUB" | "MUL" | "DIV" | "POW":
                                a = check_in_table(var_table, first_parameter)
                                b = check_in_table(var_table, second_parameter)
                                if type(a) == int and type(b) == int:
                                    if   token[1] == "ADD": var_table["ANS"] = a + b
                                    elif token[1] == "SUB": var_table["ANS"] = a - b
                                    elif token[1] == "MUL": var_table["ANS"] = a * b
                                    elif token[1] == "DIV": var_table["ANS"] = a / b
                                    elif token[1] == "POW": var_table["ANS"] = a ** b
                                else:
                                    raise ValueError(f"\nTRS: The command {token[1]} on line {line_pointer+1} has an incorrect parameter")
                            case "JNZ":
                                if check_in_table(var_table, first_parameter) != 0:
                                    line_pointer = int(line[token_pointer+2][1])-2
                            case "VAR":
                                var_table[first_parameter] = check_in_table(var_table, second_parameter)
                            case "READ":
                                list_name = first_parameter
                                list_index = second_parameter
                                try:
                                    var_table["ANS"] = var_table.get(list_name)[int(list_index)]
                                except:
                                    raise ValueError(f"\nTRS: The list read on line {line_pointer+1} is invalid.")
                    # commands with three parameters (wow, so sophisticated)
                    elif token[1] in ["WRITE"]:
                        try:
                            first_parameter = line[token_pointer+1][1]
                            second_parameter = line[token_pointer+2][1]
                            third_parameter = line[token_pointer+3][1]
                        except:
                            raise ValueError(f"\nTRS: The command {token[1]} on line {line_pointer+1} needs a parameter")
                        match token[1]:
                            case "WRITE":
                                list_name = first_parameter
                                list_index = check_in_table(var_table, second_parameter)
                                new_value = check_in_table(var_table, third_parameter)
                                try:
                                    _list = var_table.get(list_name)
                                    if len(_list) > list_index:
                                        _list[list_index] = new_value
                                    else:
                                        _list.append([None]*(len(_list)-list_index))
                                        _list[list_index] = new_value
                                except:
                                    raise ValueError(f"\nTRS: The command {token[1]} on line {line_pointer+1} ran into an error")
                    # can have one or two parameters (great langugage design btw)
                    elif token[1] in ["UPDATE"]:
                        if len(line) == 2:
                            try:
                                parameter = line[token_pointer+1][1]
                            except:
                                raise ValueError(f"\nTRS: The command {token[1]} on line {line_pointer+1} needs a parameter")
                            var_table[parameter] = var_table.get("ANS")
                        elif len(line) == 3:
                            try:
                                first_parameter = line[token_pointer+1][1]
                                second_parameter = line[token_pointer+2][1]
                            except:
                                raise ValueError(f"\nTRS: The command {token[1]} on line {line_pointer+1} needs a parameter")
                            var_table[first_parameter] = var_table.get(second_parameter)
            token_pointer += 1
        line_pointer += 1
