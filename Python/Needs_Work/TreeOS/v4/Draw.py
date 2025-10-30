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

def vector_magnitude(vector):
    value = math.sqrt(vector[0]**2+vector[1]**2+vector[2]**2)
    if value == 0:
        return 0.001
    else:
        return value

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

def draw_3d_point(screen, point, color, camera):
    new_point = perspective_projection(screen, point, camera)
    draw_pt(screen, new_point, color)

def draw_3d_line(screen, point_a, point_b, color, camera):
    new_point_a = perspective_projection(screen, point_a, camera)
    new_point_b = perspective_projection(screen, point_b, camera)
    draw_pt(screen, new_point_a, color)
    draw_pt(screen, new_point_b, color)
    pygame.draw.line(screen, color, new_point_a, new_point_b)

def draw_polygons(screen, camera, poly_list, clock, offset=(0,0,0)):
    back_culling = False
    sun = [100, 80, 90]
    for poly in poly_list:
        perspective_poly = []
        direction_vector = [camera.point.x - poly[0][0][0]]
        direction_vector.append(camera.point.y - poly[0][0][1])
        direction_vector.append(camera.point.z - poly[0][0][2])
        color = array_dot_product(sun, poly[1])/(
            vector_magnitude(sun)*vector_magnitude(poly[1]))
        color = color * 255
        if color >= 20:
            poly_color = (color, color, color)
        else:
            poly_color = (25, 25, 25)
        if back_culling: 
            if array_dot_product(direction_vector, poly[1]) >= 0:
                for point in poly[0]:
                    perspective_poly.append(
                        perspective_projection(screen, point, camera))
                pygame.draw.polygon(screen, poly_color, perspective_poly)
        else:
            for point in poly[0]:
                perspective_poly.append(perspective_projection(screen, point, camera))
            pygame.draw.polygon(screen, poly_color, perspective_poly)
        # NOTE: enable for poly by poly rendering.
        #pygame.display.update()
        #clock.tick(1)

# sort the polygons from back to front to ensure no overlap
def sort_polygons(camera, poly_list, offset=(0,0,0)):
    output_list = []
    for poly in poly_list:
        centroid = [0,0,0]
        for vertex in poly[0]:
            for i in range(3): centroid[i] += vertex[i]
        for i in range(len(centroid)):
            centroid[i] = centroid[i] / len(poly[0])
        distance = math.sqrt(
            (camera.point.x - centroid[0])**2
            +(camera.point.y - centroid[1])**2
            +(camera.point.z - centroid[2])**2)
        output_list.append([poly, distance])
    sorted_list = sorted(output_list, key=lambda row: row[1], reverse=True)
    final_list = []
    for poly in sorted_list:
        final_list.append(poly[0])
    return final_list

# 'main' function of Draw
def draw_frame_poly(screen, camera, obj_list, debug, clock):
    #draw_3d_line(screen, (0,-2,0), (0,0,0), (255,0,0), camera)
    for obj in obj_list[1:]: # don't draw the camera's hitbox
        draw_polygons(screen, camera, sort_polygons(camera, obj.model), clock)
    camera.fix_angles() # keeps the camera's angles in realistic boundaries.
    if debug: camera.show_pos(screen, round(clock.get_fps(), 2))
