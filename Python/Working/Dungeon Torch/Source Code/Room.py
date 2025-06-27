import random
import pygame

class Room():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        random_r = random.randint(100, 255)
        random_g = random.randint(100, 255)
        random_b = random.randint(100, 255)
        self.color = (random_r, random_g, random_b)
        self.visited = False 
        self.has_enemy = True
        self.door_states = [0, 0, 0, 0] # W A S D locked = 0, unlockded = 1, no door = 2, escape door = 3, closed escape = 4
        self.treasure = None

    def draw(self, screen, tile_size):
        pygame.draw.rect(screen, self.color, pygame.Rect(20, 20, 680, 680)) 
        # door mats
        door_mat_color = (self.color[0]-30,self.color[1]-30,self.color[2]-30) 
        if self.door_states[0] != 2:
            pygame.draw.rect(screen, door_mat_color, pygame.Rect(292, 20, 136, tile_size))
        if self.door_states[2] != 2:
            pygame.draw.rect(screen, door_mat_color, pygame.Rect(292, 700-68, 136, tile_size))
        if self.door_states[1] != 2:
            pygame.draw.rect(screen, door_mat_color, pygame.Rect(20, 292, tile_size, 136))
        if self.door_states[3] != 2:
            pygame.draw.rect(screen, door_mat_color, pygame.Rect(700-68, 292, tile_size, 136))
        # actual doors
        door_colors = [(0,0,0), (255,255,255), (60,60,60), (0, 255, 100), (255, 50, 0)]
        door_rects = [pygame.Rect(292, 0, 136, 20), pygame.Rect(0, 292, 20, 136), 
                      pygame.Rect(292, 700, 136, 20), pygame.Rect(700, 292, 20, 136)]
        for i in range(4):
            pygame.draw.rect(screen, door_colors[self.door_states[i]], door_rects[i])

    def change_room(self, direction, torches):
        door_index = 0
        match direction:
            case 'u': door_index = 0
            case 'l': door_index = 1
            case 'd': door_index = 2
            case 'r': door_index = 3
        if self.door_states[door_index] == 0: 
            if torches > 0:
                return "remove torch"
            else:
                return "cannot move"
        elif self.door_states[door_index] == 2: 
            return "cannot move"
        elif self.door_states[door_index] == 3:
            return "You are free"
        elif self.door_states[door_index] == 4:
            return "cannot move"