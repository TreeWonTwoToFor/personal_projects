class zone:
    def __init__(self, x, y, object_list, description):
        self.x = x
        self.y = y
        self.object_list = object_list
        self.description = description

    def print_zone(self):
        line_len = ""
        for i in range(len(self.description)+13):
            line_len += "#"
        print(f"{line_len}\n(x, y): ({self.x, self.y})\nobject_list = {self.object_list}\ndescription: {self.description}\n{line_len}")

    def print_desc(self):
        print(self.description)