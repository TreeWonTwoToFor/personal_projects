import math
import pygame

from Engine import Helper
from Engine import ViewFrustum

frustum_planes = None
camera_pos = None

frustum_culling = True 
back_culling = True
lighting = True

def perspective_projection(screen, projected_point, camera):
    screen_resolution = screen.get_size()
    # redefining our list inputs into points/vectors with names that align with wikipedia
    a = projected_point
    c = camera.point
    theta = camera.angle
    # now we need to find the 'd' values, aka a vector that will intersect with the image surface
    # before we find the d values, let's match the variable names on the page
    cx, cy, cz = math.cos(theta[0]), math.cos(theta[1]), math.cos(theta[2])
    sx, sy, sz = math.sin(theta[0]), math.sin(theta[1]), math.sin(theta[2])
    x, y, z = (a[0]-c[0]), (a[1]-c[1]), (a[2]-c[2])
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
    # dz included for depth buffering
    return ((bx+size_x,size_y-by), dz)

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

def draw_polygons(screen, camera, obj_list, light_list, offset=(0,0,0)):
    global frustum_planes
    poly_list = []
    # sorting all of the objects into one list to ensure proper ordering
    for obj in obj_list:
        out_of_bounds = False
        if frustum_culling:
            for i in range(len(frustum_planes)):
                plane = frustum_planes[i]
                if ViewFrustum.aabb_outside_plane(plane, obj.aabb_min, obj.aabb_max):
                    out_of_bounds = True
                    break
        if not out_of_bounds:
            poly_list = obj.model + poly_list
        #for square_full in obj.collision_box:
        #    square = square_full[0]
        #    for i in range(3):
        #        Helper.draw_3d_line(screen, square[i], square[i+1], (255,255,255), camera)
        #    Helper.draw_3d_line(screen, square[3], square[0], (255,255,255), camera)
    poly_list = sort_polygons(camera, poly_list)
    # render polygons, one by one
    for poly in poly_list:
        direction_vector = [
            camera.point[0] - poly[0][0][0],
            camera.point[1] - poly[0][0][1],
            camera.point[2] - poly[0][0][2]]
        # back culling
        if back_culling and Helper.array_dp(direction_vector, poly[1]) < 0:
            continue
        # using face vector to calculate light intensity
        poly_color = list(poly[3])
        if lighting:
            new_color = [0,0,0]
            for light in light_list:
                light_pos = light[0]
                light_str = light[1]
                color_mod = Helper.array_dp(light_pos, poly[1])/Helper.vector_magnitude(light_pos)
                if color_mod < 0: color_mod = 0
                for i in range(3): 
                    new_color[i] = (poly_color[i]*color_mod*(light_str/100)) + new_color[i]
            for i in range(len(new_color)):
                if new_color[i] < 20: new_color[i] = 20
                if new_color[i] > 255: new_color[i] = 255
            poly_color = new_color
        # rendering polygons
        perspective_poly = []
        for point in poly[0]:
            # perspective_projection's 0 index is the xy screen position
            # the 1 index is the distance value, would be used for depth buffering
            perspective_poly.append(perspective_projection(screen, point, camera)[0])
        pygame.draw.polygon(screen, poly_color, perspective_poly)

# 'main' function of Draw
def draw_frame_poly(screen, camera, obj_list, light_list, debug, clock):
    global camera_pos, frustum_planes
    current_camera = ((camera.point[0], camera.point[1], camera.point[2]),
                        (camera.angle[0], camera.angle[1], camera.angle[2]))
    if camera_pos != current_camera:
        frustum_planes = ViewFrustum.get(screen, camera)
        camera_pos = current_camera
    draw_polygons(screen, camera, obj_list[1:], light_list)
    camera.fix_angles() # keeps the camera's angles in realistic boundaries.
    if debug: camera.show_pos(screen, round(clock.get_fps(), 2))
