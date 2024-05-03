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

zone_array = []

def get_zone(x,y):
    return zone_array[y][x]

def give_scene(zone):
    zone.print_desc()

def make_map(map_size):
    for i in range(map_size[0]):
        zone_row = []
        for j in range(map_size[1]):
            zone_row.append(zone(j, i, [], f"You are currently at {j, i}"))
        zone_array.append(zone_row)