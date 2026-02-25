import sys

from trc_pack import parser
from trc_pack import interperter

class variable():
    def __init__(self, name, value, index):
        self.name = name
        self.value = value
        self.index = index

def parse_text(user_input):
    return parser.return_tokens(parser.format_text(user_input))

def run_trs():
    print("Tree Script")
    file = open(current_file)
    user_input = file.read()
    parsed_tokens = parse_text(user_input)
    interperter.interpert(parsed_tokens)
    file.close()

if len(sys.argv) > 1:
  current_file = sys.argv[1]
  run_trs()
else:
  print("please enter the name of a file")
