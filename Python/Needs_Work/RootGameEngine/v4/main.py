# General libraries
import pygame
import os
import math

# Testing
import cProfile
import pstats

# Project files
from Engine import Draw
from Engine import SceneManager
from Engine import LaunchSettings

# pull the general settings
settings = LaunchSettings.get_settings()
FPS               = settings[0]
resolution        = settings[1]
debug             = settings[2]
mode              = settings[3]
scene_name        = settings[4]
frame_count       = settings[5]
mouse_control     = settings[6]
mouse_sensitivity = settings[7]

# title the pygame window
clean_title = ""
split_title = scene_name.split('.')[0].split('_')
for token in split_title:
    clean_title += token.capitalize() + " "
clean_title = clean_title.strip()
pygame.display.set_caption(clean_title)

# initialize some key components
screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
depth_buffer = []
clock = pygame.time.Clock()
pygame.event.set_grab(mouse_control)
pygame.mouse.set_visible(not mouse_control)

# load in the scene
scene = SceneManager.load_scene("./Assets/Scenes/" + scene_name)
game_camera      = scene[0]
object_dict      = scene[1]
scene_actions    = scene[2]
background_color = scene[3]
light_sources    = scene[4]
dt = 0.016 # presumes 60 FPS, but gets recalculated every frame

# one time run operations
if scene_name == "rubiks_cube.txt":
    Draw.lighting = False # makes the colors more vibrant
    LaunchSettings.GameFile.scramble(list(object_dict.values()))

def iterate():
    global running, dt

    # scene specific code
    GameFile = LaunchSettings.GameFile
    game_logic      = GameFile.game_logic
    game_function   = GameFile.player_movement
    update_function = GameFile.player_movement_update

    # object update
    for action in scene_actions:
        match action[0]:
            case "translate": action[1].translate([val*dt for val in action[2]])
            case "scale": action[1].scale([val*dt for val in action[2]])
            case "rotate": action[1].rotate(action[2], action[3] * dt)
            case "orbit": action[1].orbit(action[2], action[3] * dt, action[4])
    object_list = list(object_dict.values())
    game_logic(object_list)

    # visual/game update
    screen.fill(background_color)
    depth_buffer = [math.inf] * (screen.get_width() * screen.get_height())
    Draw.draw_frame_poly(screen, depth_buffer, game_camera, object_list, light_sources, debug, clock)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or game_function(event):
            # this is a little unintuitive, but since game_function
            #   handles the escape key, it returns True when ESC
            #   is pressed. It updates the keyboard when called.
            running = False
    # the player movement needs to be checked every frame, and not just when a key changes.
    update_function(game_camera, mouse_control, mouse_sensitivity, object_list, dt)
    # delay if necessary
    dt = round(clock.tick(FPS) * 0.001, 4)

match mode:
    case "normal":
        running = True
        while running:
            iterate()
    case "testing":
        with cProfile.Profile() as pr:
            running = True
            for i in range(frame_count):
                if running:
                    iterate()
        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME).print_stats(10)
    case "render":
        # creates an empty folder, named 'render'
        current_path = os.getcwd()
        render_path = current_path + "/render/"
        if not os.path.isdir(render_path):
            os.mkdir(render_path)
        else:
            for file in os.listdir(render_path):
                file_path = os.path.join(render_path, file)
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                    except OSError as e:
                        print(f"Error removing {file_path}: {e}")
        # iterates for the given number of frames, saving each frame as a file.
        debug = False # ensures that only the world is being drawn
        running = True
        frame_digits = len(str(frame_count))
        for i in range(frame_count):
            if running:
                iterate()
                dt = 0.016 # forces 60 FPS for rendering
                number = f"{i:0{frame_digits}}"
                pygame.image.save(screen, "render/frame" + number + ".png")
