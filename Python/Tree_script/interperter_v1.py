import os

class VAR:
    def __init__(self, name, value, index):
        self.name = name
        self.value = value
        self.index = index
    
    def return_var(self):
        print(self.name, self.value, self.index)

var_array = []
line_array = []
line_index = 0
dev = False
var_flag = False
var_index = 1

def check_if_var(usr_array, i):
    global var_flag, var_index
    var_flag = False
    output = usr_array[i+1] # value of the number/text
    for var in var_array:
        if var.name == usr_array[i+1]:
            var_flag = True
            var_index = var.index
            output = var.value # value of the variable
        if len(usr_array) == 4:
            if var.name == usr_array[i+2]:
                output = var.value
    return output

def make_var(usr_array, i):
    for var in var_array:
        if var.name == usr_array[i+2]:
            var_array.append(VAR(usr_array[i+1], var_array[i+2].value, len(var_array)))
            return 0
    var_array.append(VAR(usr_array[i+1], usr_array[i+2], len(var_array)))
    return 1

def remove_dupe_vars(show_dupe):
    for var1 in var_array:
        for var2 in var_array:
            if var1.index != var2.index:
                if var1.name == var2.name:
                    if show_dupe:
                        print(var_array)
                        print(var1.name, var1.value, var1.index)
                        print(var2.name, var2.value, var2.index)
                    var1.value = var2.value
                    var_array.pop(var2.index)

def var_array_report(lined):
    for var in var_array:
        print(var.name, var.value)
    if lined:
        print("------")

def update_ans_var(value):
    var_array[0] = VAR("ANS", value, 0)

def get_text(usr_array):
    global dev, line_index
    command = "unknown"
    command_array = []
    for i in range(0, len(usr_array)):
        current_item = usr_array[i]
        match current_item:
            case "PRINT":
                command = current_item
                print(check_if_var(usr_array, i))
            case "ADD":
                command = current_item
                value_1 = check_if_var(usr_array, i)
                value_2 = check_if_var(usr_array, i+1)
                func_out = int(value_1)+int(value_2)
                update_ans_var(func_out)
            case "SUB":
                command = current_item
                value_1 = check_if_var(usr_array, i)
                value_2 = check_if_var(usr_array, i+1)
                func_out = int(value_1)-int(value_2)
                update_ans_var(func_out)
            case "MULT":
                command = current_item
                value_1 = check_if_var(usr_array, i)
                value_2 = check_if_var(usr_array, i+1)
                func_out = int(value_1)*int(value_2)
                update_ans_var(func_out)
            case "DIV":
                command = current_item
                value_1 = check_if_var(usr_array, i)
                value_2 = check_if_var(usr_array, i+1)
                func_out = int(value_1)/int(value_2)
                update_ans_var(func_out)
            case "VAR":
                command = current_item
                make_var(usr_array, i)
            case "UPDATE":
                command = current_item
                check_if_var(usr_array, i)
                var_to_update = var_array[var_index]
                if var_flag and len(usr_array) == 2:
                    var_array[var_index].value = var_array[0].value
                if var_flag and len(usr_array) == 3:
                    update_value = check_if_var(usr_array, i+1)
                    var_to_update.value = update_value
            case "JUMP":
                command = current_item
                line_index = int(check_if_var(usr_array, i))-2
            case "CONDJUMP":
                command = current_item
                if int(check_if_var(usr_array, i)): # jumps if a + value
                    line_index = int(check_if_var(usr_array, i+1))-2
            case "INPUT":
                command = current_item
                usr_input = input()
                for var in var_array:
                    if var.name == usr_array[i+1]:
                        var.value = int(usr_input)
            case default:
                item_type = ""
                if current_item.isnumeric():
                    item_type = "NUM"
                if item_type == "":
                    item_type = "TEXT"
                command = f"{item_type}: {current_item}"
        command_array.append(command)
    return command_array

def main():
    global line_index
    os.system('cls')
    var_array.append(VAR("ANS", 0, 0))
    if input_type == "console":
        running = True
        while running:
            global dev
            text = input("Tree Script>")
            main_output = get_text(text.split())
            if dev:
                print(main_output)
            if main_output[0] == "TEXT: EXIT":
                running = False
            if main_output[0] == "TEXT: DEV":
                dev = True
            if main_output[0] == "TEXT: CLS":
                os.system('cls')
        os.system('cls')
    if input_type == "file":
        file_path = input("File path>")
        file = open(file_path,'r')
        content = file.read()
        line_array = content.split("\n")
        count = 0
        while (len(line_array) > line_index) and (count < 1000):
            alt_output = get_text((line_array[line_index]).split())
            remove_dupe_vars(False)
            line_index += 1
            count += 1
        file.close()

input_type = "file"
main()