# General libraries
import pygame

# Project files
import Camera
import Draw
import PlayerMovement

FPS = 60
resolution = (600,600)
debug = True
mouse_control = True
mouse_sensitivity = 1

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

if mouse_control:
    pygame.mouse.set_visible(False)

# cube_points = [
#     (0,0,0),
#     (0,1,0),
#     (1,0,0),
#     (1,1,0),
#     (1,0,1),
#     (1,1,1),
#     (0,0,1),
#     (0,1,1),
#     (0,0,0),
#     (0,1,0)
# ]

cube_points = [
    (0,1,0), (1,1,0), (1,1,1),
    (0,1,0), (0,1,1), (1,1,1),
    (0,1,0), (0,1,1), (0,0,1),
    (0,0,0), (0,1,0), (0,0,1),
    (0,1,0), (1,1,0), (0,0,0),
    (1,0,0), (1,1,0), (0,0,0),
    (1,0,0), (1,1,0), (1,1,1),
    (1,0,0), (1,0,1), (1,1,1),
    (0,1,1), (1,0,1), (1,1,1),
    (0,1,1), (0,0,1), (1,0,1),
    (0,0,1), (1,0,0), (1,0,1),
    (1,0,0), (0,0,1), (0,0,0)
]

# pos + angle is simply to highlight the current drawing setup.
game_camera = Camera.Camera((1.25,-0.5,-5), (Camera.degrees_to_radians(-10), 0, 0))

running = True
while running:
    Draw.draw_frame(screen, game_camera, cube_points, debug)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or PlayerMovement.player_movement(event, mouse_control):
            # this is a little unintuitive, but since PlayerMovment
            #   handles the escape key, it returns True when ESC
            #   is pressed. It updates the keyboard when called.
            running = False
    # the player movement needs to be checked every frame, and not just when a key changes.
    PlayerMovement.player_movement_update(game_camera, mouse_control, mouse_sensitivity)
    clock.tick(FPS)