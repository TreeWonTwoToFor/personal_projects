import pygame
import math

from Engine import Point

pressing_space = False
flapped = False

def player_movement(event, mouse_control):
    global pressing_space
    if event.type == pygame.KEYDOWN:
        match event.key:
            case pygame.K_SPACE: pressing_space = True
            case pygame.K_ESCAPE: return True
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_SPACE:
            pressing_space = False
    return False

def player_movement_update(camera, m_control, m_sensitivity, object_list):
    global flapped
    if pressing_space and not flapped:
        flapped = True
        object_list[1].translate((0,2,0))
    elif not pressing_space and flapped:
        flapped = False

    if object_collision(object_list):
        print('you died')

def game_logic(object_list):
    pipes = object_list[2:]
    for i in range(len(pipes)-1):
        bottom = pipes[i]
        top = pipes[i]
        if bottom.center_point[0] > 10:
            bottom.move_to_origin()
            top.move_to_origin()
            height = (random.random()-0.5) * 4
            bottom.translate((-16, -5.5 + height, 0))
            top.translate((-16, 5.5 + height, 0))

def object_collision(object_list):
    player = object_list[1].collision_values
    intersect_list = []
    for obj in object_list[2:]:
        object_values = obj.collision_values
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
    
