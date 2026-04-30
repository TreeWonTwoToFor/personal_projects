import sys

from PIL import Image
from Engine import Parser

def draw_line(img, x0, y0, x1, y1, color):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        # draw pixel
        img[x0, y0] = color
        # stop condition
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

# python3 TextureMapper.py object_file sizeX sizeY
file_name = sys.argv[1]
match len(sys.argv):
    case 2: size = (1000, 1000)
    case 3: size = (int(sys.argv[2]), int(sys.argv[2]))
    case 4: size = (int(sys.argv[2]), int(sys.argv[3]))

# load in the file data about the object
file = Parser.read_blender_file(file_name)
file_dict = Parser.get_file_dictionary(file)
file_list = Parser.file_dict_to_list(file_dict)
uv_list = file_list[2]
face_list = file_list[3]

# create an image to draw into for our fnial output
img = Image.new('RGB', size, color=(0,0,0))
pixel_map = img.load()

# now that we have the data, we want to try and draw lines between the uv points
for face in face_list:
    # get the UV values for each point in the face
    uv_index_list = []
    for point in face:
        uv_index_list.append(point[1])
    uv_face_list = []
    for uv_index in uv_index_list:
        uv_face_list.append(uv_list[int(uv_index)-1])
    # now we want to get all of the pixel values for each uv point.
    pixel_list = []
    for uv in uv_face_list:
        x = uv[0] * (size[0]-1)
        y = (1-uv[1]) * (size[1]-1)
        pixel_list.append((x,y))
    # draw a line between each pair of pixels
    for i in range(len(pixel_list)):
        pixelA = pixel_list[i]
        if i+1 == len(pixel_list):
            pixelB = pixel_list[0]
        else:
            pixelB = pixel_list[i+1]
        draw_line(pixel_map, int(pixelA[0]), int(pixelA[1]), int(pixelB[0]), int(pixelB[1]), (255,255,255))

# save that output
img.save("test_texture.bmp", "BMP")
