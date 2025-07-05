# General libraries
import pygame

# Project files
import Camera
import Draw
import PlayerMovement
import blender_parser as Parser

FPS = 60
resolution = (600,600)
debug = True
model_file = "./blender_files/monkey.obj"

mouse_control = False
mouse_sensitivity = 1

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
pygame.mouse.set_visible(not mouse_control)

model = Parser.get_model(model_file)

# pos + angle is simply to highlight the current drawing setup.
# use Camera.degrees_to_radians() for angles
game_camera = Camera.Camera((0,0,5), (0, Camera.degrees_to_radians(180), 0))

running = True
while running:
    Draw.draw_frame(screen, game_camera, model, debug)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or PlayerMovement.player_movement(event, mouse_control):
            # this is a little unintuitive, but since PlayerMovment
            #   handles the escape key, it returns True when ESC
            #   is pressed. It updates the keyboard when called.
            running = False
    # the player movement needs to be checked every frame, and not just when a key changes.
    PlayerMovement.player_movement_update(game_camera, mouse_control, mouse_sensitivity)
    clock.tick(FPS)
