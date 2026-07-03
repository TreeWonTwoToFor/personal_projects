from ..Logic import FlappyBird
from ..Logic import RubiksCube
from ..Logic import StandardMovement

FPS = 5
resolution = (800, 600)
debug = True
# normal, render, testing
mode = "normal"
scene_name = "test_scene.rsc"
local_file_path = "."
frame_count = 1000
mouse_control = False
mouse_sensitivity = 0.5

def get_settings():
    return [FPS, resolution, debug, mode, scene_name, frame_count, mouse_control, mouse_sensitivity, local_file_path]

GameFile = StandardMovement

match scene_name:
    case "flappy_bird.rsc": GameFile = FlappyBird
    case "rubiks_cube.rsc": GameFile = RubiksCube
