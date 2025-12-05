import math

from Engine import Object
from Engine import Camera
from Engine import Parser

def load_scene(scene_name):
    game_camera = None
    object_dict = {}
    with open(scene_name, "r") as file:
        content = file.read()
        content_lines = content.split("\n")
        for line in content_lines:
            if len(line) > 0 and line[0] != "/":
                line_tokens = line.split(' ')
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
                        game_camera = Camera.Camera((v_list[0],v_list[1],v_list[2]), 
                                                    (v_list[3],v_list[4],v_list[5]))
                        object_dict["camera bounding box"] = game_camera.bounding_box
                    case "open":
                        rgb = (int(line_tokens[3]),int(line_tokens[4]),int(line_tokens[5]))
                        this_obj = Object.Object(
                            (Parser.get_model("./Assets/Objects/" + line_tokens[2] + ".obj")), rgb)
                        object_dict[line_tokens[1]] = this_obj
                    case "translate" | "scale":
                        object_name = line_tokens[1]
                        this_obj = object_dict[object_name]
                        x,y,z = float(line_tokens[2]), float(line_tokens[3]), float(line_tokens[4])
                        if line_tokens[0] == 'translate':
                            this_obj.translate(x,y,z)
                        elif line_tokens[0] == 'scale':
                            x,y,z = math.sqrt(math.sqrt(x)), math.sqrt(math.sqrt(y)), math.sqrt(math.sqrt(z))
                            this_obj.scale(x,y,z)
                    case "rotate":
                        object_name = line_tokens[1]
                        this_obj = object_dict[object_name]
                        x,y,z = float(line_tokens[2]), float(line_tokens[3]), float(line_tokens[4])
                        theta = float(line_tokens[5]) * (math.pi/180) # radians to degrees
                        this_obj.rotate(x,y,z,theta)
    return [game_camera, object_dict]
        
if __name__ == '__main__':
    print(load_scene("test_scene.txt"))
