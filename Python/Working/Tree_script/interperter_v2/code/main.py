from trc_pack import parser
from trc_pack import interperter
import os

class variable():
    def __init__(self, name, value, index):
        self.name = name
        self.value = value
        self.index = index

def parse_text(user_input):
    return parser.return_tokens(parser.format_text(user_input))

current_file = "file.trs"

def run_trs():
    os.system('cls')
    print("Tree Script")
    file = open(current_file)
    user_input = file.read()
    parsed_tokens = parse_text(user_input)
    interperter.interpert(parsed_tokens)
    file.close()

run_trs()