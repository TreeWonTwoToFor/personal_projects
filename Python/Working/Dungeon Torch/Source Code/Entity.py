import pygame
import math
import random

class Entity():
    def __init__(self, x, y, color, image=None):
        self.x = x
        self.y = y
        self.sub_x = 0
        self.sub_y = 0
        self.color = color
        self.image = image
        self.alive = True
        self.is_treasure = False
        self.is_player = False
        self.direction = 'u'
        self.move_timer = 0
        self.sword_timer = 0
        self.sword_color = 175
        if image != None: 
            self.is_treasure = True

    def distance(self, entity):
        return math.sqrt((entity.x - self.x)**2 + (entity.y - self.y)**2)
    
    def die(self, torches, screen, count):
        self.alive = False
        output = 0
        if self.is_treasure:
            new_image = pygame.transform.scale(self.image, (103, 103))
            position = (982, 398)
            match count:
                case 1: position = (982 + 138, 398) 
                case 2: position = (982, 398+ 138) 
                case 3: position = (982 + 138, 398 + 138) 
            screen.blit(new_image, position)
            count = count + 1
        else:
            output = random.randint(0,2)
        return (torches + output, count)
    
    def tile_in_direction(self):
        tile = [self.x, self.y]
        match self.direction:
            case 'u':
                tile[1] -= 1
            case 'd':
                tile[1] += 1
            case 'l':
                tile[0] -= 1
            case 'r':
                tile[0] += 1
        return tile

    def move_enemy(self, direction, tile_size, door_list=[]):
        if not self.is_treasure:
            self.direction = direction
            move_threshold = 40
            out_of_bounds = 0
            if self.is_player: move_threshold = 20
            if self.move_timer >= move_threshold:
                self.move_timer = 0
                match direction:
                    case 'u': 
                        if self.y > 0: self.y -= 1
                        else: out_of_bounds = 1
                    case 'd': 
                        if self.y+1 < 680//tile_size: self.y += 1
                        else: out_of_bounds = 1
                    case 'l': 
                        if self.x > 0: self.x -= 1
                        else: out_of_bounds = 1
                    case 'r': 
                        if self.x+1 < 680//tile_size: self.x += 1
                        else: out_of_bounds = 1
                if out_of_bounds == 1 and (self.x, self.y) in door_list:
                    return direction
            else: self.move_timer += 1
            return None

    def move(self, direction, tile_size, door_list=[]):
        movement_speed = 1
        self.direction = direction
        match direction:
            case 'u': 
                if self.y >= 0: 
                    abs_x = math.fabs(self.sub_x)
                    if self.sub_x == 0 or abs_x == tile_size//8:
                        # we are tile aligned
                        self.sub_y -= movement_speed
                    else:
                        if abs_x < 4:
                            # move in towards a full tile
                            if self.sub_x > 0: self.sub_x -= movement_speed
                            if self.sub_x < 0: self.sub_x += movement_speed
                        else:
                            # move away towards a tile seam
                            if self.sub_x > 0: self.sub_x += movement_speed
                            if self.sub_x < 0: self.sub_x -= movement_speed
            case 'd': 
                if self.y+1 <= 680//tile_size: 
                    abs_x = math.fabs(self.sub_x)
                    if self.sub_x == 0 or abs_x == tile_size//8:
                        # we are tile aligned
                        self.sub_y += movement_speed
                    else:
                        if abs_x < 4:
                            # move in towards a full tile
                            if self.sub_x > 0: self.sub_x -= movement_speed
                            if self.sub_x < 0: self.sub_x += movement_speed
                        else:
                            # move away towards a tile seam
                            if self.sub_x > 0: self.sub_x += movement_speed
                            if self.sub_x < 0: self.sub_x -= movement_speed
            case 'l': 
                if self.x >= 0: 
                    abs_y = math.fabs(self.sub_y)
                    if self.sub_y == 0 or abs_y == tile_size//8:
                        # we are tile aligned
                        self.sub_x -= movement_speed
                    else:
                        if abs_y < 4:
                            # move in towards a full tile
                            if self.sub_y > 0: self.sub_y -= movement_speed
                            if self.sub_y < 0: self.sub_y += movement_speed
                        else:
                            # move away towards a tile seam
                            if self.sub_y > 0: self.sub_y += movement_speed
                            if self.sub_y < 0: self.sub_y -= movement_speed
            case 'r': 
                if self.x+1 <= 680//tile_size: 
                    abs_y = math.fabs(self.sub_y)
                    if self.sub_y == 0 or abs_y == tile_size//8:
                        # we are tile aligned
                        self.sub_x += movement_speed
                    else:
                        if abs_y < 4:
                            # move in towards a full tile
                            if self.sub_y > 0: self.sub_y -= movement_speed
                            if self.sub_y < 0: self.sub_y += movement_speed
                        else:
                            # move away towards a tile seam
                            if self.sub_y > 0: self.sub_y += movement_speed
                            if self.sub_y < 0: self.sub_y -= movement_speed
        if (self.x, self.y) in door_list:
            match direction:
                case 'u':
                    if self.sub_y < 0: 
                        self.sub_y = 0 
                        return direction
                case 'd':
                    if self.sub_y >= 0: 
                        self.sub_y = 0 
                        return direction
                case 'l':
                    if self.sub_x >= 0: 
                        self.sub_x = 0 
                        return direction
                case 'r':
                    if self.sub_x <= 0: 
                        self.sub_x = 0 
                        return direction
        print(f"Global: {self.x}, {self.y}")
        if math.fabs(self.sub_y) > tile_size//8 and (self.y != 0 or self.y != 9):
            if self.sub_y > 0: 
                self.y += 1 
                self.sub_y -= 1
            if self.sub_y < 0: 
                self.y -= 1
                self.sub_y += 1
            self.sub_y = -self.sub_y
        if math.fabs(self.sub_x) > tile_size//8  and (self.x != 0 or self.x != 9):
            if self.sub_x > 0: 
                self.x += 1 
                self.sub_x -= 1
            if self.sub_x < 0: 
                self.x -= 1
                self.sub_x += 1
            self.sub_x = -(self.sub_x)
        print(self.sub_x, self.sub_y)
        return None

    def draw(self, screen, tile_size, offset):
        if not self.is_treasure:
            if self.alive:
                draw_x = self.x * tile_size + offset + self.sub_x * 4
                draw_y = self.y * tile_size + offset + self.sub_y * 4
                pygame.draw.rect(screen, self.color, pygame.Rect(
                    draw_x, draw_y, tile_size, tile_size
                ))
                if self.is_player:
                    color = 175
                    thickness = 9
                    match self.direction:
                        case 'u': 
                            pygame.draw.rect(screen, (color, color, color), pygame.Rect(
                                draw_x, draw_y, tile_size, thickness))
                        case 'd': 
                            pygame.draw.rect(screen, (color, color, color), pygame.Rect(
                                draw_x, draw_y+tile_size-thickness, tile_size, thickness))
                        case 'l': 
                            pygame.draw.rect(screen, (color, color, color), pygame.Rect(
                                draw_x, draw_y, thickness, tile_size))
                        case 'r': 
                            pygame.draw.rect(screen, (color, color, color), pygame.Rect(
                                draw_x+tile_size-thickness, draw_y, thickness, tile_size))
        else:
            draw_x = self.x * tile_size + offset + self.sub_x * 4 + 2
            draw_y = self.y * tile_size + offset + self.sub_y * 4 + 2
            screen.blit(self.image, (draw_x, draw_y))
        if self.sword_timer != 0:
            color = self.sword_color
            draw_x = self.x * tile_size + 20
            draw_y = self.y * tile_size + 20 
            length = 40
            width = 15
            match self.direction:
                case 'u': 
                    if self.y != 0:
                        draw_x += 27
                        draw_y -= 32
                        pygame.draw.rect(screen, (color, color, color), pygame.Rect(
                            draw_x, draw_y, width, length))
                case 'd': 
                    if self.y != 9:
                        draw_x += 27
                        draw_y += 70
                        pygame.draw.rect(screen, (color, color, color), pygame.Rect(
                            draw_x, draw_y, width, length))
                case 'l': 
                    if self.x != 0:
                        draw_x -= length
                        draw_y += 28
                        pygame.draw.rect(screen, (color, color, color), pygame.Rect(
                            draw_x, draw_y, length, width))
                case 'r': 
                    if self.x != 9:
                        draw_x += length + 20
                        draw_y += 28
                        pygame.draw.rect(screen, (color, color, color), pygame.Rect(
                            draw_x, draw_y, length, width))
            self.sword_timer -= 1