class CPU:
    def __init__(self):
        self.running = True
        self.program_counter = 0
        self.instruction_register = ""
        self.accumulator = 0
        self.state = "fetch"

    def tick(self):
        match self.state:
            case "fetch":
                self.fetch()
            case "execute":
                print("something")

    def fetch(self, command_input):
        command_list = self.instruction_register.split()
        command = command_list[0]
        if len(command_list) == 2:
            command_value = command_input[1]
        match command:
            case "LOAD":
                self.accumulator = command_value
            case "ADD":
                self.accumulator += command_value
            case "SUB":
                self.accumulator = self.accumulator - command_value
            case "MUL":
                self.accumulator = self.accumulator * command_value
            case "DIV":
                # divides to an integer value using floor based division
                self.accumulator = self.accumulator // command_value
            case "STR":
                # put the accumulator value into RAM at address command_value
                print("STR command call")
            case "JMP":
                self.program_counter = command_value
            case "OUT":
                # doesnt involve a command value at all
                print(self.accumulator)
            case "IN":
                # places the value into the accumulator (or into a RAM address if specified)
                # FORMAT: IN value address
                if len(command_list) == 1:
                    self.accumulator = input('>')
                elif len(command_list) == 2:
                    # set the RAM at the specific address to the input
                    address = input('>')
            case "HALT":
                self.running = False