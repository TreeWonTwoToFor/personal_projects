import pygame
from pygame import mixer

pygame.init()

screen_resolution = (500, 500)
disk_resolution = (500, 500)
FPS = 60
rotation_amount = 360
volume = 0.05
screen = pygame.display.set_mode(screen_resolution)
clock = pygame.time.Clock()
disk_overlay = pygame.image.load("disk_overlay.png")
disk = pygame.transform.scale(pygame.image.load("disk.png"), disk_resolution)
mixer.music.load("song.mp3")
mixer.music.set_volume(0.05) 
mixer.music.play() 

def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect)

def mouse_action(start, end):
    global volume
    if start[0] > 250 and end[0] > 250: # on the right side
        if end[1] - start[1] < 50: # scroll up 
            volume += 0.05
        elif end[1] - start[1] > 50: # scroll down
            volume -= 0.05
    volume_update()
    
def volume_update():
    mixer.music.set_volume(volume)

running = True
while running:
    screen.fill((255,255,255))
    blitRotateCenter(screen, disk, (0,0), rotation_amount)
    screen.blit(disk_overlay, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = pygame.mouse.get_pos()
            drawing = True
        if event.type == pygame.MOUSEBUTTONUP:
            end_pos = pygame.mouse.get_pos()
            drawing = False
            mouse_action(start_pos, end_pos)
    rotation_amount -= 1
    if rotation_amount < 0: rotation_amount = 360
    clock.tick(FPS)
    pygame.display.update()