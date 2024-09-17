import os
import time
import pygame
from math import *

import pygame.draw

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Comfortaa", 32)

angle = 0
camera_pos = [0, 0, 400]
point_matrix = [
    [10, 10, 0],
    [10, 10, -20],
    [10, -10, -20],
    [10, -10, 0],
    [-10, -10, 0],
    [-10, -10, -20],
    [-10, 10, -20],
    [-10, 10, 0]
]

cross_matrix = [
    [2,0,1],
    [0,0,1],
    [0,2,1],
    [0,0,1],
    [0,0,3]
]

def matrix_m(a, b):
    # a is going to be a modifying matrix
    # b is going to be a 3d point matrix
    a_row = len(a)
    b_row = len(b)
    a_col = len(a[0])
    b_col = len(b[0])

    out_matrix = []

    for i in range(b_row):
        mini_output = []
        for j in range(a_col):
            running_total = 0
            for k in range(b_col):
                running_total += b[i][k] * a[j][k]
            mini_output.append(running_total)
        out_matrix.append(mini_output)

    return out_matrix

def project(axis_to_project, z, FL):
    return (FL * axis_to_project)/(FL + z)

def draw_segment(point_a, point_b):
    pygame.draw.line(screen, (0, 200, 50), point_a, point_b)

def draw_cube(projected_point_list):
    for i in range(4):
        draw_segment(projected_point_list[i], projected_point_list[7-i])
        if i+1 !=4: 
            draw_segment(projected_point_list[i], projected_point_list[i+1]) 
            draw_segment(projected_point_list[i+4], projected_point_list[i+5]) 
        else: 
            draw_segment(projected_point_list[i], projected_point_list[0])
            draw_segment(projected_point_list[i+4], projected_point_list[4])

def draw_attached_segments(point_list):
    for i in range(len(point_list)):
        if i+1 != len(point_list):
            draw_segment(point_list[i], point_list[i+1])

def camera_transform(matrix, camera_position):
    out_matrix = []
    for point in matrix: out_matrix.append([0, 0, point[2]])
    for p in range(len(matrix)):
        for i in range(len(point)-1):
            out_matrix[p][i] = matrix[p][i]-camera_position[i]
    return out_matrix

def revolve_point(point, camera, amount):
    distance = sqrt(pow((camera[0]-point[0]), 2) + pow((camera[2]-point[2]), 2))
    difference = (camera[0]-point[0],camera[1]-point[1],camera[2]-point[2])
    scaled_difference = (difference[0]/distance, difference[2]/distance)
    print(scaled_difference) # we now have a point that we can compare to sin+cos in order to revolve the point


holding_w, holding_a, holding_s, holding_d = False, False, False, False
holding_left, holding_right, holding_up, holding_down = False, False, False, False
angle_x, angle_y, angle_z = 0, 0, 0
running = True
while running:
    screen.fill((0,0,0))
    text = font.render(f"{camera_pos[0]}, {camera_pos[1]}, {camera_pos[2]}", True, (255, 0, 0))
    screen.blit(text, (0,0))
    rotation_x = [
        [1, 0, 0],
        [0, cos(angle_y), -sin(angle_y)],
        [0, sin(angle_y), cos(angle_y)]
    ]

    rotation_y = [
        [cos(angle_x), 0, sin(angle_x)],
        [0, 1, 0],
        [-sin(angle_x), 0, cos(angle_x)]
    ]

    rotation_z = [
        [cos(angle_z), -sin(angle_z), 0],
        [sin(angle_z), cos(angle_z), 0],
        [0, 0, 1]
    ]
    #cube_matrix = matrix_m(rotation_z, matrix_m(rotation_y, matrix_m(rotation_x, camera_transform(point_matrix, camera_pos))))
    cube_matrix = camera_transform(matrix_m(rotation_z, matrix_m(rotation_y, matrix_m(rotation_x, point_matrix))), camera_pos)
    origin_matrix = camera_transform([[0,0,0]], camera_pos)
    print(point_matrix)
    print(camera_pos)
    os.system('cls')
    projected_cube_list = []
    #for point in cube_matrix: print(point)
    for point in cube_matrix:
        for i in range(len(point)):
            point[i] = (point[i] * 10)
        projected_point = (project(point[0], point[2], camera_pos[2])+400, project(point[1], point[2], camera_pos[2])+400)
        projected_cube_list.append(projected_point)
        pygame.draw.circle(screen, (0, 200, 50), projected_point, 5)
    pygame.draw.circle(screen, (0, 255, 0), (project(origin_matrix[0][0], origin_matrix[0][2], camera_pos[2]+400), project(origin_matrix[0][1], origin_matrix[0][2], camera_pos[2]+400)), 2)
    draw_cube(projected_cube_list)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w: holding_w = True
            if event.key == pygame.K_a: holding_a = True
            if event.key == pygame.K_s: holding_s = True
            if event.key == pygame.K_d: holding_d = True
            if event.key == pygame.K_LEFT: holding_left = True
            if event.key == pygame.K_RIGHT: holding_right = True
            if event.key == pygame.K_UP: holding_up = True
            if event.key == pygame.K_DOWN: holding_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w: holding_w = False
            if event.key == pygame.K_a: holding_a = False
            if event.key == pygame.K_s: holding_s = False
            if event.key == pygame.K_d: holding_d = False
            if event.key == pygame.K_LEFT: holding_left = False
            if event.key == pygame.K_RIGHT: holding_right = False
            if event.key == pygame.K_UP: holding_up = False
            if event.key == pygame.K_DOWN: holding_down = False
    if holding_w: camera_pos[2] -= 1
    if holding_a: camera_pos[0] -= 1
    if holding_s: camera_pos[2] += 1
    if holding_d: camera_pos[0] += 1
    if holding_left: angle_x -= 0.02
    if holding_right: angle_x += 0.02
    if holding_up: angle_y -= 0.02
    if holding_down: angle_y += 0.02
    pygame.display.update()
    clock.tick(60)