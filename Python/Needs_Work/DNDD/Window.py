import pygame

class Window:
    def __init__(self, application_name, surface, location):
        self.name = application_name
        self.surface = surface
        self.location = location
        self.size = list(surface.get_size())
        
        # dragging/resizing logic
        self.min_size = (50,50)
        self.old_size = surface.get_size()
        self.old_location = (self.location[0], self.location[1])
        self.selected = False

        self.border_px = 5
        self.border_color = (200, 200, 200)
        self.title_bar_px= 15
        self.title_bar_color = (150,150,150)

        self.dragging = False
        self.relative_drag_position = None
        self.resizing = False
        self.resizing_type = None
        self.relative_mouse_position = None

        self.debug = False

    def draw(self, screen):
        bars = self.get_window_bars()
        title_bar, border, corners, long_bars = bars[0], bars[1], bars[2], bars[3]
        
        # drawing the border
        if not self.debug:
            pygame.draw.rect(screen, self.border_color, border)
            pygame.draw.rect(screen, self.title_bar_color, title_bar)
            # not 100% sure that I love this, but it's gonna stay for now lol
            pygame.draw.rect(screen, self.title_bar_color, corners[0])
            pygame.draw.rect(screen, self.title_bar_color, corners[1])
        else:
            pygame.draw.rect(screen, [0,0,255], title_bar)
            for corner in corners:
                pygame.draw.rect(screen, [255,0,0], corner)
            for bar in long_bars:
                pygame.draw.rect(screen, [0,255,0], bar)
        # draw canvas
        screen.blit(self.surface, self.location)

    def check_mouse_interaction(self, mouse_buttons, mouse_pos):
        title_bar, border, corners, long_bars = self.get_window_bars()
        tl, tr, bl, br = corners
        left, right, bottom = long_bars

        if mouse_buttons[0]: # left click
            canvas_rect = pygame.rect.Rect(*self.location, *self.surface.get_size())
            if self.inside_rect(canvas_rect, mouse_pos) and not self.resizing and not self.dragging:
                return ["canvas"]
            elif self.inside_rect(tr, mouse_pos) and not self.resizing:
                self.resizing = True
                self.resizing_type = "tr"
            elif self.inside_rect(tl, mouse_pos) and not self.resizing:
                self.resizing = True
                self.resizing_type = "tl"
            elif self.inside_rect(br, mouse_pos) and not self.resizing:
                self.resizing = True
                self.resizing_type = "br"
            elif self.inside_rect(bl, mouse_pos) and not self.resizing:
                self.resizing = True
                self.resizing_type = "bl"
            elif self.inside_rect(left, mouse_pos) and not self.resizing:
                self.resizing = True
                self.resizing_type = "left"
            elif self.inside_rect(right, mouse_pos) and not self.resizing:
                self.resizing = True
                self.resizing_type = "right"
            elif self.inside_rect(bottom, mouse_pos) and not self.resizing:
                self.resizing = True
                self.resizing_type = "bottom"
            elif self.inside_rect(title_bar, mouse_pos) and not self.dragging:
                self.dragging = True
                self.relative_drag_position = (self.location[0]-mouse_pos[0], self.location[1]-mouse_pos[1])

            if self.dragging:
                self.location = (mouse_pos[0]+self.relative_drag_position[0], 
                                 mouse_pos[1]+self.relative_drag_position[1])
                return ["dragging"]
            elif self.resizing:
                match self.resizing_type:
                    case "bl":
                        # change the width and height of the window to be location + relative_mouse_position
                        #   and make the position track the mouse
                        self.location = [mouse_pos[0]-self.border_px//2, self.location[1]]
                        self.size = [self.old_size[0]+self.old_location[0]-mouse_pos[0], 
                                     mouse_pos[1]-self.old_location[1]]
                    case "tr":
                        # change the width and height of the window to be location + relative_mouse_position
                        #   and make the position track the mouse
                        self.location = [self.old_location[0]-self.border_px*2, mouse_pos[1]+self.title_bar_px]
                        self.size = [mouse_pos[0]-self.old_location[0], 
                                     self.old_size[1]+self.old_location[1]-mouse_pos[1]]
                    case "tl":
                        # change the width and height of the window to be location + relative_mouse_position
                        #   and make the position track the mouse
                        self.location = [mouse_pos[0]+self.border_px*2, mouse_pos[1]+self.title_bar_px]
                        self.size = [self.old_size[0]+self.old_location[0]-mouse_pos[0],
                                     self.old_size[0]+self.old_location[1]-mouse_pos[1]]
                    case "br":
                        # change the width and height of the window to be location + relative_mouse_position
                        self.size = [mouse_pos[0]-self.location[0]-self.border_px//2,
                                     mouse_pos[1]-self.location[1]-self.border_px//2]
                    case "left":
                        # change the width of the window to be location + relative_mouse_position,
                        #   and make the position track the mouse
                        self.size = [self.old_size[0]+self.old_location[0]-mouse_pos[0], self.size[1]]
                        self.location = [mouse_pos[0]-self.border_px//2, self.location[1]]
                    case "right":
                        # change the width of the window to be location + relative_mouse_position
                        self.size = [mouse_pos[0]-self.location[0]-self.border_px//2, self.size[1]]
                    case "bottom":
                        # change the height of the window to be location + relative_mouse_position
                        self.size = [self.size[0], mouse_pos[1]-self.location[1]-self.border_px//2]
            else:
                self.old_size = self.size
                self.old_location = self.location
        if self.size != list(self.surface.get_size()):
            self.size[0] = max(self.size[0], self.min_size[0])
            self.size[1] = max(self.size[1], self.min_size[1])
            return ['resize', self.size]

    def normalize(self):
        self.old_size = self.size
        self.old_location = self.location
        self.dragging = False
        self.resizing = False
        self.selected = False

    def get_window_bars(self):
        canvas_size = self.surface.get_size()
        scaler = 2

        # one title bar along the whole top
        title_bar_size = (canvas_size[0], self.title_bar_px)
        title_bar_rect = pygame.rect.Rect(self.location[0], self.location[1]-self.title_bar_px, *title_bar_size)
        # 4 corners for diagonal scaling
        corner_size = (self.border_px*scaler, self.border_px*scaler)
        tl_corner_rect = pygame.rect.Rect(self.location[0]-corner_size[0], 
                                          self.location[1]-title_bar_size[1], corner_size[0], title_bar_size[1])
        tr_corner_rect = pygame.rect.Rect(self.location[0]+canvas_size[0], 
                                          self.location[1]-title_bar_size[1], corner_size[0], title_bar_size[1])
        bl_corner_rect = pygame.rect.Rect(self.location[0]-corner_size[0], 
                                          self.location[1]+canvas_size[1], *corner_size)
        br_corner_rect = pygame.rect.Rect(self.location[0]+canvas_size[0], 
                                          self.location[1]+canvas_size[1], *corner_size)
        corners = [tl_corner_rect, tr_corner_rect, bl_corner_rect, br_corner_rect]
        # two vertical bars for horizontal scaling
        vertical_bar_size = (self.border_px*scaler, canvas_size[1])
        left_bar  = pygame.rect.Rect(self.location[0]-vertical_bar_size[0], self.location[1], *vertical_bar_size)
        right_bar = pygame.rect.Rect(self.location[0]+canvas_size[0], self.location[1], *vertical_bar_size)
        # one bottom bar for vertical scaling
        horizontal_bar_size = (canvas_size[0], self.border_px*scaler)
        bottom_bar = pygame.rect.Rect(self.location[0], self.location[1]+canvas_size[1], *horizontal_bar_size)
        bars = [left_bar, right_bar, bottom_bar]

        border_size = (canvas_size[0]+self.border_px*2, canvas_size[1]+self.border_px)
        border_rect = pygame.rect.Rect(self.location[0]-self.border_px, self.location[1], *border_size)

        return [title_bar_rect, border_rect, corners, bars]
    
    def inside_rect(self, rectangle, xy):
        x, y = xy[0], xy[1]
        if x >= rectangle.left and x <= rectangle.right:
            if y >= rectangle.top and y <= rectangle.bottom:
                return True
        return False
