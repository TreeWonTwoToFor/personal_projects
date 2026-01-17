import math
import pygame
from PIL import Image

edge_search = True

def dp(vector_a, vector_b):
    return vector_a[0]*vector_b[0] + vector_a[1]*vector_b[1]

def right_angle(vector):
    return (-vector[1], vector[0])

def inside_triangle(a, b, c, p):
    # abc define a triangle, while p is a point
    ab = (b[0]-a[0], b[1]-a[1])
    bc = (c[0]-b[0], c[1]-b[1])
    ca = (a[0]-c[0], a[1]-c[1])

    ab_r = right_angle(ab)
    bc_r = right_angle(bc)
    ca_r = right_angle(ca)

    ap = (p[0]-a[0], p[1]-a[1])
    bp = (p[0]-b[0], p[1]-b[1])
    cp = (p[0]-c[0], p[1]-c[1])

    right_ab = dp(ab_r, ap)/2
    right_bc = dp(bc_r, bp)/2
    right_ca = dp(ca_r, cp)/2

    area = math.fabs(dp(ab, right_angle(bc)))/2
    return (right_ab, right_bc, right_ca, area)

def check_inside_triangle(inside_triangle_values):
    tri_vals = inside_triangle_values
    return tri_vals[0]>=0 and tri_vals[1]>=0 and tri_vals[2]>=0 and tri_vals[3] != 0

def find_edges(points, scanline_height):
    min_x, max_x = points[0][0], points[0][0]
    for point in points:
        if point[0] < min_x: min_x = point[0]
        if point[0] > max_x: max_x = point[0]
    # line intersection based approach
    intersections = []
    point_pairs = [(points[0], points[1]), (points[2], points[1]), (points[2], points[0])]
    for pair in point_pairs:
        y0 = scanline_height
        x1, y1 = pair[0][0], pair[0][1]
        x2, y2 = pair[1][0], pair[1][1]
        if (y1 <= y0 < y2) or (y2 <= y0 < y1):
            try:
                t = (y0 - y1) / (y2 - y1)
            except:
                continue
            x = x1 + t * (x2 - x1)
            if x >= min_x-1 and x <= max_x: intersections.append(x)
    left, right = int(min(intersections))+1, int(max(intersections))+1
    tri_1 = inside_triangle(points[0], points[1], points[2], (left, scanline_height))
    tri_2 = inside_triangle(points[0], points[1], points[2], (left+1, scanline_height))
    return(left, right, tri_1, (tri_1[0]-tri_2[0], tri_1[1]-tri_2[1], tri_1[2]-tri_2[2]))

def read_pixel_buffer(buffer, ss, pixel_pos):
    buffer_offset = (pixel_pos[0] + pixel_pos[1] * ss[0]) * 4
    return buffer.raw[buffer_offset:buffer_offset+4]

def write_pixel_buffer(buffer, screen_size, pixel_pos, pixel_color, extra_byte=0):
    ss = screen_size
    buffer_offset = (pixel_pos[0] + pixel_pos[1] * ss[0]) * 4
    # coded to RGB instead of BGR
    byte_color = bytes([pixel_color[2], pixel_color[1], pixel_color[0], extra_byte])
    try:
        buffer.write(byte_color, buffer_offset)
    except IndexError:
        raise IndexError(f"Bad buffer offset: buffer_offset -> {buffer_offset}, max_offset -> {ss[0]*ss[1]*4}")

def draw_polygon(screen, points, texture, light_val):
    buffer = screen.get_buffer()
    ss = screen.get_size()
    # getting bounds of polygon + uv values
    uv_list = []
    min_x, max_x = points[0][0], points[0][0]
    min_y, max_y = points[0][1], points[0][1]
    for point in points:
        uv_list.append([point[3], point[4]])
        if point[0] < min_x: min_x = point[0]
        if point[0] > max_x: max_x = point[0]
        if point[1] < min_y: min_y = point[1]
        if point[1] > max_y: max_y = point[1]
    # NOTE: this is actually black magic, idk how this works
    ia, ib, ic = 2,0,1
    uv_list = [uv_list[ia], uv_list[ib], uv_list[ic]]
    # checking every pixel in the bounding box
    for i in range(min_y, max_y):
        if i < 0 or i >= ss[1]: continue # prevent buffer overflow
        edges_and_area_change = find_edges(points, i)
        if edges_and_area_change == None: continue
        left_edge = edges_and_area_change[0]
        right_edge = edges_and_area_change[1]
        tri_vals = list(edges_and_area_change[2])
        deltas = edges_and_area_change[3]
        #tri_vals = list(inside_triangle(points[0], points[1], points[2], (left_edge,i)))
        if tri_vals[0] < 0 or tri_vals[1] < 0 or tri_vals[2] < 0 or tri_vals[3] == 0:
            continue
        # removing the +1 actually makes a decent view of the individual polygons
        for j in range(left_edge, right_edge):
            if j < 0 or j >= ss[0]: continue # prevent buffer overflow
            final_uv = [0,0]
            for k in range(3):
                area_mod = tri_vals[k]/tri_vals[-1]
                for l in range(2):
                    final_uv[l] += uv_list[k][l] * area_mod
            # pull that new uv color from our texture, and write it to the buffer
            color = list(get_color_NN(texture, final_uv[0], final_uv[1]))
            for k in range(len(color)):
                color[k] = int(color[k] * light_val)
            write_pixel_buffer(buffer, ss, (j,i), color)
            # update the area of the triangles for uv blending
            for k in range(3):
                tri_vals[k] -= deltas[k]

def load_texture(file_name):
    img = Image.open(file_name)
    return (img.size, img.load())

# nearest neighbor
def get_color_NN(texture, u,v):
    img_size = texture[0]
    # subtraction needed for index error if uv = 1
    pixel_x = round(u * (img_size[0]-1))
    pixel_y = round((1-v) * (img_size[1]-1)) #bottom left origin
    color_val = texture[1][pixel_x, pixel_y]
    return color_val

if __name__ == "__main__":
    triangle = [(20,20,0,0,0), (100, 25, 0,0,0), (50, 50,0,0,0)]
    texture = load_texture("./Assets/Objects/cylinder/red_texture.bmp")
    pygame.init()
    screen = pygame.display.set_mode((200, 200))
    draw_polygon(screen, triangle, texture, 1)
    print(find_edges(triangle, 40))
    pygame.display.update()
    while True:
        continue
