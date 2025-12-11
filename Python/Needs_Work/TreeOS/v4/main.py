# General libraries
import pygame
import os
import random

# Testing
import cProfile
import pstats

# Project files
from Engine import Draw
from Engine import SceneManager
from Engine import PlayerMovement
from Engine import FlappyBird

FPS = 60
resolution = (800, 600) # XGA
debug = True
# normal, render, testing
mode = "normal"
scene_name = "test_scene.txt"
frame_count = 100

mouse_control = False
mouse_sensitivity = 0.5

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
pygame.mouse.set_visible(not mouse_control)

scene = SceneManager.load_scene("./Assets/Scenes/" + scene_name)
game_camera = scene[0]
object_dict = scene[1]
scene_actions = scene[2]
background_color = scene[3]

def iterate():
    global running

    # scene specific code
    game_function = PlayerMovement.player_movement
    update_function = PlayerMovement.player_movement_update
    if scene_name == "flappy_bird.txt":
        game_function = FlappyBird.player_movement
        update_function = FlappyBird.player_movement_update
    
    # object update
    for action in scene_actions:
        match action[0]:
            case "translate": action[1].translate(action[2])
            case "scale": action[1].scale(action[2])
            case "rotate": action[1].rotate(action[2], action[3])
    object_list = list(object_dict.values())
    # specific game logic
    if scene_name == "flappy_bird.txt":
        pipes = object_list[2:]
        for i in range(len(pipes)-1):
            bottom = pipes[i]
            top = pipes[i+1]
            if bottom.center_point[0] > 10:
                bottom.move_to_origin()
                top.move_to_origin()
                height = (random.random()-0.5)* 4
                bottom.translate((-16,-5.5 + height,0))
                top.translate((-16,5.5 + height,0))

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
    clock.tick(FPS)

match mode:
    case "normal":
        running = True
        while running:
            iterate()
    case "testing":
        with cProfile.Profile() as pr:
            for i in range(frame_count):
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
