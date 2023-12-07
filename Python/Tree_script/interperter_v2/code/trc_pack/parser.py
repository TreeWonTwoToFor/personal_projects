command_list = ["PRINT", "ADD", "SUB", "MUL", "DIV", "POW", "VAR", "UPDATE", "JUMP", "JNZ", "INPUT"]

def format_text(user_input):
    parser_array_output = []
    parser_output = user_input.split("\n")
    for line in parser_output:
        quote_marker_list = []
        quote_output = ""
        line_array = line.split()
        for i in range(0, len(line_array)):
            if '"' in line_array[i]:
                quote_marker_list.append(i)
        for i in range(0, len(line_array)):
            if i in quote_marker_list:
                if len(quote_output) == 0:
                    quote_output += line_array[i]
                else:
                    quote_output += " " + line_array[i]
        if len(quote_output) > 0:
            quote_marker_list = quote_marker_list[::-1]
            for index in quote_marker_list:
                line_array.pop(index)
            line_array.append(quote_output)
        parser_array_output.append(line_array)
    return parser_array_output

def return_tokens(user_input):
    output_list = []
    is_var = False
    for line in user_input:
        line_output = []
        for token in line:
            if token == "ANS":
                is_var = True
                line_output.append(("VAR", token))
            if token in command_list:
                line_output.append(("COMMAND", token))
            elif token.isnumeric():
                line_output.append(("NUM", token))
            elif not is_var:
                line_output.append(("TXT", token))
        output_list.append(line_output)
    return output_list