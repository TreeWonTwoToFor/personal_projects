import pygame

class Dropdown:
    # parent initialization option
    def __init__(self, dropdown_type, desktop_screen, font, initial_pos, dropdown_items):
        # general initialization
        self.font = font
        self.screen = desktop_screen
        self.initial_pos = initial_pos
        self.label = dropdown_type

        self.dropdown_items = dropdown_items
        self.size = (0,0)
        self.rect = None
        self.button_rect = None
        self.color = (180,180,180)

        self.draw()

        self.sub_dropdowns = []
        if dropdown_type == "main":
            for item in dropdown_items:
                if type(item) == str:
                    # it's just a regular option, so we let it stay
                    pass
                elif type(item) == list:
                    # it's a submenu. idx 0 is the label for the dropdown, with 1-n being the options
                    submenu_start_height = initial_pos[1] + self.size[1] / len(self.dropdown_items) * 0 
                    self.sub_dropdowns.append(Dropdown("apps", desktop_screen, font, (self.size[0], submenu_start_height), item[1:]))

    # submenu initialization option
    def create_submenu(self, submenu_items):
        submenu = Dropdown("submenu", self.screen, self.font, self.initial_pos, submenu_items[1:])
        initial_x = self.initial_pos[0]+self.size[0]
        initial_y = 0
        offset = 0
        for item in self.dropdown_items:
            if item == submenu_items:
                initial_y = self.initial_pos[1]+self.size[1]/len(self.dropdown_items) * offset
            offset += 1
        submenu.initial_pos = (initial_x, initial_y)
        return submenu

    def draw(self):
        self.size = [0,0]
        item_text_list = []
        for item in self.dropdown_items:
            if type(item) == list: item = item[0] # gets the name for the submenu header
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
                    if type(item[0]) == list:
                        # go into the list at index 0, then grab the first element for the submenu header
                        menu_option = item[0][0]
                    else:
                        # simply grab the string at index 0
                        menu_option = item[0]
                    return menu_option

    def inside_rect(self, rectangle, xy):
            x, y = xy[0], xy[1]
            if x >= rectangle.left and x <= rectangle.right:
                if y >= rectangle.top and y <= rectangle.bottom:
                    return True
            return False