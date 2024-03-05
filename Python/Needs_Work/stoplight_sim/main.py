import pygame

screen_x = 1280
screen_y = 720
FPS = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Stoplight sim")

grass_color = (0, 255, 100)
road_color = (70, 70, 70)
line_color = (255, 255, 255)
headlight_on_color = (255, 255, 0)
headlight_off_color = (100, 100, 100)

red = (255, 0, 0)
blue = (0, 0, 255)
purple = (255, 0, 255)

class intersection:
    def __init__(self, x, y, width, height, line_thickness):
        self.color = road_color
        self.rect = pygame.Rect(x, y, width, height)
        self.line_thickness = line_thickness

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def draw_lines(self):
        pygame.draw.rect(screen, line_color, 
                         pygame.Rect(self.rect.topleft[0], self.rect.topleft[1], self.line_thickness, self.rect.height))
        pygame.draw.rect(screen, line_color, 
                         pygame.Rect(self.rect.topright[0], self.rect.topright[1], self.line_thickness, self.rect.height))
        pygame.draw.rect(screen, line_color, 
                         pygame.Rect(self.rect.topleft[0], self.rect.topleft[1], self.rect.width, self.line_thickness))
        pygame.draw.rect(screen, line_color, 
                         pygame.Rect(self.rect.bottomleft[0], self.rect.bottomleft[1]-self.line_thickness, self.rect.width, self.line_thickness))

class road:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(screen, road_color, self.rect)

class car:
    def __init__(self, color, car_id, x, y, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.car_id = car_id
        self.animation_tick = 0
        self.facing_direction = "right"
        self.turning_direction = "none"
        self.speed = 2

    def drive(self):
        if self.facing_direction == "right":
            self.x += self.speed
        elif self.facing_direction == "left":
            self.x -= self.speed
        elif self.facing_direction == "up":
            self.y -= self.speed
        elif self.facing_direction == "down":
            self.y += self.speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        

def draw_stoplights(light_list):
    for light in light_list:
        light.draw()
        light.draw_lines()

def update_cars(car_list):
    for car in car_list:
        pygame.draw.rect(screen, car.color, car.rect)

        car.animation_tick += 1
        headlight_color = 0
        if car.animation_tick < 30: #headlight should be off
            headlight_color = headlight_off_color
        elif car.animation_tick < 60: #headlight should be on
            headlight_color = headlight_on_color

        if car.animation_tick >= 60:
            car.animation_tick = 0

        pygame.draw.rect(screen, headlight_off_color, pygame.Rect(car.x+car.width - 10, car.y, 10, 15))
        pygame.draw.rect(screen, headlight_off_color, pygame.Rect(car.x+car.width - 10, car.y+car.height - 15, 10, 15))

        if car.turning_direction == "left":
            pygame.draw.rect(screen, headlight_color, pygame.Rect(car.x+car.width - 10, car.y, 10, 15))
        elif car.turning_direction == "right":
            pygame.draw.rect(screen, headlight_color, pygame.Rect(car.x+car.width - 10, car.y+car.height - 15, 10, 15))
            

light_list = [intersection(25, 25, 200, 200, 2), 
              intersection(325, 25, 200, 200, 5), 
              intersection(625, 25, 200, 200, 7),
              intersection(925, 25, 200, 200, 10)]
car_list = [car((255, 40, 40), 0, 50, 50, 80, 40),
            car((0, 100, 255), 1, 50, 150, 80, 40)]

running = True
while running:
    screen.fill(grass_color)
    draw_stoplights(light_list)
    update_cars(car_list)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                car_list[0].turning_direction = "none"
                car_list[0].facing_direction = "left"
            elif event.key == pygame.K_RIGHT:
                car_list[0].turning_direction = "none"
                car_list[0].facing_direction = "right"
            elif event.key == pygame.K_UP:
                car_list[0].turning_direction = "left"
                car_list[0].facing_direction = "up"
            elif event.key == pygame.K_DOWN:
                car_list[0].turning_direction = "right"
                car_list[0].facing_direction = "down"
            else:
                car_list[0].turning_direction = "none"
                car_list[0].facing_direction = "none"
    car_list[0].drive()
    pygame.display.update()
    clock.tick(FPS)