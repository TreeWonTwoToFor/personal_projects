# General libraries
import pygame
import os

# Testing
import cProfile
import pstats

# Project files
from Engine import LaunchSettings
from Engine import SceneManager
from Engine import PlayerMovement
from Engine import FlappyBird
from Engine import Draw

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

# initialize some key components
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
pygame.mouse.set_visible(not mouse_control)

# load in the scene
scene = SceneManager.load_scene("./Assets/Scenes/" + scene_name)
game_camera      = scene[0]
object_dict      = scene[1]
scene_actions    = scene[2]
background_color = scene[3]
dt = 0.016

def iterate():
    global running, dt

    # scene specific code
    GameFile = PlayerMovement
    if scene_name == "flappy_bird.txt":
        GameFile = FlappyBird
    game_logic      = GameFile.game_logic
    game_function   = GameFile.player_movement
    update_function = GameFile.player_movement_update
    
    # object update
    for action in scene_actions:
        match action[0]:
            case "translate": action[1].translate([val*dt for val in action[2]])
            case "scale": action[1].scale([val*dt for val in action[2]])
            case "rotate": action[1].rotate(action[2], action[3] * dt)
    object_list = list(object_dict.values())
    game_logic(object_list)

    # visual/game update
    screen.fill(background_color)
    Draw.draw_frame_poly(screen, game_camera, object_list, debug, clock)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or game_function(event, mouse_control):
            # this is a little unintuitive, but since game_function
            #   handles the escape key, it returns True when ESC
            #   is pressed. It updates the keyboard when called.
            running = False
    # the player movement needs to be checked every frame, and not just when a key changes.
    update_function(game_camera, mouse_control, mouse_sensitivity, object_list)
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
        # creates an empty folder, named render
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
        debug = False
        running = True
        for i in range(frame_count):
            if running:
                iterate()
                number = f"{i:03}" # 3 = digits
                pygame.image.save(screen, "render/frame" + number + ".png")
