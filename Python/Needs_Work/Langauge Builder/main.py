import pygame
from package import Phonology

color = Phonology.set_background()
trim = 20

screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)


running = True
while running:
    h = screen.get_height()
    w = screen.get_width()
    screen.fill(color)
    square = pygame.Rect((trim, trim), (w-(2*trim), h-(2*trim)))
    pygame.draw.rect(screen, (255, 255, 255), square)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(f"{pos[0]}, {pos[1]}")
    pygame.display.flip()

Phonology.start_print()
pygame.quit()