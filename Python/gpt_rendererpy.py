import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 32
GRID_WIDTH, GRID_HEIGHT = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE
FPS = 60

LIGHT_GREEN = (144, 238, 144)
GREY = (169, 169, 169)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

HOTBAR_HEIGHT = 50
HOTBAR_ITEM_WIDTH = 50

SQUARE, CIRCLE, TRIANGLE, HEXAGON = "square", "circle", "triangle", "hexagon"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Factory Building Game")
clock = pygame.time.Clock()

offset_x, offset_y = 0, 0

hotbar_items = [
    {"type": SQUARE, "color": WHITE, "selected_color": (255, 0, 0)},
    {"type": CIRCLE, "color": WHITE, "selected_color": (255, 0, 0)},
    {"type": TRIANGLE, "color": WHITE, "selected_color": (255, 0, 0)},
    {"type": HEXAGON, "color": WHITE, "selected_color": (255, 0, 0)},
]

def draw_shape(surface, color, x, y, size, shape_fn):
    shape_fn(surface, color, x, y, size)

def draw_square(surface, color, x, y, size):
    pygame.draw.rect(surface, color, (x, y, size, size), 0)

def draw_circle(surface, color, x, y, size):
    pygame.draw.circle(surface, color, (x + size // 2, y + size // 2), size // 2, 0)

def draw_triangle(surface, color, x, y, size):
    pygame.draw.polygon(surface, color, [(x + size // 2, y), (x, y + size), (x + size, y + size)], 0)

def draw_hexagon(surface, color, x, y, size):
    angle, x_offset, y_offset = 2 * math.pi / 6, size // 2, size // 3 + 10  # Adjusted the y_offset
    vertices = [(x + x_offset + int(size * 0.65 * math.cos(i * angle)), y + y_offset + int(size * 0.65 * math.sin(i * angle))) for i in range(6)]
    pygame.draw.polygon(surface, color, vertices, 0)

building_draw_functions = {SQUARE: draw_square, CIRCLE: draw_circle, TRIANGLE: draw_triangle, HEXAGON: draw_hexagon}

running, panning, pan_start = True, False, (0, 0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                panning, pan_start = True, event.pos
            elif event.button == 1:
                x, y = event.pos
                if HEIGHT - HOTBAR_HEIGHT <= y <= HEIGHT:
                    clicked_box = x // HOTBAR_ITEM_WIDTH
                    if 0 <= clicked_box < len(hotbar_items):
                        for item in hotbar_items:
                            item["color"] = WHITE
                        selected_building = hotbar_items[clicked_box]
                        selected_building["color"] = selected_building["selected_color"]
                        print(f"Selected Building Type: {selected_building['type']}")

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            panning = False
        elif event.type == pygame.MOUSEMOTION and panning:
            dx, dy = event.rel
            offset_x -= dx
            offset_y -= dy

    screen.fill(LIGHT_GREEN)

    for x in range(0, WIDTH, TILE_SIZE):
        pygame.draw.line(screen, GREY, (x - offset_x, -offset_y), (x - offset_x, HEIGHT - offset_y))
    for y in range(0, HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, GREY, (-offset_x, y - offset_y), (WIDTH - offset_x, y - offset_y))

    pygame.draw.rect(screen, GREY, (0, HEIGHT - HOTBAR_HEIGHT, WIDTH, HOTBAR_HEIGHT))
    for i, item in enumerate(hotbar_items):
        pygame.draw.rect(screen, BLACK, (i * HOTBAR_ITEM_WIDTH, HEIGHT - HOTBAR_HEIGHT, HOTBAR_ITEM_WIDTH, HOTBAR_HEIGHT), 2)
        draw_shape(screen, item["color"], i * HOTBAR_ITEM_WIDTH + 2, HEIGHT - HOTBAR_HEIGHT + 2, HOTBAR_ITEM_WIDTH - 4, building_draw_functions[item["type"]])

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
