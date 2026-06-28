import pygame

pygame.init()

pygame.display.set_caption("D&D Desktop")

class Desktop:
    def __init__(self, screen_size):
        self.width = screen_size[0]
        self.height = screen_size[1]
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.canvas_list = []

    def request_canvas(self):
        canvas_size = self.width, self.height
        if len(self.canvas_list) == 0:
            screen_location = (0,0)
        # elif len(self.canvas_list) == 1:
        #     screen_location = (self.width//2,0)
        canvas = Canvas(pygame.Surface(canvas_size), screen_location)
        self.canvas_list.append(canvas)
        return canvas.surface
    
    def draw(self):
        self.screen.fill([0,0,0])
        for canvas in self.canvas_list:
            self.screen.blit(canvas.surface, canvas.location)
        pygame.display.flip()

    def logic(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "stop"
        
class Canvas:
    def __init__(self, surface, location):
        self.surface = surface
        self.location = location