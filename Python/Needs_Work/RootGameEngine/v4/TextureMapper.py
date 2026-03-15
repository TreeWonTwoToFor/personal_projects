import sys
import random

from PIL import Image
from Engine import Parser

# python3 TextureMapper.py object_file sizeX sizeY
file_name = sys.argv[1]
if len(sys.argv) == 3: size = (int(sys.argv[2]), int(sys.argv[2]))
elif len(sys.argv) == 4: size = (int(sys.argv[2]), int(sys.argv[3]))

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
    uv_index_list = []
    for point in face:
        uv_index_list.append(point[1])
    uv_face_list = []
    for uv_index in uv_index_list:
        uv_face_list.append(uv_list[int(uv_index)-1])
    color = random.randint(150, 255)
    for uv in uv_face_list:
        x = uv[0] * (size[0]-1)
        y = (1-uv[1]) * (size[1]-1)
        pixel_map[x,y] = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))

# save that output
img.save("test_texture.bmp", "BMP")
