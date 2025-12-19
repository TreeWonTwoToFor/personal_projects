import pygame
import math

from Engine import Parser
from Engine import Object

pygame.font.init()
font = pygame.font.Font("./Assets/Comfortaa.ttf", 15)
move_speed = 0.05

def radians_to_degrees(radians):
    return radians * (180/math.pi)

def degrees_to_radians(degrees):
    return degrees * (math.pi/180)

class Camera:
    def __init__(self, xyz, theta, is_parser=False):
        theta = list(theta)
        for i in range(len(theta)):
            theta[i] = degrees_to_radians(theta[i])
        self.point = [xyz[0], xyz[1], xyz[2]]
        self.angle = theta

        if not is_parser:
            # setting up the player's collision
            player_box = Object.Object(Parser.get_model("./Assets/Objects/cube.obj"), ["camera"]*6)
            player_box.translate([self.point[0], self.point[1]-0.5, self.point[2]])
            self.bounding_box = player_box
            self.bounding_box.scale([0.2, 0.7, 0.2])

        # setup movement stuff
        self.movement_type = "absolute"

    def __str__(self):
        return f"Camera Info\n\tPos: {self.point}\n\tAngle: {self.angle}"
    
    def show_pos(self, screen, fps):
        # like cl_showpos from portal.
        text = font.render(f"Pos: x: {self.point[0]:.2f}, y: {self.point[1]:.2f}, z: {self.point[2]:.2f}", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (20, 10)
        screen.blit(text, textRect.center)
        text = font.render(
            f"Ang: x: {radians_to_degrees(self.angle[0]):.2f}, y: {radians_to_degrees(self.angle[1]):.2f}, z: {radians_to_degrees(self.angle[2]):.2f}", 
            True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (20, 30)
        screen.blit(text, textRect.center)
        text = font.render(
            f"FPS: {fps}",
            True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (20, 50)
        screen.blit(text, textRect.center)

    def fix_angles(self):
        # if angles are outside of normal bounds, we want to fix them up.
        if self.angle[0] > degrees_to_radians(90):
            self.angle[0] = degrees_to_radians(90)
        elif self.angle[0] < -degrees_to_radians(90):
            self.angle[0] = -degrees_to_radians(90)
        if self.angle[1] > degrees_to_radians(180):
            self.angle[1] -= degrees_to_radians(360)
        elif self.angle[1] < -degrees_to_radians(180):
            self.angle[1] += degrees_to_radians(360)

    def move_direction(self, theta, amount=move_speed):
        direction = degrees_to_radians(90) - self.angle[1] + theta
        # calculate the triangle of movement based on our angle theta in radians
        dx = math.cos(direction)
        dz = math.sin(direction)
        # change the position based on that change times the length of our difference
        self.point[0] += dx * amount
        self.point[2] += dz * amount
        self.bounding_box.translate([self.point[0] + dx*amount, 0, self.point[2] + dz*amount])

    def move_vertically(self, up_or_down, amount=move_speed):
        dy = 0
        match up_or_down:
            case "up":   dy = amount
            case "down": dy = -amount
        self.point[1] += dy
        self.bounding_box.translate([0, dy, 0])
