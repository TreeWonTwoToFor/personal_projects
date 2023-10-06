import pygame

pygame.init()

screenX = 1080
screenY = 720
bg_color = (34, 238, 85)

screen = pygame.display.set_mode((screenX, screenY))

running = True
while running:
    screen.fill(bg_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

pygame.quit()
