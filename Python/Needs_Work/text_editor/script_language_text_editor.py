import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 32
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adjustable Tilemap")

clock = pygame.time.Clock()

# Define the tilemap
tilemap = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8],
    [1, 2, 3, 4, 5, 6, 7, 8, 0]
]

# Load images
tile_images = {
    0: pygame.Surface((TILE_SIZE, TILE_SIZE)),
    1: pygame.image.load("d.png"),
    2: pygame.image.load("t.png"),
    3: pygame.image.load("k.png"),
    4: pygame.image.load("g.png"),
    5: pygame.image.load("n.png"),
    6: pygame.image.load("m.png"),
    7: pygame.image.load("h.png"), 
    8: pygame.image.load("p.png"), 
}

# Main game loop
key_pressed = False
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and key_pressed == False:
            key_pressed = True
            print(event.key)
            if event.key == pygame.K_SPACE:
                tilemap[0][0] = 0
        if event.type == pygame.KEYUP:
            key_pressed = False

    # Handle player input here

    # Update the game state here

    # Draw the tilemap
    for row_index, row in enumerate(tilemap):
        for col_index, tile in enumerate(row):
            screen.blit(tile_images[tile], (col_index * TILE_SIZE, row_index * TILE_SIZE))

    pygame.display.flip()
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()
