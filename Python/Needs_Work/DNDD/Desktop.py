import os 
import time
import pygame
from Window import Window
from Dropdown import Dropdown

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
pygame.display.set_caption("D&D Desktop")
font = pygame.font.Font("../Comfortaa.ttf", 20)

debug = False
clicking = False

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
        self.dropdown_list = []
        self.main_dropdown = Dropdown("main", self.screen, font, (0, self.task_bar_height_px), ["Open App >", "Exit"])

        # backend window management
        self.window_dict = {}
        self.application_order = []
        self.selected_window = None
        self.focused_window = None

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
        minutes = str(current_time.tm_min) if current_time.tm_min > 10 else "0" + str(current_time.tm_min)
        hours = str(current_time.tm_hour) if current_time.tm_hour != 12 else "12"
        time_string = f"{hours}:{minutes}"
        test_text = font.render(time_string, True, (0,0,0), None)
        self.screen.blit(test_text, (self.width-test_text.get_width()-2, 2))
        # dropdown button
        text_string = "Desktop"
        text_surface = font.render(text_string, True, (0,0,0), None)
        self.main_dropdown.button_rect = text_surface.get_rect()
        self.screen.blit(text_surface, (2, 2))
        # dropdowns
        for dropdown in self.dropdown_list:
            dropdown.draw()
        # app icons
        icon_location = [self.main_dropdown.button_rect.width+10,2]
        for app in self.application_order:
            icon_name = self.icons[app]
            scaled_icon = pygame.transform.scale(pygame.image.load(icon_name), (self.task_bar_height_px-3, self.task_bar_height_px-3))
            self.screen.blit(scaled_icon, icon_location)
            icon_location[0] += self.task_bar_height_px + 2
        # refresh screen
        pygame.display.flip()

    def logic(self):
        global debug, clicking
        # handling the pygame events
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
                        return ["keyboard", (event.key, self.focused_window)]
                case pygame.MOUSEBUTTONDOWN:
                    clicking = True
                case pygame.MOUSEBUTTONUP:
                    clicking = False
        # handling mouse interactions
        if clicking:
            mouse_buttons = pygame.mouse.get_pressed()
            cursor_position = pygame.mouse.get_pos()
            # taskbar
            if self.inside_taskbar(cursor_position):
                if self.inside_rect(self.main_dropdown.button_rect, cursor_position):
                    if self.main_dropdown in self.dropdown_list:
                        self.dropdown_list = []
                    else:
                        self.dropdown_list.append(self.main_dropdown)
                    clicking = False
            # main dropdown menu
            elif self.main_dropdown in self.dropdown_list and self.inside_rect(self.main_dropdown.rect, cursor_position):
                clicking = False
                x = self.main_dropdown.clicking_logic(mouse_buttons, cursor_position)
                match x:
                    case "disable": self.dropdown_list = []
                    case "stop": return "stop"
                    case "draw submenu": self.dropdown_list.append(self.main_dropdown.sub_dropdowns[0])
            # secondary dropdown menu
            elif self.main_dropdown.sub_dropdowns[0] in self.dropdown_list and self.inside_rect(self.main_dropdown.sub_dropdowns[0].rect, cursor_position):
                clicking = False
                app = self.main_dropdown.sub_dropdowns[0].clicking_logic(mouse_buttons, cursor_position)
                if app is not None:
                    self.dropdown_list = []
                if app not in self.application_order:
                    return app
            # general sceen space
            elif self.inside_screen(cursor_position):
                self.dropdown_list = []
                return self.window_clicking_logic(mouse_buttons, cursor_position)
        else:
            self.selected_window = None
            for app in self.application_order:
                window = self.window_dict[app]
                window.normalize()
    
    def window_clicking_logic(self, mouse_buttons, cursor_position):
        if self.selected_window is not None:
            window = self.window_dict[self.selected_window]
            x = window.check_mouse_interaction(mouse_buttons, cursor_position)
            if x != None:
                if x[0] == "resize":
                    self.resize_window(window.name)
                self.application_order.remove(window.name)
                self.application_order.insert(0, window.name)
        else:
            for app in self.application_order:
                window = self.window_dict[app]
                if window.selected and self.selected_window is None:
                    self.selected_window = app
                    x = window.check_mouse_interaction(mouse_buttons, cursor_position)
                    if x != None:
                        if x[0] == "resize":
                            self.resize_window(window.name)
                        self.application_order.remove(window.name)
                        self.application_order.insert(0, window.name)
                        break
                elif not window.selected and self.selected_window is None:
                    x = window.check_mouse_interaction(mouse_buttons, cursor_position)
                    if x != None:
                        window.selected = True
        if self.selected_window is not None: 
            self.focused_window = self.selected_window
        relative_location = None
        for app in self.application_order:
            if app == self.focused_window:
                app_location = self.window_dict[app].location
                x = (cursor_position[0]-app_location[0], cursor_position[1]-app_location[1])
                relative_location = x
        return ["mouse", (mouse_buttons, relative_location, self.focused_window)]
    
    def inside_rect(self, rectangle, xy):
        x, y = xy[0], xy[1]
        if x >= rectangle.left and x <= rectangle.right:
            if y >= rectangle.top and y <= rectangle.bottom:
                return True
        return False
    
    def inside_screen(self, xy):
        x, y = xy[0], xy[1]
        if x > 0 and x < self.width:
            if y > self.task_bar_height_px and y < self.height:
                return True
        return False

    def inside_taskbar(self, xy):
        x, y = xy[0], xy[1]
        if x > 0 and x < self.width:
            if y > 0 and y < self.task_bar_height_px:
                return True
        return False