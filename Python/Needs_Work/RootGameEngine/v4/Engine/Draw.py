import math
import numpy
import pygame
import copy

from Engine import Helper
from Engine import ViewFrustum
from Engine import Rasterizer

frustum_planes = None
camera_pos = None

culling_coloring = False
frustum_culling = True
back_culling = True
lighting = True
homemade_rasterizer = False

# 'main' funtion of draw
def draw_frame_poly(screen, depth_buffer, camera, obj_list, light_list, debug, clock):
    global camera_pos, frustum_planes
    # remove unnecessary deatil from the camera
    current_camera = ((camera.point[0], camera.point[1], camera.point[2]),
                        (camera.angle[0], camera.angle[1], camera.angle[2]))
    # the camera position has changed since the last frame
    if camera_pos != current_camera:
        frustum_planes = ViewFrustum.get(screen, camera)
        camera_pos = current_camera
    draw_polygons(screen, depth_buffer, camera, obj_list, light_list)
    if debug: 
        camera.show_pos(screen, round(clock.get_fps(), 2))

def draw_polygons(screen, depth_buffer, camera, obj_list, light_list):
    # get screen information
    screen_size = (screen.get_width(), screen.get_height())
    screen_buffer = memoryview(screen.get_buffer())
    # remove objects that are completely outside our view
    culled_obj_list = frustum_culling(obj_list)
    for obj in culled_obj_list:
        poly_list = obj.model
        if not homemade_rasterizer:
            # Painter's Algorithm
            poly_list = sort_polygons(camera, poly_list)
        for poly in poly_list:
            direction_vector = [
                camera.point[0] - poly[0][0][0],
                camera.point[1] - poly[0][0][1],
                camera.point[2] - poly[0][0][2]]
            # back culling
            if back_culling and Helper.array_dp(direction_vector, poly[1]) < 0:
                continue
            # lighting
            if lighting:
                light_value = calculate_lighting(poly, light_list)
            else:
                light_value = 1
            # draw polygons onto the screen
            rasterize(
                poly, 
                camera, 
                screen, screen_buffer, screen_size, depth_buffer, 
                obj.texture, light_value
            )

def sort_polygons(camera, poly_list, offset=(0,0,0)):
    output_list = []
    for poly in poly_list:
        centroid = [0,0,0]
        for vertex in poly[0]:
            for i in range(3): centroid[i] += vertex[i]
        for i in range(len(centroid)):
            centroid[i] = centroid[i] / len(poly[0])
        distance = math.sqrt(
            (camera.point[0] - centroid[0])**2
            +(camera.point[1] - centroid[1])**2
            +(camera.point[2] - centroid[2])**2)
        output_list.append([poly, distance])
    # sort based on how far the centroid is from the camera
    sorted_list = sorted(output_list, key=lambda row: row[1], reverse=True)
    final_list = []
    for poly in sorted_list:
        final_list.append(poly[0])
    return final_list

def frustum_culling(obj_list):
    global frustum_planes
    culled_obj_list = []
    for obj in obj_list:
        out_of_bounds = False
        if frustum_culling:
            for plane in frustum_planes:
                if ViewFrustum.aabb_outside_plane(plane, obj.aabb_min, obj.aabb_max):
                    out_of_bounds = True
                    break
        if not out_of_bounds:
            culled_obj_list.append(obj)
    return culled_obj_list

def calculate_lighting(poly, light_list):
    light_value = 0
    for light in light_list:
        light_pos = light[0]
        light_str = light[1]
        color_mod = Helper.array_dp(light_pos, poly[1])/Helper.vector_magnitude(light_pos)
        if color_mod < 0: color_mod = 0
        light_value += (color_mod*(light_str/100))
    if light_value < 0.1: light_value = 0.1
    return light_value

def rasterize(poly, camera, screen, screen_buffer, screen_size, depth_buffer, texture, light_value):
    # perspective_poly format:
    # index 0 and 1 are for xy position, 2 is depth, 3 and 4 are uv values
    perspective_poly = []
    uv_values = poly[2]
    for i in range(len(poly[0])):
        point = poly[0][i]
        projected_point = Helper.perspective_projection(screen, point, camera)
        screen_pos = projected_point[0]
        depth = projected_point[1]
        perspective_poly.append([int(screen_pos[0]), int(screen_pos[1]), depth] + uv_values[i])
    poly_points = [pt[:2] for pt in perspective_poly]
    short_triangle = False
    for point in poly_points:
        x = point[0]
        y = point[1]
        if x < 0 or y < 0 or x > screen_size[0] or y > screen_size[1]:
            short_triangle = True
    clipped_points = copy.deepcopy(poly_points)
    # are there/how many vertices are outside of the screen?
    clipped_points = triangle_clipping(clipped_points, screen_size)
    poly_a, poly_b = None, None
    match len(clipped_points):
        case 0:
            # no work to do, just use poly_points
            pass
        case 3:
            # we have a perfectly new triangle, so just use those vertices with new uv values
            poly_points = clipped_points
            pass
        case 4:
            # use a fan algorithm to make two triangles
            poly_a = clipped_points[0:3]
            poly_b = clipped_points[1:4]
            pass
    if homemade_rasterizer:
        Rasterizer.draw_polygon(
            screen_buffer, screen_size, depth_buffer, 
            perspective_poly, texture, light_value
        )
    else:
        base_color = [255, 255, 255]
        if culling_coloring:
            short_triangle_color = [0, 255, 0]
            base_color_a = [255, 0, 0]
            base_color_b = [0, 0, 255]
        else:
            short_triangle_color = base_color
            base_color_a = base_color
            base_color_b = base_color
        if poly_a is None:
            if short_triangle:
                base_color = short_triangle_color
            lit_color = [x * light_value for x in base_color]
            pygame.draw.polygon(screen, lit_color, poly_points)
        else:
            lit_color_a = [x * light_value for x in base_color_a]
            lit_color_b = [x * light_value for x in base_color_b]
            pygame.draw.polygon(screen, lit_color_a, poly_a)
            pygame.draw.polygon(screen, lit_color_b, poly_b)
            

def triangle_clipping(poly_points, screen_size):
    clipped_vertices = []
    for i in range(len(poly_points)):
        pt = poly_points[i]
        x, y = pt[0], pt[1]
        left_cond = x < 0
        right_cond = x > screen_size[0]
        above_cond = y < 0
        below_cond = y > screen_size[1]
        bool_list = [left_cond, right_cond, above_cond, below_cond]
        clipped_vertices.append(bool_list)
    new_poly = []
    for i in range(len(clipped_vertices)):
        first_index = i
        second_index = i+1
        if second_index == len(clipped_vertices):
            second_index = 0
        first_clip = numpy.array(clipped_vertices[first_index])
        second_clip = numpy.array(clipped_vertices[second_index])
        and_clip = first_clip & second_clip
        if not first_clip.any() and not second_clip.any():
            # trivial accept, so just return that point
            continue
        elif and_clip.any():
            # we know that this full line segment it outside of the screen, so we should reject it.
            continue
        else:
            # the line crosses the screen somewhere
            first_pt = poly_points[first_index]
            second_pt = poly_points[second_index]
            x1, y1 = first_pt[0], first_pt[1]
            x2, y2 = second_pt[0], second_pt[1]

            # determining which points needs to be clipped
            if first_clip.any():
                clip = first_clip
                x, y = x1, y1
            else:
                clip = second_clip
                x, y = x2, y2

            if clip[0]: # left
                if x1 == x2: continue
                t = (0 - x1)/(x2-x1) # 0 as in left x value
                x = 0
                y = y1 + t * (y2 - y1)
            elif clip[1]: # right
                if x1 == x2: continue
                t = (screen_size[0] - x1)/(x2-x1)
                x = screen_size[0]
                y = y1 + t * (y2 - y1)
            elif clip[2]: # up
                if y1 == y2: continue
                t = (0 - y1)/(y2-y1)
                x = x1 + t * (x2 - x1)
                y = 0
            elif clip[3]: # down
                if y1 == y2: continue
                t = (screen_size[1] - y1)/(y2-y1)
                x = x1 + t * (x2 - x1)
                y = screen_size[1]

            if clip is first_clip:
                new_poly.append((x,y))
                if (x2, y2) not in new_poly:
                    new_poly.append((x2,y2))
                #poly_points[first_index][0] = x
                #poly_points[first_index][1] = y
            else:
                new_poly.append((x,y))
                if (x1, y1) not in new_poly:
                    new_poly.append((x1,y1))
                #poly_points[second_index][0] = x
                #poly_points[second_index][1] = y
    return new_poly
