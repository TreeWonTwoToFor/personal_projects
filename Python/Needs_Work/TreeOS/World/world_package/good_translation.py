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
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.t = 0

    def __str__(self):
        return (f"{self.x} {self.y} {self.z} \n{self.z}")

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
            x_projected = ((self.z + point.z) * (point.x + self.x))
            y_projected = ((self.z + point.z) * (point.y - self.y))
        else:
            x_projected = ((self.z + point.z) * (point.x + self.x))/(self.z + (point.z))
            y_projected = ((self.z + point.z) * (point.y - self.y))/(self.z + (point.z))
        return (screenX/2+x_projected, screenY/2-y_projected, can_draw)
    
    def get_projected_angle(self, point, theta):
        player_pos = (self.x, self.z)
        object_pos = (point.x, point.z)
        new_object_pos = self.rotate_object(player_pos, object_pos, theta)
        # we say "coords" here because it's not a point object.
        new_pt_coords = (new_object_pos[0], point.y, new_object_pos[1])
        can_draw = True
        if (self.z + point.z) < 0:
            can_draw = False
        if (self.z + point.z) <= 0:
            x_projected = ((self.z + point.z) * (new_pt_coords[0] + self.x))
            y_projected = ((self.z + point.z) * (new_pt_coords[1] - self.y))
        else:
            x_projected = ((self.z + point.z) * (new_pt_coords[0] + self.x))/((self.z) + (new_pt_coords[2]))
            y_projected = ((self.z + point.z) * (new_pt_coords[1] - self.y))/((self.z) + (new_pt_coords[2]))
        return (screenX/2+x_projected, screenY/2-y_projected, can_draw)
    
    # checks to see if the two projection systems are the same when theta is zero
    def test_projections(self, point):
        # Standard projection
        can_draw = True
        #point.z = point.z * out_z
        # projected = (Focal Length * axis)/(Focal Length + depth)
        if (self.z + point.z) < 0:
            can_draw = False
        if (self.z + point.z) <= 0:
            x_proj_std = (self.z * (point.x + self.x))
            y_proj_std = (self.z * (point.y - self.y))
        else:
            x_proj_std = (self.z * (point.x + self.x))/(self.z + (point.z))
            y_proj_std = (self.z * (point.y - self.y))/(self.z + (point.z))
        # Angle Projection
        player_pos = (self.x, self.z)
        object_pos = (point.x, point.z)
        new_object_pos = self.rotate_object(player_pos, object_pos, 0)
        # we say "coords" here because it's not a point object.
        new_pt_coords = (new_object_pos[0], point.y, new_object_pos[1])
        can_draw = True
        if (self.z + point.z) < 0:
            can_draw = False
        if (self.z + point.z) <= 0:
            x_proj_ang = (self.z * (new_pt_coords[0] + self.x))
            y_proj_ang = (self.z * (new_pt_coords[1] - self.y))
        else:
            x_proj_ang = (self.z * (new_pt_coords[0] + self.x))/(self.z + (new_pt_coords[2]))
            y_proj_ang = (self.z * (new_pt_coords[1] - self.y))/(self.z + (new_pt_coords[2]))
        print(f"X: {x_proj_std, x_proj_ang}\nY: {y_proj_std, y_proj_ang}")
        print(f"Diff: {math.fabs(x_proj_std)-math.fabs(x_proj_ang), math.fabs(y_proj_std)-math.fabs(y_proj_ang)}")

    # returns the position of a vertex which has been rotated by the camera
    def rotate_object(self, player_position, object_position, d_theta):
        x = object_position[0] - player_position[0]
        z = math.fabs(object_position[1] - player_position[1])

        distance = math.sqrt(
            math.pow(x,2) + math.pow(z,2)
        )

        # avoiding a divide by 0 error
        if x != 0:
            theta = math.atan2(z, x)
        else:
            theta = -math.atan2(z, 1) # this negative is a little sus

        new_position = (math.cos(theta+d_theta)*distance+player_position[0], math.sin(theta+d_theta)*distance+player_position[1])
        return new_position

class point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def __str__(self):
        return f"{self.x} {self.y} {self.z}"
                
    def move(self, direction, amount):
        match direction:
            case "x": self.x += amount
            case "y": self.y += amount
            case "z": self.z += amount


# Graphics Functions
def draw_point(x, y):
    pygame.draw.circle(screen, (0,0,0), (x, y), 5)

def draw_line(pa, pb):
    # drawing the angle changed object
    #print(game_camera.test_projections(pa))
    print(game_camera)
    pa_projected = game_camera.get_projected_angle(pa, math.pi/12)
    pb_projected = game_camera.get_projected_angle(pb, math.pi/12)
    if not pa_projected[2] and not pb_projected[2]:
        doesnt_draw = True
    else:
        pygame.draw.line(screen, (255,255,255), (pa_projected[0], pa_projected[1]), (pb_projected[0], pb_projected[1]), 2)
    # drawing the acutal projection that we want
    pa_projected = game_camera.get_projected(pa)
    pb_projected = game_camera.get_projected(pb)
    if not pa_projected[2] and not pb_projected[2]:
        doesnt_draw = True
    else:
        pygame.draw.line(screen, (0,0,0), (pa_projected[0], pa_projected[1]), (pb_projected[0], pb_projected[1]), 2)

# Draws the lines for each polygon in the list
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

game_camera = camera()
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
            