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
    def __init__(self, screen_size, tool_reference_table, in_debug_mode=False):
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
        self.tool_reference_table = tool_reference_table # for handling dropdown options
        self.main_dropdown = Dropdown("main", self.screen, font, (0, self.task_bar_height_px), [["Open App >"] + list(tool_reference_table), "Exit"])
        self.dropdown_path = ""

        # backend window management
        self.window_dict = {}
        self.application_order = []
        self.selected_window = None
        self.focused_window = None

    def open_app(self, application_name):
        self.request_window(application_name)
        self.application_order.append(application_name)
        
    def close_app(self, application_name):
        self.application_order.remove(application_name)
        self.icons.pop(application_name)
        self.window_dict.pop(application_name)
        num_icons = 0
        for app in self.application_order:
            icon_location = [self.main_dropdown.button_rect.width+10 + (self.task_bar_height_px + 2) * num_icons, 2]
            self.icons[app] = (self.icons[app][0], icon_location)
            num_icons += 1

    def request_window(self, application_name):
        offset = 1 + len(self.application_order)
        screen_location = (50 * offset, 50 * offset)
        canvas_size = (400, 300)
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
    
    def load_icon(self, app_name, icon_path="./icons/default_icon.png"):
        icon = pygame.transform.scale(pygame.image.load(icon_path), (self.task_bar_height_px-3, self.task_bar_height_px-3))
        icon_location = [self.main_dropdown.button_rect.width+10 + (self.task_bar_height_px + 2) * len(self.icons), 2]
        self.icons[app_name] = (icon, icon_location)

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
        minutes = str(current_time.tm_min) if current_time.tm_min >= 10 else "0" + str(current_time.tm_min)
        hours = str(current_time.tm_hour%12) if current_time.tm_hour % 12 != 0 else "12"
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
            dropdown[1].draw()
        # app icons
        for app in self.application_order:
            self.screen.blit(*self.icons[app])
        # refresh screen
        pygame.display.flip()

    def logic(self):
        global debug, clicking
        # handling the pygame events 
        # FIXME: only will handle the first of the seen events, as it'll just return out
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return "stop"
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "stop"
                    #elif event.key == pygame.K_SPACE:
                    #    debug = not debug
                    else:
                        return ["keyboard down", (pygame.key.name(event.key), self.focused_window)]
                case pygame.KEYUP:
                    return ["keyboard up", (pygame.key.name(event.key), self.focused_window)]
                case pygame.MOUSEBUTTONDOWN:
                    clicking = True
                case pygame.MOUSEBUTTONUP:
                    clicking = False
                    self.selected_window = None
                    for app in self.application_order:
                        window = self.window_dict[app]
                        window.normalize()
                    return ["mouse", ("not clicking", self.focused_window)]
        # handling mouse interactions
        if clicking:
            mouse_buttons = pygame.mouse.get_pressed()
            cursor_position = pygame.mouse.get_pos()
            clicking = self.taskbar_clicking_logic(mouse_buttons, cursor_position, clicking)
            clicking, instruction = self.dropdown_clicking_logic(mouse_buttons, cursor_position, clicking)
            if instruction is not None:
                return instruction
            # general sceen space
            if self.inside_screen(cursor_position) and clicking:
                self.dropdown_list = []
                return self.window_clicking_logic(mouse_buttons, cursor_position)

    def taskbar_clicking_logic(self, mouse_buttons, cursor_position, clicking):
        if self.inside_taskbar(cursor_position):
            if self.inside_rect(self.main_dropdown.button_rect, cursor_position):
                clicking = False
                if self.main_dropdown in self.dropdown_list:
                    self.dropdown_list = []
                else:
                    self.dropdown_list = [("Desktop", self.main_dropdown)]
            for icon_name in list(self.icons):
                icon = self.icons[icon_name]
                icon_image, icon_location = icon
                icon_rect = pygame.rect.Rect(*icon_location, icon_image.get_rect().width, icon_image.get_rect().height)
                if self.inside_rect(icon_rect, cursor_position):
                    clicking = False
                    app = icon_name
                    self.dropdown_list = [(app, Dropdown(app, self.screen, font, [icon_location[0], self.task_bar_height_px], self.tool_reference_table[app]["dropdown"]))]
        return clicking
    
    def dropdown_clicking_logic(self, mouse_buttons, cursor_position, clicking):
        output = None
        for dropdown_info in self.dropdown_list:
            parent_app, dropdown = dropdown_info
            if self.inside_rect(dropdown.rect, cursor_position):
                clicking = False
                x = dropdown.clicking_logic(mouse_buttons, cursor_position)
                if x is not None:
                    if '>' in x:
                        # FIXME: when clicking to another submenu in the same dropdown, it keeps the other one on screen.
                        #   I either have to make it s.t. it clears the dropdown list every time, but keeps track of the full path,
                        #   or I have a recursive function to go through and remove the full depth of submenus in a specific path
                        option = x
                        # open a submenu
                        for dropdown_option in dropdown.dropdown_items:
                            if type(dropdown_option) == list and dropdown_option[0] == option:
                                # we now need to make a new submenu based on the parent's information,
                                # along with which menu options it has
                                submenu = dropdown.create_submenu(dropdown_option)
                                # then we can add it to the list
                                self.dropdown_list.append((parent_app, submenu))
                                if len(self.dropdown_path) == 0:
                                    self.dropdown_path = dropdown_option[0]
                                else:
                                    self.dropdown_path = self.dropdown_path + " " + dropdown_option[0]
                    else:
                        # it's some final option that we need to execute
                        self.dropdown_list = []
                        instruction = x
                        if len(self.dropdown_path) != 0:
                            output = (parent_app, self.dropdown_path + " " + instruction)
                            self.dropdown_path = ""
                        else:
                            output = (parent_app, instruction)
                        match parent_app:
                            case "Desktop":
                                if instruction == "Exit": 
                                    output = "stop"
        return (clicking, output)

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
    
