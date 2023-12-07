class variable():
    def __init__(self, name, value, index):
        self.name = name
        self.value = value
        self.index = index

current_var_index = 0

def format_var_list(var_list):
    output_list = []
    for var in var_list:
        output_list.append((var.name, var.value, var.index))
    return output_list

def return_var_value(formatted_list, possible_var):
    global current_var_index
    for i in range(0,len(formatted_list)):
        current_var = formatted_list[i]
        if possible_var == current_var[0]:
            current_var_index = current_var[2]
            return current_var[1]
    return possible_var

def return_var(formatted_list, var_name):
    for var in formatted_list:
        output_var = variable(var[0], var[1], var[2])
        if var_name == output_var.name:
            return output_var

def interpert(token_list):
    var_list = [variable("ANS", 0, 0)]
    line_pointer = 0
    while len(token_list) > line_pointer:
        line = token_list[line_pointer]
        token_pointer = 0
        for token in line:
            match token[0]:
                case "COMMAND":
                    found_list = format_var_list(var_list)
                    match token[1]:
                        case "PRINT":
                            var_to_check = line[token_pointer+1][1]
                            print(return_var_value(found_list, var_to_check))
                        case "INPUT":
                            var_value = input("?")
                            var_name = line[token_pointer+1][1]
                            input_var = return_var(found_list, var_name)
                            var_list[input_var.index] = variable(input_var.name, var_value, input_var.index)
                        # math - woooo
                        case "ADD":
                            item1 = line[token_pointer+1]
                            item2 = line[token_pointer+2]
                            checked_item1 = return_var_value(found_list, item1[1])
                            checked_item2 = return_var_value(found_list, item2[1])
                            var_list[0].value = int(checked_item1)+int(checked_item2)
                        case "SUB":
                            item1 = line[token_pointer+1]
                            item2 = line[token_pointer+2]
                            checked_item1 = return_var_value(found_list, item1[1])
                            checked_item2 = return_var_value(found_list, item2[1])
                            var_list[0].value = int(checked_item1)-int(checked_item2)
                        case "MUL":
                            item1 = line[token_pointer+1]
                            item2 = line[token_pointer+2]
                            checked_item1 = return_var_value(found_list, item1[1])
                            checked_item2 = return_var_value(found_list, item2[1])
                            var_list[0].value = int(checked_item1)*int(checked_item2)
                        case "DIV":
                            item1 = line[token_pointer+1]
                            item2 = line[token_pointer+2]
                            checked_item1 = return_var_value(found_list, item1[1])
                            checked_item2 = return_var_value(found_list, item2[1])
                            var_list[0].value = int(checked_item1)/int(checked_item2)
                        case "POW":
                            item1 = line[token_pointer+1]
                            item2 = line[token_pointer+2]
                            checked_item1 = return_var_value(found_list, item1[1])
                            checked_item2 = return_var_value(found_list, item2[1])
                            var_list[0].value = int(checked_item1)**int(checked_item2)
                        case "VAR":
                            name = line[token_pointer+1][1]
                            value = line[token_pointer+2][1]
                            index = len(var_list)
                            line[token_pointer+1] = ("VAR", line[token_pointer+1][1])
                            var_list.append(variable(name, value, index))
                        case "UPDATE":
                            var_to_update_name = line[token_pointer+1][1]
                            var_to_update = return_var(found_list, var_to_update_name)
                            if len(line) == 2:
                                var_to_update.value = var_list[0].value
                            elif len(line) == 3:
                                new_var_value_name = line[token_pointer+2][1]
                                new_var_value = return_var(found_list, new_var_value_name)
                                var_to_update.value = new_var_value.value
                            var_list[var_to_update.index] = var_to_update
                        case "JUMP":
                            line_pointer = int(line[token_pointer+1][1])-2
                        case "JNZ":
                            condition = line[token_pointer+1]
                            checked_condition = return_var_value(found_list, condition[1])
                            if checked_condition != 0:
                                line_pointer = int(line[token_pointer+2][1])-2
            token_pointer += 1
        line_pointer += 1