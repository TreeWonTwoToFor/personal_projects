import pygame
import math

from Engine import Point

w_held, a_held, s_held, d_held = False, False, False, False
left_held, right_held, up_held, down_held = False, False, False, False

def player_movement(event, using_mouse):
    global w_held, a_held, s_held, d_held, left_held, right_held, up_held, down_held
    if not using_mouse:
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
    else:
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_w: w_held = True 
                case pygame.K_s: s_held = True 
                case pygame.K_a: a_held = True  
                case pygame.K_d: d_held = True 
                case pygame.K_ESCAPE: return True
        if event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_w: w_held = False
                case pygame.K_s: s_held = False 
                case pygame.K_a: a_held = False
                case pygame.K_d: d_held = False
    return False

def player_movement_update(camera, using_mouse, mouse_sensitivity, object_list):
    old_camera_position = Point.Point(camera.point.x, camera.point.y, camera.point.z)
    if w_held: 
        camera.move(0)
    if s_held: 
        camera.move(math.pi)
    if a_held: 
        camera.move(math.pi/2)
    if d_held: 
        camera.move(-math.pi/2)
    # if we are running into an object, undo that move
    if object_collision(camera, object_list):
        camera.point = old_camera_position

    if not using_mouse:
        if up_held: camera.angle.x -= 0.02
        if down_held: camera.angle.x += 0.02
        if left_held: camera.angle.y -= 0.02
        if right_held: camera.angle.y += 0.02
    else:
        mouse_x, mouse_y = pygame.mouse.get_rel()
        camera.angle.x += mouse_sensitivity*(mouse_y/500)
        camera.angle.y += mouse_sensitivity*(mouse_x/500)
        pygame.mouse.set_pos((300, 300))

def object_collision(camera, object_list):
    player = camera.bounding_box.collision_values
    intersect_list = []
    for object in object_list[1:]:
        object_values = object.collision_values
        intersect_list.append(
            player[0] <= object_values[3] and # x low
            player[1] <= object_values[4] and # y low
            player[2] <= object_values[5] and # z low
            player[3] >= object_values[0] and # x max
            player[4] >= object_values[1] and # y max
            player[5] >= object_values[2]     # z max
        )
    # returns TRUE if intersecting with another object
    for intersect in intersect_list:
        if intersect: return True
    return False
    
