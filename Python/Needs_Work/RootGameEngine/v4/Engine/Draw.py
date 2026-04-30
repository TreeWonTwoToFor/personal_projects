import math
import pygame

from Engine import Helper
from Engine import ViewFrustum
from Engine import Rasterizer

frustum_planes = None
camera_pos = None

frustum_culling = True
back_culling = True
lighting = True
homemade_rasterizer = True

def draw_polygons(screen, depth_buffer, camera, obj_list, light_list):
    global frustum_planes
    culled_obj_list = []
    # sorting all of the objects into one list to ensure proper ordering
    for obj in obj_list:
        out_of_bounds = False
        if frustum_culling:
            for plane in frustum_planes:
                if ViewFrustum.aabb_outside_plane(plane, obj.aabb_min, obj.aabb_max):
                    out_of_bounds = True
                    break
        if not out_of_bounds:
            culled_obj_list.append(obj)
    for obj in culled_obj_list:
        for poly in obj.model:
            direction_vector = [
                camera.point[0] - poly[0][0][0],
                camera.point[1] - poly[0][0][1],
                camera.point[2] - poly[0][0][2]]
            # back culling
            if back_culling and Helper.array_dp(direction_vector, poly[1]) < 0:
                continue
            if lighting:
                light_value = 0
                for light in light_list:
                    light_pos = light[0]
                    light_str = light[1]
                    color_mod = Helper.array_dp(light_pos, poly[1])/Helper.vector_magnitude(light_pos)
                    if color_mod < 0: color_mod = 0
                    light_value += (color_mod*(light_str/100))
                if light_value < 0.2: light_value = 0.2
            else:
                light_value = 1
            # rendering polygons
            if homemade_rasterizer:
                perspective_poly = []
                uv_values = poly[2]
                for i in range(len(poly[0])):
                    point = poly[0][i]
                    # perspective_projection's 0 index is the xy screen position
                    # the 1 index is the distance value, would be used for depth buffering
                    projected_point = Helper.perspective_projection(screen, point, camera)
                    screen_pos = projected_point[0]
                    depth = projected_point[1]
                    perspective_poly.append([int(screen_pos[0]), int(screen_pos[1]), depth] + uv_values[i])
                Rasterizer.draw_polygon(screen, depth_buffer, perspective_poly, obj.texture, light_value)
            else:
                base_color = [255, 255, 255]
                lit_color = [x * light_value for x in base_color]
                perspective_poly = []
                for point in poly[0]:
                    # perspective_projection's 0 index is the xy screen position
                    # the 1 index is the distance value, would be used for depth buffering
                    perspective_poly.append(Helper.perspective_projection(screen, point, camera)[0])
                pygame.draw.polygon(screen, lit_color, perspective_poly)

# 'main' function of Draw
def draw_frame_poly(screen, depth_buffer, camera, obj_list, light_list, debug, clock):
    global camera_pos, frustum_planes
    current_camera = ((camera.point[0], camera.point[1], camera.point[2]),
                        (camera.angle[0], camera.angle[1], camera.angle[2]))
    if camera_pos != current_camera:
        frustum_planes = ViewFrustum.get(screen, camera)
        camera_pos = current_camera
    draw_polygons(screen, depth_buffer, camera, obj_list[1:], light_list)
    camera.fix_angles() # keeps the camera's angles in realistic boundaries.
    if debug: camera.show_pos(screen, round(clock.get_fps(), 2))
