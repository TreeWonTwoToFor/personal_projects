import sys

from PIL import Image
from Engine import Parser

# python3 TextureMapper.py object_file sizeX sizeY
file_name = sys.argv[1]
if len(sys.argv) == 3: size = (int(sys.argv[2]), int(sys.argv[2]))
elif len(sys.argv) == 4: size = (int(sys.argv[2]), int(sys.argv[3]))
file = Parser.read_blender_file(file_name)
file_dict = Parser.get_file_dictionary(file)
file_list = Parser.file_dict_to_list(file_dict)
uv_list = file_list[2]
img = Image.new('RGB', size, color=(0,0,0))
pixel_map = img.load()
for uv in uv_list:
    x = uv[0] * (size[0]-1)
    y = (1-uv[1]) * (size[1]-1)
    pixel_map[x,y] = (255,255,255)
img.save("test_texture.bmp", "BMP")
