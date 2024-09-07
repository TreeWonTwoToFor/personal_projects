import pygame
import time
import os

pygame.init()

screenX = 1080
screenY = 720
bg_color = (107, 181, 199)
FPS = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screenX, screenY), pygame.RESIZABLE)

def is_touching(rect_list_a, rect_list_b):
    for i in range(len(rect_list_a)):
        for j in range(len(rect_list_b)):
            if pygame.Rect.colliderect(rect_list_a[i], rect_list_b[j]):
                return True
    return False

class Player:
    def __init__(self):
        self.x = 150
        self.y = 150
        self.w = 50
        self.h = 100
        self.hspeed = 5
        self.color = (255, 0, 0)
        self.collide_color = (0, 255, 50)
        self.collider_thickness = 5
        self.draw_colliders = False
        self.air_state = "ground"


    def update(self, stage):
        # we want to flip the y value so that 0 is the ground
        self.display_y = screenY - self.y - self.h

        # creating rectangles for collision purposes
        self.rect = pygame.Rect(self.x, self.display_y, self.w, self.h)
        self.left_collider = pygame.Rect(self.x, self.display_y, self.collider_thickness, self.h)
        self.right_collider = pygame.Rect(self.x+self.w-self.collider_thickness, self.display_y, self.collider_thickness, self.h)
        self.ground_collider = pygame.Rect(self.x, self.display_y+self.h, self.w, self.collider_thickness)
        self.ceiling_collider = pygame.Rect(self.x, self.display_y-self.collider_thickness, self.w, self.collider_thickness)
        self.touching_stage = is_touching([self.ground_collider], [stage.rect])
        self.grabbing_ledge = is_touching([self.left_collider, self.right_collider, self.ceiling_collider], [stage.left_ledge, stage.right_ledge])
        if self.touching_stage: self.y = 150
        if self.grabbing_ledge and not self.touching_stage: 
            if self.x < screenX/2: 
                # we are on the left side
                self.x, self.y = stage.x-self.w, stage.y-self.h/2
            elif self.x > screenX/2: 
                # we are on the left side
                self.x, self.y = stage.x+stage.w, stage.y-self.h/2

        # updating states
        if self.touching_stage: 
            self.air_state = "ground"
        elif self.grabbing_ledge:
            self.air_state = "ledge"
        else:
            self.air_state = "falling"

        if self.air_state == "falling":
            self.y -= 3

        print(self.air_state)

    def display(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.draw_colliders:
            pygame.draw.rect(screen, self.collide_color, self.ground_collider)
            pygame.draw.rect(screen, self.collide_color, self.ceiling_collider)
            pygame.draw.rect(screen, self.collide_color, self.left_collider)
            pygame.draw.rect(screen, self.collide_color, self.right_collider)

    def move(self, direction):
        match direction:
            case "left":
                self.x -= self.hspeed
            case "right":
                self.x += self.hspeed
            case "jump":
                if self.grabbing_ledge:
                    self.y += self.h
                    self.air_state = "jumping"
                if not (self.air_state == "jumping" or self.air_state == "falling"):
                    self.y += 100
                    self.air_state = "jumping"

class Stage:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.w = 880
        self.h = 50
        self.color = (50, 57, 59)
        self.collide_color = (0, 255, 50)
        self.collider_thickness = 5
        self.draw_colliders = False

    def update(self):
        display_y = screenY - self.y - self.h
        self.rect = pygame.Rect(self.x, display_y, self.w, self.h)
        self.left_ledge = pygame.Rect(self.x, display_y, self.collider_thickness, self.h)
        self.right_ledge = pygame.Rect(self.x+self.w-self.collider_thickness, display_y, self.collider_thickness, self.h)

    def display(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.draw_colliders:
            pygame.draw.rect(screen, (0, 255, 50), self.left_ledge)
            pygame.draw.rect(screen, (0, 255, 50), self.right_ledge)

player_one = Player()
my_stage = Stage()

running = True
while running:
    os.system("cls")
    screen.fill(bg_color)
    my_stage.update()
    my_stage.display(screen)
    player_one.update(my_stage)
    player_one.display(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print(mouse_pos)
    key_list = pygame.key.get_pressed()
    if key_list[97]:
        player_one.move("left")
    if key_list[100]:
        player_one.move("right")
    if key_list[119]:
        player_one.move("jump")
    for i in range(len(key_list)):
        if key_list[i]:
            print(i)
    pygame.display.update()
    clock.tick(FPS)