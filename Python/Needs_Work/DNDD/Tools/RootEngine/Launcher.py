# General libraries
import pygame
import math

# Project files
from .Engine import Draw
from .Engine import SceneManager
from .Engine import LaunchSettings

application_name = "RootEngine"

background_color = (255,255,255)
canvas = None

def run(window_dict, desktop_instruction):
    global canvas, screen
    canvas = window_dict[application_name].surface
    screen = canvas 
    if desktop_instruction is not None:
        event_type, event_details = desktop_instruction[0], desktop_instruction[1]
    else:
        event_type, event_details = None, None
    logic_output = logic(event_type, event_details)
    draw(logic_output)

def draw(logic_output):
    iterate()

def logic(event_type, event_details):
    match event_type:
        case "mouse":
            buttons_pressed = event_details[0]
            mouse_pos = None
            locations = event_details[1]
            for location in locations:
                if location[0] == application_name:
                    mouse_pos = location[1]
            if not mouse_in_window(mouse_pos):
                return None
            # otherwise, perform mouse logic
            print(buttons_pressed, mouse_pos)
        case "keyboard":
            pass

def mouse_in_window(mouse_position):
    canvas_size = canvas.get_size()
    if mouse_position[0] > 0 and mouse_position[0] <= canvas_size[0]:
        if mouse_position[1] > 0 and mouse_position[1] <= canvas_size[1]:
            return True
    return False

# pull the general settings
settings = LaunchSettings.get_settings()
FPS               = settings[0]
resolution        = (0,0)
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
# screen = pygame.display.set_mode(resolution)
screen = canvas
ui_layer = pygame.display.set_mode(resolution, pygame.RLEACCEL)
depth_buffer = []
clock = pygame.time.Clock()
pygame.event.set_grab(mouse_control)
pygame.mouse.set_visible(not mouse_control)

# load in the scene
scene = SceneManager.load_scene("./Tools/RootEngine/Assets/Scenes/" + scene_name)
game_camera      = scene[0]
object_dict      = scene[1]
scene_actions    = scene[2]
background_color = scene[3]
light_sources    = scene[4]
dt = 0.016 # presumes 60 FPS, but gets recalculated every frame

# one time run operations
if scene_name == "rubiks_cube.rsc":
    Draw.lighting = False # makes the colors more vibrant
    LaunchSettings.GameFile.scramble(list(object_dict.values()))

def iterate():
    global running, dt

    resolution = canvas.get_size()

    # scene specific code
    GameFile = LaunchSettings.GameFile
    game_logic      = GameFile.game_logic
    game_function   = GameFile.player_movement
    update_function = GameFile.player_movement_update
    ui_logic        = GameFile.ui_logic

    # object update
    for action in scene_actions:
        match action[0]:
            case "translate": action[1].translate([val*dt for val in action[2]])
            case "scale": action[1].scale([val*dt for val in action[2]])
            case "rotate": action[1].rotate(action[2], action[3] * dt)
            case "orbit": action[1].orbit(action[2], action[3] * dt, action[4])
    object_list = list(object_dict.values())
    game_logic(object_list)

    # visual update
    screen.fill(background_color)
    depth_buffer = [math.inf] * (screen.get_width() * screen.get_height())
    Draw.draw_frame_poly(screen, depth_buffer, game_camera, object_list, light_sources, debug, clock)
    ui_logic(ui_layer, False)
    pygame.display.update()

    # game update
    for event in pygame.event.get():
        if event.type == pygame.QUIT or game_function(screen, event):
            # this is a little unintuitive, but since game_function
            #   handles the escape key, it returns True when ESC
            #   is pressed. It updates the keyboard when called.
            # also, we include screen for screenshot capabilities
            running = False
    # the player movement needs to be checked every frame, and not just when a key changes.
    update_function(game_camera, mouse_control, mouse_sensitivity, object_list, dt)

    # delay if necessary
    dt = round(clock.tick(FPS) * 0.001, 4)