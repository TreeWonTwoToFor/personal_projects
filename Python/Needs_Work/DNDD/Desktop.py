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
        self.canvas_dict = {}

    def request_canvas(self, application_name):
        canvas_names = list(self.canvas_dict.keys())
        canvas_names.sort()
        match len(self.canvas_dict):
            case 0: # full screen
                screen_location = (0,0)
                canvas_size = self.width, self.height
            case 1: # veritcal split
                screen_location = (self.width//2,0)
                canvas_size = self.width//2, self.height
                self.canvas_dict[canvas_names[0]] = Canvas(pygame.Surface(canvas_size), (0,0))
            case 2: # horizontal split for 1 and 2 on left side, vertical split for 3 on right
                # tool 3
                screen_location = (self.width//2,0)
                canvas_size = self.width//2, self.height
                # tools 1 and 2 are now half height
                small_canvas_size = self.width//2, self.height//2
                self.canvas_dict[canvas_names[0]] = Canvas(
                    pygame.Surface(small_canvas_size), (0,0))
                self.canvas_dict[canvas_names[1]] = Canvas(
                    pygame.Surface(small_canvas_size), (0, self.height//2))
            case 3: # one tool in each corner
                # tool 4
                screen_location = (self.width//2,self.height//2)
                canvas_size = self.width//2, self.height//2
                self.canvas_dict[canvas_names[0]] = Canvas(
                    pygame.Surface(canvas_size), (0,0))
                self.canvas_dict[canvas_names[1]] = Canvas(
                    pygame.Surface(canvas_size), (0, self.height//2))
                self.canvas_dict[canvas_names[2]] = Canvas(
                    pygame.Surface(canvas_size), (self.width//2, 0))


        self.canvas_dict[application_name] = Canvas(pygame.Surface(canvas_size), screen_location)
    
    def draw(self):
        self.screen.fill([0,0,0])
        for canvas in list(self.canvas_dict.values()):
            self.screen.blit(canvas.surface, canvas.location)
        pygame.display.flip()

    def logic(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return "stop"
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "stop"
        
class Canvas:
    def __init__(self, surface, location):
        self.surface = surface
        self.location = location