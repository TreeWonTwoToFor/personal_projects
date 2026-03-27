import pygame
from PIL import Image

# buffer based functions
def read_pixel_buffer(buffer, ss, pixel_pos):
    # this function is really slow for some reason. string manip?
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

# drawing functions
def make_edge(point1, point2):
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]
    A = y2 - y1
    B = -(x2 - x1)
    C = x2*y1 - y2*x1
    return A, B, C

def eval_edge(edge, x, y):
    A, B, C = edge
    return A*x + B*y + C

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

    e0 = make_edge(points[1], points[2])
    e1 = make_edge(points[2], points[0])
    e2 = make_edge(points[0], points[1])

    E0_row = eval_edge(e0, min_x, min_y)
    E1_row = eval_edge(e1, min_x, min_y)
    E2_row = eval_edge(e2, min_x, min_y)

    # checking every pixel in the bounding box
    for i in range(min_y, max_y):
        if i < 0 or i >= ss[1]: continue # prevent buffer overflow
        E0 = E0_row
        E1 = E1_row
        E2 = E2_row
        # creating + filling the buffer for the scanline
        for j in range(min_x, max_x):
            if j < 0 or j >= ss[0]: continue # prevent buffer overflow
            if E0 <= 0 and E1 <= 0 and E2 <= 0:
                color = [255,255,255]
                for k in range(len(color)):
                    color[k] = int(color[k] * light_val)
                write_pixel_buffer(buffer, ss, (j,i), color)
            E0 += e0[0]; E1 += e1[0]; E2 += e2[0]
        E0_row += e0[1]; E1_row += e1[1]; E2_row += e2[1]

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
    pygame.display.update()
    while True:
        continue
