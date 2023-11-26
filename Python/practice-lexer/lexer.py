# list of things to do
#   list of things that you are able to actually type into the terminal
#       numbers, +-()*/
#   functions that
#       hold the character
#       identify the character
#       tokeninze the character
#       advance to the next character
#   

# Constants #
digits = "123456789"

# Errors #

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result
    
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character", details)


# Position #

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
    
    def advance(self, curent_char):
        self.idx += 1
        self.col += 1

        if curent_char == "\n":
            self.ln += 1
            self.col = 0
        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

# Tokens #

TT_INT      = "INT"
TT_FLOAT    = "FLOAT"
TT_PLUS     = "PLUS"
TT_MINUS    = "MINUS"
TT_MUL      = "MUL"
TT_DIV      = "DIV"
TT_LPAREN   = "LPAREN"
TT_RPAREN   = "RPAREN"

class Token():
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}: {self.value}'
        return f'{self.type}'

# Lexer #

# Run #