import pygame
import math
import numpy
import random

from Engine import Point

frustum_planes = None
camera_pos = None

def get_view_frustum(screen_resolution, camera):
    pitch, yaw, roll = camera.angle.x, camera.angle.y, camera.angle.z
    # calculate camera's forward, right, and up vectors for view matrix
    forward = [math.cos(pitch) * math.sin(yaw)]
    forward.append(math.sin(pitch))
    forward.append(math.cos(pitch) * math.cos(yaw))
    forward = numpy.array(forward)
    forward = forward/numpy.linalg.norm(forward)
    right = numpy.cross(numpy.array([0,1,0]), forward)
    right = right/numpy.linalg.norm(right)
    up = numpy.cross(forward, right)
    up = up/numpy.linalg.norm(up)
    
    # perspective projection matrix
    near = 0.1
    far = 1000.0
    fovX = math.pi/2
    aspect = screen_resolution[0]/screen_resolution[1]
    fovY = 2 * math.atan(math.tan(fovX/2)/aspect)
    f = 1 / math.tan(fovY/2)
    
    # matrix construction
    eye = numpy.array([camera.point.x, camera.point.y, camera.point.z])
    view = numpy.array([
        [right[0], right[1], right[2], -numpy.dot(right, eye)],
        [up[0], up[1], up[2], -numpy.dot(up,eye)],
        [-forward[0], -forward[1], -forward[2], numpy.dot(forward, eye)],
        [0,0,0,1]
    ])
    projection = numpy.array([
        [f/aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, -(far+near)/(far-near), -(2*far*near)/(far-near)],
        [0, 0, -1, 0]
    ])
    VP = projection @ view
    
    # plane extraction
    planes = []
    planes.append(VP[3] + VP[0])   # left
    planes.append(VP[3] - VP[0])   # right
    planes.append(VP[3] + VP[1])   # bottom
    planes.append(VP[3] - VP[1])   # top
    planes.append(VP[3] + VP[2])   # far
    planes.append(VP[3] - VP[2])   # near
    
    # normalize the planes
    for i in range(6):
        n = planes[i][:3]
        mag = numpy.linalg.norm(n)
        planes[i] = planes[i] / mag
    
    return planes

def aabb_outside_plane(plane, aabb_min, aabb_max):
    normal = plane[:3]
    positive_vertex = numpy.where(normal >= 0, aabb_max, aabb_min)
    distance = numpy.dot(normal, positive_vertex) + plane[3]
    return distance < 0

def perspective_projection(screen_resolution, projected_point, camera):
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
    size_x, size_y = screen_resolution[0]//2, screen_resolution[1]//2
    recording_x, recording_y, recording_z = screen_resolution[0]//100, screen_resolution[1]//100, 10
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

def draw_3d_point(screen, point, color, camera):
    new_point = perspective_projection(
        [screen.get_width(), screen.get_height()], point, camera)
    draw_pt(screen, new_point, color)

def draw_3d_line(screen, point_a, point_b, color, camera):
    new_point_a = perspective_projection(
        [screen.get_width(), screen.get_height()], point_a, camera)
    new_point_b = perspective_projection(
        [screen.get_width(), screen.get_height()], point_b, camera)
    draw_pt(screen, new_point_a, color)
    draw_pt(screen, new_point_b, color)
    pygame.draw.line(screen, color, new_point_a, new_point_b)

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
    # sort based on how far the centroid is from the camera
    sorted_list = sorted(output_list, key=lambda row: row[1], reverse=True)
    final_list = []
    for poly in sorted_list:
        final_list.append(poly[0])
    return final_list

def draw_polygons(screen, camera, obj_list, clock, offset=(0,0,0)):
    global frustum_planes
    sun = [100, 80, 90]
    poly_list = []
    # sorting all of the objects into one list to ensure proper ordering
    for obj in obj_list:
        out_of_bounds = False
        for plane in frustum_planes:
            if aabb_outside_plane(plane, obj.aabb_min, obj.aabb_max):
                out_of_bounds = True
                break
        if not out_of_bounds:
            poly_list = obj.model + poly_list
    poly_list = sort_polygons(camera, poly_list)
    # render polygons, one by one
    for poly in poly_list:
        direction_vector = numpy.array([
            camera.point.x - poly[0][0][0],
            camera.point.y - poly[0][0][1],
            camera.point.z - poly[0][0][2]])
        # calculating face vectors
        vector_a, vector_b = [], []
        for i in range(3):
            vector_a.append(round(poly[0][0][i] - poly[0][1][i], 4))
            vector_b.append(round(poly[0][0][i] - poly[0][2][i], 4))
        vector_a, vector_b = numpy.array(vector_a), numpy.array(vector_b)
        poly[1] = numpy.cross(vector_a, vector_b)
        # back culling
        if numpy.dot(direction_vector, poly[1]) < 0:
            continue
        # using face vector to calculate light intensity
        color_mod = array_dot_product(sun, poly[1])/(
            vector_magnitude(sun)*vector_magnitude(poly[1]))
        if color_mod < 0: color_mod = 0
        poly_color = list(poly[2])
        for i in range(3): 
            poly_color[i] = poly_color[i]*color_mod
            if poly_color[i] < 20: poly_color[i] = 20
        # rendering polygons
        ss = screen.get_size()
        perspective_poly = []
        for point in poly[0]:
            perspective_poly.append(perspective_projection(ss, point, camera))
        pygame.draw.polygon(screen, poly_color, perspective_poly)
        # NOTE: enable for poly by poly rendering.
        #pygame.display.update()
        #clock.tick(1)

# 'main' function of Draw
def draw_frame_poly(screen, camera, obj_list, debug, clock):
    # we don't draw the camera's bounding box
    global camera_pos, frustum_planes
    current_camera = ((camera.point.x, camera.point.y, camera.point.z),(camera.angle.x, camera.angle.y))
    if camera_pos != current_camera:
        frustum_planes = get_view_frustum(screen.get_size(), camera)
        camera_pos = current_camera
    draw_polygons(screen, camera, obj_list[1:], clock)
    camera.fix_angles() # keeps the camera's angles in realistic boundaries.
    if debug: camera.show_pos(screen, round(clock.get_fps(), 2))
