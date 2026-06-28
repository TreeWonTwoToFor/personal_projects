import pygame

tile_size = (45, 45)
grid_size = (40,20)
start_location = (25,25)

background_color = (255,255,255)
outline_color = (0,0,0)
tile_color = (240, 240, 200)
outline_width = 2

def run(canvas):
    logic_output = logic()
    draw(canvas, logic_output)

def draw(canvas, logic_output):
    canvas.fill(background_color)
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

def logic():
    pass