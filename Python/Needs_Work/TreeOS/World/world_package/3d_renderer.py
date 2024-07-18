import pygame
import time
import os
import json
import math

pygame.init()

screenX = 1080
screenY = 720
bg_color = (34, 238, 85)
FPS = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode((screenX, screenY), pygame.RESIZABLE)

font = pygame.font.SysFont("comfortaa", 20)

class camera:
    def __init__(self,  FL):
        self.x = 0
        self.y = 0
        self.z = FL
        self.t = 0

    def info(self):
        print(f"{self.x} {self.y} {self.z} \n{self.z}")

    def fix_theta(self):
        while not (self.t > 0 and self.t < 360):
            if self.t > 360:
                self.t = self.t - 360
            if self.t < 0:
                self.t = self.t + 360

    # takes a xyz position and translates it to the screen position
    def get_projected(self, point):
        can_draw = True
        #point.z = point.z * out_z
        # projected = (Focal Length * axis)/(Focal Length + depth)
        if (self.z + point.z) < 0:
            can_draw = False
        if (self.z + point.z) <= 0:
            x_projected = (self.z * (point.x + self.x))
            y_projected = (self.z * (point.y - self.y))
        else:
            x_projected = (self.z * (point.x + self.x))/(self.z + (point.z))
            y_projected = (self.z * (point.y - self.y))/(self.z + (point.z))
        return (screenX/2+x_projected, screenY/2-y_projected, can_draw)
    
    def get_projected_angle(self, point):
        can_draw = True
        out_x,out_z = math.sin(math.radians(self.t)), math.sin(math.radians(self.t))+1
        rotated_x = point.x * out_x
        #point.z = point.z * out_z
        # projected = (Focal Length * axis)/(Focal Length + depth)
        if (self.z + point.z) < 0:
            can_draw = False
        if (self.z + point.z) <= 0:
            x_projected = (self.z * (rotated_x + self.x))
            y_projected = (self.z * (point.y - self.y))
        else:
            x_projected = (self.z * (rotated_x + self.x))/(self.z + (point.z))
            y_projected = (self.z * (point.y - self.y))/(self.z + (point.z))
        out_x,out_y = 1 * math.cos(self.t), 1 * math.sin(self.t)
        #return (screenX/2+x_projected, screenY/2-y_projected, can_draw) - og output 
        return (screenX/2+x_projected, screenY/2-y_projected, can_draw)

class point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def move(self, direction, amount):
        match direction:
            case "x": self.x += amount
            case "y": self.y += amount
            case "z": self.z += amount

    def info(self):
        print(f"{self.x} {self.y} {self.z}")

# Graphics Functions
def draw_point(x, y):
    pygame.draw.circle(screen, (0,0,0), (x, y), 5)

def draw_line(pa, pb):
    pa_projected = game_camera.get_projected(pa)
    pb_projected = game_camera.get_projected(pb)
    if not pa_projected[2] and not pb_projected[2]:
        doesnt_draw = True
    else:
        pygame.draw.line(screen, (0,0,0), (pa_projected[0], pa_projected[1]), (pb_projected[0], pb_projected[1]), 2)

def connect_points(poly_list):
    for poly in poly_list:
        for i in range(len(poly)):
            if i is not len(poly)-1:
                draw_line(poly[i], poly[i+1])
            else:
                draw_line(poly[0], poly[-1])

# takes a json file, and returns a list of polys (lists of points)
def points_from_model(file_name):
    json_file = open(file_name) 
    json_data = json.load(json_file)
    json_index = 1
    mega_point_list = []
    for poly in json_data: # a poly is just a list of x,y,z lists
        poly_point_list = []
        for pt in json_data[str(json_index)]: # pt is just a cordinate in 3d space
            poly_point_list.append(point(pt[0], pt[1], pt[2]))
        json_index += 1
        mega_point_list.append(poly_point_list)
    json_file.close()
    return mega_point_list

def update_poly_lists(model_list, model_index):
    global absolute_poly_list
    global relative_poly_list
    absolute_poly_list, relative_poly_list = points_from_model(model_list[model_index]),points_from_model(model_list[model_index])

def move_points(direction, amount, poly_list):
    for poly in poly_list:
        for point in poly:
            point.move(direction, amount)

game_camera = camera(500)
w_held, s_held, a_held, d_held, j_held = False, False, False, False, False
model_list = ["models//xyz_marker.json", "models//box.json", "models//arcade_machine.json", "models//room.json"]
model_index = 1
update_poly_lists(model_list, model_index)
movement_speed = 240/FPS
is_jumping = False
jump_time = 0

running = True
while running:
    screen.fill(bg_color)
    text = font.render(f"{int(game_camera.x)}, {int(game_camera.y)}, {int(game_camera.z)}", True, (0, 0, 0))
    screen.blit(text, (0, 0))
    connect_points(relative_poly_list)
    """for ply in range(len(absolute_poly_list)):
        for pt in range(len(absolute_poly_list[ply])):
            absolute_poly_list[ply][pt].info()
            relative_poly_list[ply][pt].info()"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print(mouse_pos)
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_TAB: 
                    if model_index is not len(model_list)-1: model_index += 1
                    else: model_index = 0
                    update_poly_lists(model_list, model_index)
                    game_camera.t = 0
                case pygame.K_SPACE:
                    is_jumping = True
                case pygame.K_w: w_held = True 
                case pygame.K_s: s_held = True 
                case pygame.K_a: a_held = True 
                case pygame.K_d: d_held = True 
                case pygame.K_j: j_held = True
                case pygame.K_ESCAPE: running = False
        if event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_SPACE:
                    is_jumping = False
                case pygame.K_w: w_held = False
                case pygame.K_s: s_held = False 
                case pygame.K_a: a_held = False
                case pygame.K_d: d_held = False
                case pygame.K_j: j_held = False
    if w_held: move_points("z", -movement_speed, relative_poly_list) # game_camera.z -= 2
    if s_held: move_points("z", movement_speed, relative_poly_list) # game_camera.z += 2
    if a_held: move_points("x", movement_speed, relative_poly_list) # game_camera.x += 2 
    if d_held: move_points("x", -movement_speed, relative_poly_list) # game_camera.x -= 2
    if j_held: game_camera.t += 1
    if is_jumping or jump_time != 0:
        if jump_time <= FPS/3:
            game_camera.y = math.pow((jump_time-(FPS/6)), 2) * (-1/((1/900)*math.pow(FPS,2)))+25
            jump_time += 1
        else:
            is_jumping = False
            jump_time = 0
            game_camera.y = 0
    pygame.display.update()
    clock.tick(FPS)
            