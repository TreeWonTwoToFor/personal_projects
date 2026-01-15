import math
import time
import numpy
import pygame
from PIL import Image

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
    # FIXME: this is actually black magic, idk how this kinda works, but it shouldn't be here
    ia, ib, ic = 2,0,1
    uv_list = [uv_list[ia], uv_list[ib], uv_list[ic]]
    # checking every pixel in the bounding box
    for i in range(min_y, max_y):
        for j in range(min_x, max_x):
            # will this pixel be behind another object?
            # NOTE: the read is really slow, and we need to check the depth
            #pixel_val = read_pixel_buffer(buffer, ss, (j,i))
            #buffer_depth = int.from_bytes(pixel_val[-1:])
            tri_vals = inside_triangle(points[0], points[1], points[2], (j,i))
            # is the point inside the triangle?
            if tri_vals[0]>=0 and tri_vals[1]>=0 and tri_vals[2]>=0 and tri_vals[3] != 0:
                # use our triangle area to 'blend' the uv weights
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
    # idea: on each scanline, find the 'edge' using the tri_vals, then arithmetically
    #       shift the values of the area as you go across the scanline. Should be
    #       much faster than doing all the dps
    # better idea: that scanline search should be based on binary search
    #       once to find a point inside the tri, and then once on each
    #       side to find the left/right edges. Should be faster than linear

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

# bilinear interpelation
#NOTE: 100% doesn't work lol
def get_color_BI(texture, u, v):
    img_size = texture[0]
    pixel_x = u * img_size[0]
    pixel_y = v * img_size[1]
    # getting the positons of the four nearest pixels
    top_left = (math.floor(pixel_x), math.floor(pixel_y))
    top_right = (math.ceil(pixel_x), math.floor(pixel_y))
    bottom_left = (math.floor(pixel_x), math.ceil(pixel_y))
    bottom_right = (math.ceil(pixel_x), math.ceil(pixel_y))
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
    return final_val

if __name__ == "__main__":
    texture = load_texture("./Assets/Objects/cylinder/checkered_texture.bmp")
    print(texture[1][25, 25])
    print(get_color_NN(texture, 0.25, 0.75)) # should be black
