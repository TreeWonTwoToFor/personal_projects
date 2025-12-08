# General libraries
import pygame

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

mouse_control = False
mouse_sensitivity = 0.5

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
pygame.mouse.set_visible(not mouse_control)

scene = SceneManager.load_scene("./Assets/Scenes/farlands_solar_system.txt")
game_camera = scene[0]
object_dict = scene[1]

def iterate():
    global running
    screen.fill([0,0,0])
    #object_dict["red"].rotate(1,0,0, 0.005)
    #object_dict["green"].rotate(0,1,0, 0.005)
    #object_dict["blue"].rotate(0,0,1, 0.005)
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
    case "render":
        running = True
        for i in range(615):
            if running:
                iterate()
                number = f"{i:03}" # 3 = digits
                pygame.image.save(screen, "render/frame" + number + ".png")
    case "normal":
        running = True
        while running:
            iterate()
    case "testing":
        with cProfile.Profile() as pr:
            iterate()
        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.CALLS).print_stats(200)
