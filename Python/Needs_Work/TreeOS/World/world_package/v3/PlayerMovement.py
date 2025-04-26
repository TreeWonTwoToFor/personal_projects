import pygame
import math

# NOTE: This system presumes arrow keys for looking around. Mouse movement should also be considered.

w_held, a_held, s_held, d_held = False, False, False, False
left_held, right_held, up_held, down_held = False, False, False, False

def player_movement(event):
    global w_held, a_held, s_held, d_held, left_held, right_held, up_held, down_held
    if event.type == pygame.KEYDOWN:
        match event.key:
            case pygame.K_w: w_held = True 
            case pygame.K_s: s_held = True 
            case pygame.K_a: a_held = True  
            case pygame.K_d: d_held = True 
            case pygame.K_LEFT: left_held = True 
            case pygame.K_RIGHT: right_held = True 
            case pygame.K_UP: up_held = True  
            case pygame.K_DOWN: down_held = True 
            case pygame.K_ESCAPE: return True
    if event.type == pygame.KEYUP:
        match event.key:
            case pygame.K_w: w_held = False
            case pygame.K_s: s_held = False 
            case pygame.K_a: a_held = False
            case pygame.K_d: d_held = False
            case pygame.K_LEFT: left_held = False
            case pygame.K_RIGHT: right_held = False 
            case pygame.K_UP: up_held = False
            case pygame.K_DOWN: down_held = False
    return False

def player_movement_update(camera):
    if w_held: camera.move(0)
    if s_held: camera.move(math.pi)
    if a_held: camera.move(math.pi/2)
    if d_held: camera.move(-math.pi/2)
    if up_held: camera.angle.x += 0.02
    if down_held: camera.angle.x -= 0.02
    if left_held: camera.angle.y -= 0.02
    if right_held: camera.angle.y += 0.02