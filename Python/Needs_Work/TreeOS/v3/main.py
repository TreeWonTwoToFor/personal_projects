# General libraries
import pygame

# Project files
import Camera
import Draw
import PlayerMovement
import Parser
import Object

FPS = 60
resolution = (800, 600) # XGA
debug = False

mouse_control = True
mouse_sensitivity = 0.5

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
pygame.mouse.set_visible(not mouse_control)

monkey = Object.Object(
        (Parser.get_model_wireframe("./blender_files/monkey.obj")))
monkey.rotate(0, 0, Camera.degrees_to_radians(180))
monkey.translate(0,0,1)
icosphere = Object.Object(
        (Parser.get_model_wireframe("./blender_files/icosphere.obj")))
icosphere.translate(2.5,0,1)
arcade = Object.Object(
        (Parser.get_model_wireframe("./blender_files/arcade.obj")))
arcade.scale(0.1, 0.1, 0.1)
arcade.translate(-2,0,1)

# pos + angle is simply to highlight the current drawing setup.
# use Camera.degrees_to_radians() for angles
game_camera = Camera.Camera((0,0,-1), (0, 0, 0))

object_list = [game_camera.bounding_box, monkey]

running = True
while running:
    Draw.draw_frame(screen, game_camera, object_list, debug, clock)
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
