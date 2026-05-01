from Logic import FlappyBird
from Logic import RubiksCube
from Logic import StandardMovement

FPS = 120
resolution = (800, 600)
debug = False
# normal, render, testing
mode = "normal"
scene_name = "rubiks_cube.txt"
frame_count = 100
mouse_control = True
mouse_sensitivity = 0.5

def get_settings():
    return [FPS, resolution, debug, mode, scene_name, frame_count, mouse_control, mouse_sensitivity]

GameFile = StandardMovement

match scene_name:
    case "flappy_bird.txt": GameFile = FlappyBird
    case "rubiks_cube.txt": GameFile = RubiksCube