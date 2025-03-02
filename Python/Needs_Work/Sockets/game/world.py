class World:
    def __init__(self):
        self.new_grid()

    def new_grid(self):
        world_grid = []
        for i in range(5):
            row = []
            for j in range(5):
                row.append(' ')
            world_grid.append(row)
        self.grid = world_grid

    def print_grid(self):
        for i in range(len(self.grid)):
            print(self.grid[i])

    def set_position(self, x, y, value):
        self.grid[y][x] = value

    def get_position(self, x, y):
        return self.grid[y][x]
    
    def place_object(self, obj):
        self.set_position(obj.x, obj.y, obj.char)
        

class Entity:
    def __init__(self, char, position):
        self.char = char
        self.x = position[0]
        self.y = position[1]

    def update_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return (self.x, self.y)

def move_entity(world, entity, destination):
    world.set_position(entity.x, entity.y, ' ')
    entity.x = destination[0]
    entity.y = destination[1]
    world.place_object(entity)

my_world = World()
dude = Entity("#", (2,2))
my_world.place_object(dude)
my_world.print_grid()
print()
move_entity(my_world, dude, (3,2))
my_world.print_grid()