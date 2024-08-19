import os
import time
import pygame
from math import *

import pygame.draw

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()

angle = 0

projection_matrix = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
]

point_matrix = [
    [1, 1, 1],
    [1, 1, -1],
    [1, -1, -1],
    [1, -1, 1],
    [-1, -1, 1],
    [-1, -1, -1],
    [-1, 1, -1],
    [-1, 1, 1]
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

running = True
while running:
    screen.fill((0,0,0))
    angle += 0.005
    rotation_x = [
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)]
    ]

    rotation_y = [
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)]
    ]

    rotation_z = [
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1]
    ]
    my_matrix = matrix_m(rotation_z, matrix_m(rotation_y, matrix_m(rotation_x, point_matrix)))
    os.system('cls')
    projected_point_list = []
    for point in my_matrix: print(point)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for point in my_matrix:
        for i in range(len(point)):
            point[i] = (point[i] * 100)
        projected_point = (project(point[0], point[2], 1000)+400, project(point[1], point[2], 1000)+400)
        projected_point_list.append(projected_point)
        pygame.draw.circle(screen, (0, 200, 50), projected_point, 5)
    draw_cube(projected_point_list)
    pygame.display.update()
    clock.tick(60)