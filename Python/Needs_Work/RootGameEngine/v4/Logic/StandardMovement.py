import pygame
import math

w_held, a_held, s_held, d_held = False, False, False, False
left_held, right_held, up_held, down_held = False, False, False, False
space_held, shift_held = False, False

def player_movement(screen, event):
    global w_held, a_held, s_held, d_held, left_held, right_held, up_held, down_held, space_held, shift_held
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
            case pygame.K_SPACE: space_held = True 
            case pygame.K_LSHIFT: shift_held = True 
            case pygame.K_ESCAPE: return True
            case pygame.K_BACKSPACE: pygame.image.save(screen, "screenshot.png")
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
            case pygame.K_SPACE: space_held = False
            case pygame.K_LSHIFT: shift_held = False
        
    return False

def player_movement_update(camera, using_mouse, mouse_sensitivity, object_list, dt):
    old_camera_position = (camera.point[0], camera.point[1], camera.point[2])
    old_camera_hitbox = camera.bounding_box
    if w_held: camera.move_direction(0, dt)
    if s_held: camera.move_direction(math.pi, dt)
    if a_held: camera.move_direction(math.pi/2, dt)
    if d_held: camera.move_direction(-math.pi/2, dt)
    if space_held:camera.move_vertically("up", dt)
    if shift_held:camera.move_vertically("down", dt)
    # if we are running into an object, undo that move
    if object_collision(camera, object_list):
        camera.point = old_camera_position
        camera.bounding_box = old_camera_hitbox

    if not using_mouse:
        if up_held: camera.angle[0] -= 2*dt
        if down_held: camera.angle[0] += 2*dt
        if left_held: camera.angle[1] -= 2*dt
        if right_held: camera.angle[1] += 2*dt
    else:
        mouse_x, mouse_y = pygame.mouse.get_rel()
        camera.angle[0] += mouse_sensitivity*(mouse_y/500)
        camera.angle[1] += mouse_sensitivity*(mouse_x/500)
        # ensures that the camera is within vertical bounds
        # NOTE: it wraps around the value 360 for the yaw,
        #       which means that there's two angles that rerpesents any camera direction
        nintey_degrees = math.pi/2
        three_sixty_degrees = 2 * math.pi
        if camera.angle[0] < -nintey_degrees: camera.angle[0] = -nintey_degrees
        if camera.angle[0] > nintey_degrees: camera.angle[0] = nintey_degrees
        if camera.angle[1] > three_sixty_degrees: camera.angle[1] = camera.angle[1]%three_sixty_degrees
        if camera.angle[1] < -three_sixty_degrees: camera.angle[1] = camera.angle[1]%three_sixty_degrees

def object_collision(camera, object_list):
    # FIXME: the collision checking doesn't work well. double check interset_list.append values
    player = camera.bounding_box.collision_values
    intersect_list = []
    for object in object_list:
        object_values = object.collision_values
        intersect_list.append(
            player[0] <= object_values[3] and # x low
            player[1] <= object_values[4] and # y low
            player[2] <= object_values[5] and # z low
            player[3] >= object_values[0] and # x max
            player[4] >= object_values[1] and # y max
            player[5] >= object_values[2]     # z max
        )
    # return True in intersect_list
    
def game_logic(object_list):
    # nothing to do
    return 0
