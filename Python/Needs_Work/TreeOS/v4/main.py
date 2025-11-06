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
debug = True

mouse_control = False
mouse_sensitivity = 0.5

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
pygame.mouse.set_visible(not mouse_control)

red_cylinder = Object.Object(
        (Parser.get_model("./blender_files/cylinder.obj")), (255, 0, 0))
green_cylinder = Object.Object(
        (Parser.get_model("./blender_files/cylinder.obj")), (100, 255, 100))
blue_cylinder = Object.Object(
        (Parser.get_model("./blender_files/cylinder.obj")), (100, 100, 255))
red_cylinder.translate(0,0,-1)
blue_cylinder.translate(0,0,1)

# pos + angle is simply to highlight the current drawing setup.
# use Camera.degrees_to_radians() for angles
game_camera = Camera.Camera((5,0.5,0), (10, -90, 0))

object_list = [game_camera.bounding_box, red_cylinder, green_cylinder, blue_cylinder]

running = True
while running:
    screen.fill([0,0,0])
    Draw.draw_frame_poly(screen, game_camera, object_list, debug, clock)
    red_cylinder.rotate(1,0,0, 0.005)
    green_cylinder.rotate(0,1,0, 0.005)
    blue_cylinder.rotate(0,0,1, 0.005)
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
