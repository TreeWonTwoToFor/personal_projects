import math

from Engine import Object
from Engine import Camera
from Engine import Parser

asset_path = "./Assets/"
scene_path = asset_path + "Scenes/"
object_path = asset_path + "Objects/"

# True  - reads the object based on the name given in the scene.
# False - Will simply take the name of the obj, and use that to look up a texture
read_texture_by_name = True
scenes_with_obj_textures = ["rubiks_cube.rsc"]

def load_scene(scene_name):
    global read_texture_by_name
    if scene_name.split(".")[-1] != "rsc":
        raise ValueError(f"Scene file {scene_name}")
    if scene_name in (scene_path + x for x in scenes_with_obj_textures):
        read_texture_by_name = False
    game_camera = None
    object_dict = {}
    game_actions = []
    light_list = []
    background_color = None
    setup = True
    with open(scene_name, "r") as file:
        content = file.read()
        content_lines = content.split("\n")
    for line in content_lines:
        line_tokens = line.split(' ')
        bad_tokens = []
        for token in line_tokens:
            if token == '': bad_tokens.insert(0, line_tokens.index(token))
        for token_index in bad_tokens:
            line_tokens.pop(token_index)
        if len(line) > 0 and line[0] != "/":
            if setup:
                match line_tokens[0]:
                    case "camera":
                        v_list = []
                        for i in range(1,7):
                            try:
                                v_list.append(float(line_tokens[i]))
                            except:
                                raise ValueError(f"Item at index {i} is problematic")
                        if len(v_list) != 6:
                            raise ValueError("value list is not the right length")
                        game_camera = Camera.Camera(v_list[0:3], v_list[3:6])
                    case "light":
                        light_pos = tuple(float(x) for x in line_tokens[1:4])
                        light_str = float(line_tokens[4])
                        light_list.append((light_pos, light_str))
                    case "open":
                        # index 1: name
                        # index 2: model file path
                        # index 3: texture file path
                        number_of_tokens = len(line_tokens) - 1
                        object_name = line_tokens[1]
                        match number_of_tokens:
                            case 1:
                                # no file paths specified, defaults to the name of the object
                                model_path = object_path + object_name + '/' + object_name + ".obj"
                                texture_path = object_path + object_name + '/' + object_name + ".bmp"
                            case 2:
                                # only model is given, so we guess the texture is the same with .bmp file extension
                                model_path = object_path + line_tokens[2]
                                texture_path = object_path + line_tokens[2][:-4] + ".bmp"
                            case 3:
                                # we have all info, so there's no issues
                                model_path = object_path + line_tokens[2]
                                texture_path = object_path + line_tokens[3]
                        if model_path[-4:] != ".obj":
                            raise ValueError(f"The scene {scene_name} can't read the object '{model_path}'\n{line}")
                        if texture_path[-4:] != ".bmp":
                            raise ValueError(f"The scene {scene_name} can't read the texture '{texture_path}'")
                        model = Parser.get_model(model_path)
                        this_obj = Object.Object(model, texture_path)
                        object_dict[line_tokens[1]] = this_obj
                    case "translate" | "scale":
                        object_name = line_tokens[1]
                        this_obj = object_dict[object_name]
                        x,y,z = float(line_tokens[2]), float(line_tokens[3]), float(line_tokens[4])
                        if line_tokens[0] == 'translate':
                            this_obj.translate([x,y,z])
                        elif line_tokens[0] == 'scale':
                            x,y,z = math.sqrt(math.sqrt(x)), math.sqrt(math.sqrt(y)), math.sqrt(math.sqrt(z))
                            this_obj.scale([x,y,z])
                    case "rotate":
                        object_name = line_tokens[1]
                        this_obj = object_dict[object_name]
                        x,y,z = float(line_tokens[2]), float(line_tokens[3]), float(line_tokens[4])
                        theta = float(line_tokens[5]) * (math.pi/180) # degrees to radians
                        this_obj.rotate([x,y,z],theta)
                    case "orbit":
                        object_name = line_tokens[1]
                        this_obj = object_dict[object_name]
                        # xyz = [float(line_tokens[2]), float(line_tokens[3]), float(line_tokens[4])]
                        xyz = list(float(x) for x in line_tokens[2:5])
                        theta = float(line_tokens[5]) * (math.pi/180) # degrees to radians
                        oxyz = [0,0,0]
                        if len(line_tokens) > 6:
                            oxyz = [float(line_tokens[6]), float(line_tokens[7]), float(line_tokens[8])]
                        this_obj.orbit(xyz, theta, oxyz)
                    case "#":
                        # allows for scene actions to start
                        setup = False 
                    case "background":
                        background_color = [float(line_tokens[1]), 
                                float(line_tokens[2]), float(line_tokens[3])]
            else:
                action_type = line_tokens[0]
                action_object = object_dict[line_tokens[1]]
                xyz = [float(line_tokens[2]), float(line_tokens[3]), float(line_tokens[4])]
                theta = None
                oxyz = [0,0,0]
                if action_type == "rotate":
                    theta = float(line_tokens[5]) * (math.pi/180) # degrees to radians
                elif action_type == "orbit":
                    if len(line_tokens) > 6:
                        oxyz = [float(line_tokens[6]), float(line_tokens[7]), float(line_tokens[8])]
                    theta = float(line_tokens[5]) * (math.pi/180) # degrees to radians
                game_actions.append((action_type, action_object, xyz, theta, oxyz))
    if game_camera == None:
        game_camera = Camera.Camera([0,0,0], [0,0,0])
    if background_color == None: 
        background_color = [0,0,0]
    if len(light_list) == 0: 
        light_list.append(((100, 80, 90), 100))
    return [game_camera, object_dict, game_actions, background_color, light_list]
        
if __name__ == '__main__':
    print(load_scene("test_scene.rsc"))
