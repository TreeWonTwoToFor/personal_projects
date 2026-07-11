import math
import pygame

application_name = "BattleMap"
application_icon = "./icons/compass_icon.png"

tile_size = (50, 50)
grid_size = ()

shape_option = "rectangle"
color_palette = "stone"
outline_width = 2

border = 25
start_location = (border,border)

def run(canvas_dict, desktop_instruction):
    canvas = canvas_dict[application_name].surface
    logic_output = logic(canvas.get_size(), desktop_instruction)
    draw(canvas, logic_output)

def draw(canvas, logic_output):
    canvas.fill(background_color)
    if grid_size[0] == 0 or grid_size[1] == 0:
        # we don't have the grid size, so don't draw anything
        return 
    match shape_option:
        case "rectangle": draw_rectanlge(canvas, logic_output)
        case "circle": draw_circle(canvas, logic_output)

def logic(canvas_size, desktop_instruction):
    global background_color, outline_color, tile_color, grid_size, color_palette, shape_option
    if desktop_instruction in ["Stone", "Paper"]:
        color_palette = desktop_instruction.lower()
    elif desktop_instruction in ["Rectangle", "Circle"]:
        shape_option = desktop_instruction.lower()
    match color_palette:
        case "paper":
            background_color = (255,255,255)
            outline_color = (0,0,0)
            tile_color = (240, 240, 200)
        case "stone":
            background_color = (50, 50, 50)
            outline_color = (0,0,0)
            tile_color = (100, 100, 100)
    grid_size = (canvas_size[0]-border)//tile_size[0], (canvas_size[1]-border)//tile_size[1]

def draw_rectanlge(canvas, logic_output):
    map_outline = pygame.rect.Rect(start_location[0]-outline_width, start_location[1]-outline_width,
                                    tile_size[0]*grid_size[0]+outline_width*2, tile_size[1]*grid_size[1]+outline_width*2)
    pygame.draw.rect(canvas, outline_color, map_outline)
    draw_location = [start_location[0], start_location[1]]
    for col in range(grid_size[0]):
        for square in range(grid_size[1]):
            tile_outline = pygame.rect.Rect(*draw_location, *tile_size)
            tile = pygame.rect.Rect(draw_location[0]+outline_width, draw_location[1]+outline_width, 
                                    tile_size[0]-outline_width*2, tile_size[1]-outline_width*2)
            pygame.draw.rect(canvas, outline_color, tile_outline)
            pygame.draw.rect(canvas, tile_color, tile)
            draw_location[1] += tile_size[1]
        draw_location[0] += tile_size[0]
        draw_location[1] -= tile_size[1] * grid_size[1]

def draw_circle(canvas, logic_output):
    def distance_function(xy1, xy2):
        x1, y1 = xy1
        x2, y2 = xy2
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)
    circle_radius = min(grid_size[0]+1, grid_size[1]+1)//2
    draw_location = [start_location[0], start_location[1]]
    for col in range(grid_size[0]):
        for square in range(grid_size[1]):
            if distance_function((col, square), (grid_size[0]//2, grid_size[1]//2)) < circle_radius:
                tile_outline = pygame.rect.Rect(*draw_location, *tile_size)
                tile = pygame.rect.Rect(draw_location[0]+outline_width, draw_location[1]+outline_width, 
                                        tile_size[0]-outline_width*2, tile_size[1]-outline_width*2)
                pygame.draw.rect(canvas, outline_color, tile_outline)
                pygame.draw.rect(canvas, tile_color, tile)
            draw_location[1] += tile_size[1]
        draw_location[0] += tile_size[0]
        draw_location[1] -= tile_size[1] * grid_size[1]
    # pygame.draw.circle(canvas, outline_color, (canvas.get_width()//2, canvas.get_height()//2), 
    #                    min(canvas.get_width()//2-border, canvas.get_height()//2-border))