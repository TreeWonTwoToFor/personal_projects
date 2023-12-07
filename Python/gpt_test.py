import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Improved Mario Game")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Set up Mario
class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.y_speed = 0

    def jump(self):
        if self.rect.bottom == screen_height:
            self.y_speed = -20

    def update(self):
        self.y_speed += 1
        self.rect.y += self.y_speed
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.y_speed = 0

# Set up blocks
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Create sprite groups
all_sprites = pygame.sprite.Group()
blocks_group = pygame.sprite.Group()

# Create Mario and add to sprite group
mario = Mario(screen_width // 2 - 25, screen_height - 60)
all_sprites.add(mario)

# Create blocks and add to sprite group
blocks_data = [(200, 400), (300, 300), (400, 400), (500, 300)]
for block_data in blocks_data:
    block = Block(*block_data)
    all_sprites.add(block)
    blocks_group.add(block)

# Set up game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mario.jump()

    # Handle user input
    keys = pygame.key.get_pressed()
    mario.rect.x += (keys[pygame.K_d] - keys[pygame.K_a]) * 5  # Move right with D, left with A

    # Update sprites
    all_sprites.update()

    # Check for collisions with blocks
    on_ground = pygame.sprite.spritecollide(mario, blocks_group, False)
    if on_ground and mario.y_speed > 0:
        mario.rect.y = on_ground[0].rect.top - mario.rect.height
        mario.y_speed = 0

    # Draw everything
    screen.fill(white)
    all_sprites.draw(screen)

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
