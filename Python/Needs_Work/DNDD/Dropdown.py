import pygame

class Dropdown:
    def __init__(self, dropdown_type, desktop_screen, font, initial_pos, dropdown_items):
        # general initialization
        self.font = font
        self.screen = desktop_screen
        self.initial_pos = initial_pos
        self.type = dropdown_type

        self.dropdown_items = dropdown_items
        self.size = (0,0)
        self.rect = None
        self.button_rect = None
        self.color = (180,180,180)

        self.draw()

        if dropdown_type == "main":
            # 0th index of the dropdown is where this submenu lives
            submenu_start_height = initial_pos[1]+self.size[1]/len(self.dropdown_items) * 0 
            self.sub_dropdowns = [Dropdown("apps", desktop_screen, font, (self.size[0], submenu_start_height), 
                ["BattleMap", "DefaultTool", "DiceRoller", "InitiativeTracker"])]

    def draw(self):
        self.size = [0,0]
        item_text_list = []
        for item in self.dropdown_items:
            text_surface = self.font.render(item, True, (0,0,0), self.color)
            self.size[0] = max(text_surface.get_width(), self.size[0])
            item_text_list.append(text_surface)
            self.size[1] += text_surface.get_height()
        # draw the dropdown background
        self.rect = pygame.rect.Rect(*self.initial_pos, self.size[0], self.size[1])
        pygame.draw.rect(self.screen, self.color, self.rect)
        for i in range(len(item_text_list)):
            item = item_text_list[i]
            self.screen.blit(item, (self.initial_pos[0], self.initial_pos[1]+i*text_surface.get_height()))

    def clicking_logic(self, mouse_buttons, cursor_position):
        if mouse_buttons[0]:
            item_height = self.size[1]/len(self.dropdown_items)
            item_rect_list = [(self.dropdown_items[i], pygame.rect.Rect(self.initial_pos[0], self.initial_pos[1]+i*item_height, self.size[0], item_height)) 
                                for i in range(len(self.dropdown_items))]
            for item in item_rect_list:
                if self.inside_rect(item[1], cursor_position):
                    match item[0]:
                        case "Close":
                            return "disable"
                        case "Exit":
                            return "stop"
                        case "Open App >":
                            return "draw submenu"
                        case _:
                            return item[0] # in this case, it should be the name of the program that we want to open

    def inside_rect(self, rectangle, xy):
            x, y = xy[0], xy[1]
            if x >= rectangle.left and x <= rectangle.right:
                if y >= rectangle.top and y <= rectangle.bottom:
                    return True
            return False