# General libraries
import pygame

# Project files
import Camera
import Draw
import PlayerMovement

FPS = 60
resolution = (600,600)
debug = True
mouse_control = False
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

race_track = [
    (0,0,0), (0,0,3), (3,0,0),
    (3,0,3), (0,0,3), (3,0,0),
    (0,0,3), (3,0,3), (2.5,0,5.5),
    (0,0,3), (0,0,6), (2.5,0,5.5)
]

# pos + angle is simply to highlight the current drawing setup.
game_camera = Camera.Camera((1.5,-1,-2), (Camera.degrees_to_radians(-10), 0, 0))

running = True
while running:
    Draw.draw_frame(screen, game_camera, race_track, debug)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or PlayerMovement.player_movement(event, mouse_control):
            # this is a little unintuitive, but since PlayerMovment
            #   handles the escape key, it returns True when ESC
            #   is pressed. It updates the keyboard when called.
            running = False
    # the player movement needs to be checked every frame, and not just when a key changes.
    PlayerMovement.player_movement_update(game_camera, mouse_control, mouse_sensitivity)
    clock.tick(FPS)