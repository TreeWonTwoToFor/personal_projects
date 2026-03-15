import pygame
import math
import numpy
import random

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
    # OG RETURN FUNCTION: return (bx+size_x,by+size_y)
    return (bx+size_x,size_y-by)

def array_dot_product(face_array, camera_array):
    face_vector = numpy.array(face_array)
    camera_vector = numpy.array(camera_array)
    dp = numpy.dot(face_vector, camera_vector)
    return dp

# General drawing functions
def draw_pt(screen, coords, color):
    # this is simply to help make it easier to quickly draw a point
    pygame.draw.circle(screen, color, coords, 2)

def draw_from_lines(screen, camera, line_list, offset=(0,0,0)):
    # line_list is just a list of pairs of 3d points
    for line in line_list:
        point_a = perspective_projection(
            (line[0][0]+offset[0],line[0][1]+offset[1],line[0][2]+offset[2]), 
            camera)
        point_b = perspective_projection(
            (line[1][0]+offset[0],line[1][1]+offset[1],line[1][2]+offset[2]), 
            camera)
        pygame.draw.line(screen, (255, 255, 255), point_a, point_b)

def draw_polygons_wireframe(screen, camera, pair_list, offset=(0,0,0)):
    for pair in pair_list:
        point_a = perspective_projection(screen, pair[0], camera)
        point_b = perspective_projection(screen, pair[1], camera)
        pygame.draw.line(screen, (255,255,255), point_a, point_b)     

# 'main' function of Draw
def draw_frame(screen, camera, obj_list, debug, clock):
    screen.fill((0,0,0))
    for obj in obj_list[1:]: # don't draw the camera's hitbox
        draw_polygons_wireframe(screen, camera, obj.model)
        if debug:
            draw_polygons_wireframe(screen, camera, obj.collision_box)
    camera.fix_angles() # keeps the camera's angles in realistic boundaries.
    if debug: camera.show_pos(screen, round(clock.get_fps(), 2))
    pygame.display.update()
