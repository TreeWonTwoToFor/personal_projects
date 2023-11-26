import pygame
from package import Phonology

color = Phonology.set_background()
trim = 20

screen = pygame.display.set_mode((800, 600))
screen.fill(color)

class my_rect:
    rect_pre_cut = screen.get_size()
    rectx = rect_pre_cut[0]-trim*2
    recty = rect_pre_cut[1]-trim*2
    color = (200,200,200)

pygame.draw.rect(screen, my_rect.color, pygame.Rect(trim, trim, my_rect.rectx, my_rect.recty))
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(f"{pos[0]}, {pos[1]}")


Phonology.start_print()
pygame.quit()