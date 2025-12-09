# General libraries
import pygame
import os

# Testing
import cProfile
import pstats

# Project files
from Engine import Draw
from Engine import PlayerMovement
from Engine import SceneManager

FPS = 60
resolution = (800, 600) # XGA
debug = True
# normal, render, testing
mode = "normal"
scene_name = "test_scene.txt"
render_frame_count = 630

mouse_control = False
mouse_sensitivity = 0.5

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
pygame.mouse.set_visible(not mouse_control)

scene = SceneManager.load_scene("./Assets/Scenes/" + scene_name)
game_camera = scene[0]
object_dict = scene[1]
object_actions = scene[2]

def iterate():
    global running
    screen.fill([0,0,0])
    for action in object_actions:
        match action[0]:
            case "translate":
                action[1].translate(action[2][0], action[2][1], action[2][2])
            case "scale":
                action[1].scale(action[2][0], action[2][1], action[2][2])
            case "rotate":
                action[1].rotate(action[2][0], action[2][1], action[2][2], action[3])
    object_list = list(object_dict.values())
    Draw.draw_frame_poly(screen, game_camera, object_list, debug, clock)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or PlayerMovement.player_movement(
                event, mouse_control):
            # this is a little unintuitive, but since PlayerMovment
            #   handles the escape key, it returns True when ESC
            #   is pressed. It updates the keyboard when called.
            running = False
    # the player movement needs to be checked every frame, and not just when a key changes.
    PlayerMovement.player_movement_update(
        game_camera, mouse_control, mouse_sensitivity, object_list)
    clock.tick(FPS)

match mode:
    case "normal":
        running = True
        while running:
            iterate()
    case "testing":
        with cProfile.Profile() as pr:
            iterate()
        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.CALLS).print_stats(200)
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
        for i in range(render_frame_count):
            if running:
                iterate()
                number = f"{i:03}" # 3 = digits
                pygame.image.save(screen, "render/frame" + number + ".png")
