import pygame

application_name = "BattleMap"

tile_size = (50, 50)
grid_size = ()

color_palette = "stone"
outline_width = 2

border = 25
start_location = (border,border)

def run(canvas_dict, desktop_instruction):
    canvas = canvas_dict[application_name].surface
    logic_output = logic(canvas.get_size())
    draw(canvas, logic_output)

def draw(canvas, logic_output):
    canvas.fill(background_color)
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

def logic(canvas_size):
    global background_color, outline_color, tile_color, grid_size
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