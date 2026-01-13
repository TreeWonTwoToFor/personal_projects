import math
import time
import numpy
import pygame

def dp(vector_a, vector_b):
    return vector_a[0]*vector_b[0] + vector_a[1]*vector_b[1]

def right_angle(vector):
    return (vector[1], -vector[0])

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

def read_pixel_buffer(screen, pixel_pos):
    buffer = screen.get_buffer()
    ss = screen.get_size()
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

def draw_polygon(screen, points, color, fill=False):
    buffer = screen.get_buffer()
    ss = screen.get_size()
    # getting bounds of polygon
    min_x, max_x = points[0][0], points[0][0]
    min_y, max_y = points[0][1], points[0][1]
    for point in points:
        if point[0] < min_x: min_x = point[0]
        if point[0] > max_x: max_x = point[0]
        if point[1] < min_y: min_y = point[1]
        if point[1] > max_y: max_y = point[1]
    # getting uv values per point
    uv_list = [(0,0), (1,1), (0.5, 0.5)] # shouldn't be hardcoded
    # scan line based filling
    ab = (points[0][0]-points[1][0], points[0][1]-points[1][1])
    ac = (points[0][0]-points[2][0], points[0][1]-points[2][1])
    triangle_area = math.fabs(dp(ab, right_angle(ac)))/2
    for i in range(min_y, max_y):
        for j in range(min_x, max_x):
            pixel_val = read_pixel_buffer(screen, (j,i))
            tri_vals = inside_triangle(points[0], points[1], points[2], (j,i))
            if tri_vals[0]>0 and tri_vals[1]>0 and tri_vals[2]>0:
                r = int(tri_vals[0]/triangle_area*255)
                g = int(tri_vals[1]/triangle_area*255)
                b = int(tri_vals[2]/triangle_area*255)
                write_pixel_buffer(buffer, ss, (j,i), [r,g,b])

def load_texture(file_name):
    # use PIL to load and read image
    print("")

def get_color(image, u, v):
    img_size = (800, 600) # should actually be read from the image
    pixel_x = u * img_size[0]
    pixel_y = v * img_size[1]
    print(pixel_x, pixel_y)
    # getting the positons of the four nearest pixels
    top_left = (math.floor(pixel_x), math.floor(pixel_y))
    top_right = (math.ceil(pixel_x), math.floor(pixel_y))
    bottom_left = (math.floor(pixel_x), math.ceil(pixel_y))
    bottom_right = (math.ceil(pixel_x), math.ceil(pixel_y))
    print(top_left, top_right, bottom_left, bottom_right)
    # average out the values
    # also should be read from the image
    tl_val = (0,0,0)
    tr_val = (255,0,0)
    bl_val = (0,0,255)
    br_val = (255,255,255)
    # performing bilinear interpolation
    horizontal_weight = pixel_x % 1
    vertical_weight = pixel_y % 1
    top_val = [0,0,0]
    for i in range(3):
        top_val[i] = (tl_val[i] * (1-horizontal_weight)) + (tr_val[i] * (horizontal_weight))
    bottom_val = [0,0,0]
    for i in range(3):
        bottom_val[i] = (bl_val[i] * (1-horizontal_weight)) + (br_val[i] * (horizontal_weight))
    final_val = [0,0,0]
    for i in range(3):
        final_val[i] = round((top_val[i] * (1-vertical_weight)) + (bottom_val[i] * vertical_weight), 4)
    print(final_val)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((200,200))
    start = time.time()
    draw_polygon(screen, ((20, 20), (100, 100), (180,30)), (255,255,255))
    draw_polygon(screen, ((100, 100), (160, 180), (180,30)), (255,255,0))
    draw_polygon(screen, ((20, 180), (100, 180), (20, 60)), (255,0,255))
    print(time.time() - start)
    #load_texture("./Assets/Objects/cube/rubiks_texture.png")
    #get_color("blah", 0.123478, 0.4398)
    pygame.display.update()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
