import os 
import time
import pygame
from Window import Window

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

pygame.display.set_caption("D&D Desktop")

font = pygame.font.Font("../Comfortaa.ttf", 20)

debug = False
clicking = False
selected_window = None
focused_window = None

class Desktop:
    def __init__(self, screen_size, in_debug_mode=False):
        global debug
        debug = in_debug_mode

        # pygame window information
        self.width = screen_size[0]
        self.height = screen_size[1]
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fps = 120
        self.bg_color = (63, 117, 102)
        self.clock = pygame.time.Clock()

        # task bar information
        self.task_bar_height_px = 25
        self.task_bar_color = (220,220,220)
        self.icons = {}

        # backend window management
        self.window_dict = {}
        self.application_order = []

    def request_window(self, application_name):
        offset = 1 + len(list(self.window_dict))
        screen_location = (40 * offset, 40 * offset)
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
        # fill background
        self.screen.fill(self.bg_color)
        # draw applications
        self.application_order.reverse()
        for window_name in self.application_order:
            window = self.window_dict[window_name]
            window.debug = debug
            window.draw(self.screen)
        self.application_order.reverse()
        # TASK BAR
        # draw task bar
        task_bar_rect = pygame.rect.Rect(0, 0, self.width, self.task_bar_height_px)
        pygame.draw.rect(self.screen, self.task_bar_color, task_bar_rect)
        # task bar clock
        current_time = time.localtime()
        time_string = f"{current_time.tm_hour%12}:{current_time.tm_min}"
        test_text = font.render(time_string, True, (0,0,0), None)
        self.screen.blit(test_text, (self.width-test_text.get_width()-2, 2))
        # app icons
        icon_location = [2,2]
        for app in self.application_order:
            icon_name = self.icons[app]
            scaled_icon = pygame.transform.scale(pygame.image.load(icon_name), (self.task_bar_height_px-3, self.task_bar_height_px-3))
            self.screen.blit(scaled_icon, icon_location)
            icon_location[0] += self.task_bar_height_px
        # refresh screen
        pygame.display.flip()

    def logic(self):
        global debug, clicking, selected_window
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
                        return ["keyboard", (event.key, focused_window)]
                case pygame.MOUSEBUTTONDOWN:
                    clicking = True
                case pygame.MOUSEBUTTONUP:
                    clicking = False
        if clicking:
            mouse_buttons = pygame.mouse.get_pressed()
            cursor_position = pygame.mouse.get_pos()
            # are we inside the screen?
            if cursor_position[0] > 0 and cursor_position[0] < self.width:
                if cursor_position[1] > self.task_bar_height_px and cursor_position[1] < self.height:
                    return self.clicking_logic(mouse_buttons, cursor_position)
        else:
            selected_window = None
            for app in self.application_order:
                window = self.window_dict[app]
                window.normalize()
    
    def clicking_logic(self, mouse_buttons, cursor_position):
        global selected_window, focused_window
        
        if selected_window is not None:
            window = self.window_dict[selected_window]
            x = window.check_mouse_interaction(mouse_buttons, cursor_position)
            if x != None:
                if x[0] == "resize":
                    self.resize_window(window.name)
                self.application_order.remove(window.name)
                self.application_order.insert(0, window.name)
        else:
            for app in self.application_order:
                window = self.window_dict[app]
                if window.selected and selected_window is None:
                    selected_window = app
                    x = window.check_mouse_interaction(mouse_buttons, cursor_position)
                    if x != None:
                        if x[0] == "resize":
                            self.resize_window(window.name)
                        self.application_order.remove(window.name)
                        self.application_order.insert(0, window.name)
                        break
                elif not window.selected and selected_window is None:
                    x = window.check_mouse_interaction(mouse_buttons, cursor_position)
                    if x != None:
                        window.selected = True
        if selected_window is not None: 
            focused_window = selected_window
        relative_location = None
        for app in self.application_order:
            if app == focused_window:
                app_location = self.window_dict[app].location
                x = (cursor_position[0]-app_location[0], cursor_position[1]-app_location[1])
                relative_location = x
        return ["mouse", (mouse_buttons, relative_location, focused_window)]