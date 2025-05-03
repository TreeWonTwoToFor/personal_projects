import pygame
import math

import Point
import Polygon

# Functions for 3d manipulations

def rotate_object(player_position, object_position, d_theta):
    # uses two 2d points and a change in rotation (radians) to return a point rotated about the player
    x = object_position[0] - player_position[0]
    y = math.fabs(object_position[1] - player_position[1])
    distance = math.sqrt(
        math.pow(x,2) + math.pow(y,2)
    )
    if x != 0: # avoiding a divide by 0 error
        theta = math.atan2(y, x)
    else:
        theta = -math.atan2(y, 1) # this negative is a little sus
    new_position = (math.cos(theta+d_theta)*distance+player_position[0], math.sin(theta+d_theta)*distance+player_position[1])
    return new_position

def perspective_projection(screen, projected_point, camera):
    # redefining our list inputs into points/vectors with names that align with wikipedia
    a = Point.Point(projected_point[0], projected_point[1], projected_point[2])
    c = camera.point
    theta = camera.angle
    # now we need to find the 'd' values, aka a vector that will intersect with the image surface
    # before we find the d values, let's match the variable names on the page
    cx, cy, cz = math.cos(theta.x), math.cos(theta.y), math.cos(theta.z)
    sx, sy, sz = math.sin(theta.x), math.sin(theta.y), math.sin(theta.z)
    x, y, z = (a.x-c.x), (a.y-c.y), (a.z-c.z)
    # now let's find our 3 d values
    dx = cy*(sz*y + cz*x) - sy*z
    dy = sx*(cy*z + sy*(sz*y + cz*x)) + cx*(cz*y - sz*x)
    dz = cx*(cy*z + sy*(sz*y + cz*x)) - sx*(cz*y - sz*x)
    if dz <= 0:
        dz = 0.001
    # now we need to find our 'b' values, which are the points projected to the screen.
    # size is the screen size, r is the 'recording surface'
    size_x, size_y = screen.get_width()//2, screen.get_height()//2
    recording_x, recording_y, recording_z = screen.get_width()//100, screen.get_height()//100, 10
    bx = (dx*size_x)/(dz*recording_x)*recording_z
    by = (dy*size_y)/(dz*recording_y)*recording_z
    # bx and by need to be centered to the screen instead of 0,0
    return (bx+size_x,by+size_y)

# General drawing functions

def draw_pt(screen, coords, color):
    # this is imply to help make it easier to quickly draw a point
    pygame.draw.circle(screen, color, coords, 2)

def draw_from_lines(screen, camera, line_list, offset=(0,0,0)):
    # line_list is just a list of pairs of 3d points
    for line in line_list:
        point_a = perspective_projection((line[0][0]+offset[0],line[0][1]+offset[1],line[0][2]+offset[2]), camera)
        point_b = perspective_projection((line[1][0]+offset[0],line[1][1]+offset[1],line[1][2]+offset[2]), camera)
        pygame.draw.line(screen, (255, 255, 255), point_a, point_b)

def draw_polygons(screen, camera, p_list, offset=(0,0,0)):
    for poly in range(len(p_list)//3):
        first = p_list[poly*3]
        second = p_list[poly*3+1]
        third = p_list[poly*3+2]
        point_a = perspective_projection(screen, first, camera)
        point_b = perspective_projection(screen, second, camera)
        point_c = perspective_projection(screen, third, camera)
        pygame.draw.line(screen, (255, 255, 255), point_a, point_b)
        pygame.draw.line(screen, (255, 255, 255), point_b, point_c)
        pygame.draw.line(screen, (255, 255, 255), point_c, point_a)

    # p_counter = 0
    # while p_counter < len(p_list)-2:
    #     first = (p_list[p_counter][0]+offset[0], p_list[p_counter][1]+offset[1], p_list[p_counter][2]+offset[2]) 
    #     second = (p_list[p_counter+1][0]+offset[0], p_list[p_counter+1][1]+offset[1], p_list[p_counter+1][2]+offset[2]) 
    #     third = (p_list[p_counter+2][0]+offset[0], p_list[p_counter+2][1]+offset[1], p_list[p_counter+2][2]+offset[2]) 
    #     point_a = perspective_projection(screen, first, camera)
    #     point_b = perspective_projection(screen, second, camera)
    #     point_c = perspective_projection(screen, third, camera)
    #     pygame.draw.line(screen, (255, 255, 255), point_a, point_b)
    #     pygame.draw.line(screen, (255, 255, 255), point_b, point_c)
    #     pygame.draw.line(screen, (255, 255, 255), point_c, point_a)
    #     p_counter += 1

# Specific implementations for other shapes.

def draw_circle(screen, camera):
    angle_change = 10
    angle_conversion = math.pi/(180//angle_change)
    for i in range((360//angle_change)):
        point_a = perspective_projection(screen, (math.cos(i*angle_conversion), 1, math.sin((i)*angle_conversion)), camera)
        point_b = perspective_projection(screen, (math.cos((i+1)*angle_conversion), 1, math.sin((i+1)*angle_conversion)), camera)
        pygame.draw.line(screen, (255,255,255), point_a, point_b)

def draw_sphere(screen, camera):
    angle_change = 10
    angle_conversion = math.pi/(180//angle_change)
    for i in range((360//angle_change)):
        point_a = perspective_projection(screen, (math.cos(i*angle_conversion), 1, math.sin((i)*angle_conversion)), camera)
        point_b = perspective_projection(screen, (math.cos((i+1)*angle_conversion), 1, math.sin((i+1)*angle_conversion)), camera)
        pygame.draw.line(screen, (255,255,255), point_a, point_b)
    for i in range((360//angle_change)):
        point_a = perspective_projection(screen, (0, math.cos(i*angle_conversion)+1, math.sin((i)*angle_conversion)), camera)
        point_b = perspective_projection(screen, (0, math.cos((i+1)*angle_conversion)+1, math.sin((i+1)*angle_conversion)), camera)
        pygame.draw.line(screen, (255,255,255), point_a, point_b)
    for i in range((360//angle_change)):
        point_a = perspective_projection(screen, (math.cos(i*angle_conversion), math.sin((i)*angle_conversion)+1, 0), camera)
        point_b = perspective_projection(screen, (math.cos((i+1)*angle_conversion), math.sin((i+1)*angle_conversion)+1, 0), camera)
        pygame.draw.line(screen, (255,255,255), point_a, point_b)

# 'main' function of Draw

def draw_frame(screen, camera, point_list, debug):
    screen.fill((0,0,0))
    #draw_sphere(screen, camera)
    poly_list = Polygon.points_to_polygons(point_list)
    print(poly_list)
    draw_polygons(screen, camera, point_list, (2,0,-0.5)) # in this case, it draws a cube
    camera.fix_angles() # keeps the camera's angles in realistic boundaries.
    if debug: camera.show_pos(screen)
    pygame.display.update()