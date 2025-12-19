import pygame
import math
import random

j_held, f_held, i_held, k_held, e_held, d_held = False, False, False, False, False, False
h_held, g_held, o_held, w_held, l_held, s_held = False, False, False, False, False, False

turning = -1
layers = None
layer_names = ['u', 'd', 'f', 'b', 'r', 'l']
side_index = None
frame_count = 10
amount = math.pi/frame_count/2

def player_movement(event, using_mouse):
    global j_held,f_held,i_held,k_held,e_held,d_held,h_held,g_held,o_held,w_held,l_held,s_held
    if event.type == pygame.KEYDOWN:
        match event.key:
            case pygame.K_j: j_held = True 
            case pygame.K_f: f_held = True 
            case pygame.K_i: i_held = True  
            case pygame.K_k: k_held = True 
            case pygame.K_e: e_held = True 
            case pygame.K_d: d_held = True 
            case pygame.K_h: h_held = True  
            case pygame.K_g: g_held = True 
            case pygame.K_o: o_held = True 
            case pygame.K_w: w_held = True 
            case pygame.K_l: l_held = True  
            case pygame.K_s: s_held = True 
            case pygame.K_ESCAPE: return True
    if event.type == pygame.KEYUP:
        match event.key:
            case pygame.K_j: j_held = False
            case pygame.K_f: f_held = False 
            case pygame.K_i: i_held = False
            case pygame.K_k: k_held = False
            case pygame.K_e: e_held = False
            case pygame.K_d: d_held = False 
            case pygame.K_h: h_held = False
            case pygame.K_g: g_held = False
            case pygame.K_o: o_held = False
            case pygame.K_w: w_held = False 
            case pygame.K_l: l_held = False
            case pygame.K_s: s_held = False
    return False

def player_movement_update(camera, using_mouse, mouse_sensitivity, object_list):
    return 0

# j = U, f = U'
# s = D, l = D'
# i = R, k = R'
# d = L, e = L'
# h = F, g = F'
# w = B, o = B'

def game_logic(object_list):
    global turning, layers, side_index, amount
    if turning == -1 or layers == None:
        layers = get_layers(object_list)
        if j_held:
            side_index = 0
        elif f_held:
            side_index = 0
            amount *= -1
        elif s_held:
            side_index = 1
            amount *= -1
        elif l_held:
            side_index = 1
        elif h_held:
            side_index = 2
        elif g_held:
            side_index = 2
            amount *= -1
        elif w_held:
            side_index = 3
            amount *= -1
        elif o_held:
            side_index = 3
        elif i_held:
            side_index = 4
            amount *= -1
        elif k_held:
            side_index = 4
        elif d_held:
            side_index = 5
        elif e_held:
            side_index = 5
            amount *= -1
        if side_index != None:
            turning = 0
    else:
        turning += 1
        turn_layer(layers[side_index], layer_names[side_index], amount)
        if turning == frame_count:
            turning = -1
            amount = math.fabs(amount)
            side_index = None

def scramble(object_list):
    turn_list = []
    while len(turn_list) < 20: 
        turn_side = layer_names[random.randint(0,5)]
        if len(turn_list) > 0 and turn_side == turn_list[-1][0]:
            # we have the same layer turned
            continue
        is_prime = random.randint(0,1)
        turn_list.append((turn_side, is_prime))
    for turn in turn_list:
        layers = get_layers(object_list)
        turn_index = layer_names.index(turn[0])
        turn_value = math.pi/2
        if turn[1] == 1:
            turn_value *= -1
        turn_layer(layers[turn_index], turn[0], turn_value)
    
def get_layers(object_list):
    u_lay, d_lay, f_lay, b_lay, r_lay, l_lay = [], [], [], [], [], []
    layers = [u_lay, d_lay, f_lay, b_lay, r_lay, l_lay]
    for piece in object_list[1:]:
        pos = piece.center_point
        if pos[0] > 1.9:
            l_lay.append(piece)
        elif pos[0] < -1.9:
            r_lay.append(piece)
        if pos[1] > 1.9:
            u_lay.append(piece)
        elif pos[1] < -1.9:
            d_lay.append(piece)
        if pos[2] > 1.9:
            f_lay.append(piece)
        elif pos[2] < -1.9:
            b_lay.append(piece)
    return layers

def turn_layer(pieces, side, direction):
    match side:
        case 'r' | 'l':
            for piece in pieces:
                piece.orbit([1,0,0], direction)
                piece.rotate([1,0,0], direction)
        case 'u' | 'd':
            for piece in pieces:
                piece.orbit([0,1,0], direction)
                piece.rotate([0,1,0], direction)
        case 'f' | 'b':
            for piece in pieces:
                piece.orbit([0,0,1], direction)
                piece.rotate([0,0,1], direction)
