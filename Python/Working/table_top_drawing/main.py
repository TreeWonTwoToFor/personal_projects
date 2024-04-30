import pygame
import time

pygame.init()

screenX = 1080
screenY = 720
bg_color = (0,200,150)
FPS = 1000
clock = pygame.time.Clock()

screen = pygame.display.set_mode((screenX, screenY), pygame.RESIZABLE)

def draw(x, y, size):
    pygame.draw.circle(screen, (0,0,0), (x,y), size)

screen.fill(bg_color)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                screen.fill(bg_color)
    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        draw(mouse_pos[0], mouse_pos[1], 10)
    pygame.display.update()
    clock.tick(FPS)