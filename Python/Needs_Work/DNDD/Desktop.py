import pygame
import os 
from Window import Window

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

pygame.display.set_caption("D&D Desktop")

debug = False
clicking = False

class Desktop:
    def __init__(self, screen_size, is_debug=False):
        global debug
        debug = is_debug

        # pygame window information
        self.width = screen_size[0]
        self.height = screen_size[1]
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fps = 120
        self.bg_color = (63, 117, 102)
        self.clock = pygame.time.Clock()

        # backend window management
        self.window_dict = {}
        self.application_order = []

    def request_window(self, application_name):
        offset = 1 + len(list(self.window_dict))
        screen_location = (25 * offset, 25 * offset)
        canvas_size = (400, 300)
        self.application_order.append(application_name)
        self.window_dict[application_name] = Window(application_name, pygame.Surface(canvas_size), screen_location)

    def resize_window(self, application_name):
        old_window = self.window_dict[application_name]
        new_window = Window(application_name, pygame.Surface(old_window.size), old_window.location)
        # restore old window state
        new_window.dragging = old_window.dragging
        new_window.relative_drag_position = old_window.relative_drag_position
        new_window.resizing = old_window.resizing
        new_window.resizing_type = old_window.resizing_type
        new_window.relative_mouse_position = old_window.relative_mouse_position
        new_window.old_size = old_window.old_size
        new_window.old_location = old_window.old_location
        # replace old window in dict
        self.window_dict[application_name] = new_window
    
    def draw(self):
        self.screen.fill(self.bg_color)
        for window_name in self.application_order:
            window = self.window_dict[window_name]
            window.debug = debug
            window.draw(self.screen)
        pygame.display.flip()

    def logic(self):
        global debug, clicking
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return "stop"
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "stop"
                    elif event.key == pygame.K_SPACE:
                        debug = not debug
                    else:
                        return ["keyboard", None]
                case pygame.MOUSEBUTTONDOWN:
                    clicking = True
                case pygame.MOUSEBUTTONUP:
                    clicking = False
        if clicking:
            self.clicking_logic()
        else:
            for app in self.application_order:
                window = self.window_dict[app]
                window.dragging = False
                window.resizing = False
    
    def clicking_logic(self):
        mouse_buttons = pygame.mouse.get_pressed()
        cursor_position = pygame.mouse.get_pos()
        for app in self.application_order:
            window = self.window_dict[app]
            new_size = window.check_mouse_interaction(mouse_buttons, cursor_position)
            if new_size is not None:
                # should resize
                self.resize_window(window.name)
                pass
        relative_locations = []
        for app in self.application_order:
            app_location = self.window_dict[app].location
            x = (cursor_position[0]-app_location[0], cursor_position[1]-app_location[1])
            relative_locations.append((app, x))
        return ["mouse", (mouse_buttons, relative_locations)]
