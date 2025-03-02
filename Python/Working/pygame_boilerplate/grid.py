import pygame
import time

pygame.init()

# PLACE GRID COPNSTANTS HERE
tile_size = 40 # pixels
tile_outline = False # change if you want to draw outlines or not
tile_boundary_color = (255, 0, 0) 
tile_boundary_thickness = 2
grid_outline = True
grid_color = (0, 0, 0)
world_size = (10, 10)
visual_size = world_size #(5, 5)

# extra grid calculations
grid_boundaries = ((45, 45), (450, 315))
grid_visual_size = ((grid_boundaries[1][0]-grid_boundaries[0][0])/tile_size, (grid_boundaries[1][1]-grid_boundaries[0][1])/tile_size)

# pygame constants
screenX = 500
screenY = 500
bg_color = (255, 255, 255)
FPS = 60
clock = pygame.time.Clock()
pygame.display.set_caption("Grid example")
file_path = r"C:\Tree's Stuff\Programming\Python\Working\pygame_boilerplate\\"
font = pygame.font.Font(file_path + "Comfortaa.ttf", 30)
screen = pygame.display.set_mode((screenX, screenY))

class Grid:
    def __init__(self, width, height, x, y, array):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.array = array
        if self.array == []:
            for i in range(height):
                row = []
                for i in range(width):
                    row.append(' ')
                self.array.append(row)

    def grab_partial_array(self, x, y, width, height):
        out_array = []
        for i in range(y, y+height):
            out_array.append([])
            for j in range(x, x+width):
                out_array[i-y].append(' ')
            for j in range(x, x+width):
                out_array[i-y][j-x] = self.array[i][j]
        return out_array

    def draw_outline(self, tile_size, tile_color, tile_thickness, outline_color):
        left = self.x
        top = self.y
        grid_width = self.width * tile_size
        grid_height = self.height * tile_size
        if tile_outline:
            for i in range(self.height):
                for j in range(self.width):
                    pygame.draw.rect(screen, tile_color, pygame.Rect(left+j*tile_size, top+i*tile_size, tile_size, tile_size), tile_thickness//2)
        if grid_outline:
            pygame.draw.rect(screen, outline_color, pygame.Rect(left, top, grid_width, grid_height), tile_thickness)

    def draw_tiles(self, tile_thickness):
        for i in range(self.height):
            for j in range(self.width):
                tile_value = self.array[i][j]
                if type(tile_value) == str or type(tile_value) == chr:
                    tile_x = tile_size * j + self.x + tile_thickness + 7
                    tile_y = tile_size * i + self.y + tile_thickness
                    text = font.render(tile_value, True, (0,0,0), (255, 255, 255))
                    textRect = text.get_rect()
                    textRect.topleft = (tile_x, tile_y)
                    screen.blit(text, textRect)
                elif type(tile_value) == Entity:
                    tile_x = tile_size * j + self.x 
                    tile_y = tile_size * i + self.y
                    tile_value.display(self, tile_x, tile_y)

    def place_value(self, value, x, y):
        if (self.height > y and self.width > x):
            self.array[y][x] = value

    def get_tile(self, x, y, size):
        out_tile = self.array[y][x]
        x_pos = self.x + x*size
        y_pos = self.y + y*size
        return (out_tile, x_pos, y_pos)

class Entity:
    def __init__(self, name, width, height, image, grid):
        self.name = name
        self.width = width
        self.height = height
        self.image = image
        self.grid = grid
        self.position = (3,3)

    def display(self, grid, visual_x, visual_y):
        screen.blit(self.image, (visual_x, visual_y))

    def move(self, x, y):
        if x != 0:
            if self.position[0]+x >= 0 and self.position[0]+x < world_size[0]:
                self.move_helper(x, y)
        if y != 0:
            if self.position[1]-y >= 0 and self.position[1]-y < world_size[1]:
                self.move_helper(x, y)

    def move_helper(self, x, y):
        self.grid.place_value(" ", self.position[0], self.position[1])
        self.grid.place_value(self, self.position[0]+x, self.position[1]-y)
        self.position = (self.position[0]+x, self.position[1]-y)


world_grid = Grid(world_size[0], world_size[1], 0, 0, [])
dude = Entity("Dude", 1, 1, pygame.image.load(file_path + r"images\dude.png"), world_grid)
tree = Entity("tree", 1, 1, pygame.image.load(file_path + r"images\tree.png"), world_grid)
for i in range(world_size[0]):
    world_grid.place_value(tree, i, 0)
    world_grid.place_value(tree, i, world_size[1]-1)
for j in range(world_size[1]):
    world_grid.place_value(tree, 0, j)
    world_grid.place_value(tree, world_size[0]-1, j)
world_grid.place_value(dude, 3, 3)
current_position = [0, 0]

print(f"grid size: {grid_visual_size}")
running = True
while running:
    test_array = world_grid.grab_partial_array(current_position[0], current_position[1], visual_size[0], visual_size[1])
    visual_grid = Grid(visual_size[0], visual_size[1], tile_size//2, tile_size//2, test_array)
    screen.fill(bg_color)
    visual_grid.draw_tiles(tile_boundary_thickness)
    if (tile_outline or grid_outline):
        visual_grid.draw_outline(tile_size, tile_boundary_color, tile_boundary_thickness, grid_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print(mouse_pos)
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_UP: 
                    if current_position[1] > 0:
                        current_position[1] -= 1
                case pygame.K_DOWN: 
                    if current_position[1]+visual_size[1] < world_grid.height:
                        current_position[1] += 1
                case pygame.K_LEFT: 
                    if current_position[0] > 0:
                        current_position[0] -= 1
                case pygame.K_RIGHT: 
                    if current_position[0]+visual_size[0] < world_grid.width:
                        current_position[0] += 1
                case pygame.K_w: dude.move(0, 1)
                case pygame.K_s: dude.move(0, -1)
                case pygame.K_a: dude.move(-1, 0)
                case pygame.K_d: dude.move(1, 0)
    pygame.display.update()
    clock.tick(FPS)