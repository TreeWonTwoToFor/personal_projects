import math
import pygame

screen = pygame.display.set_mode((500, 500))
FPS = 60
clock = pygame.time.Clock()

print(screen.get_size())

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"Point Info: {self.x, self.y, self.z}"

class Camera:
    def __init__(self, xyz, theta):
        self.x = xyz[0]
        self.y = xyz[1]
        self.z = xyz[2]
        self.point = Point(self.x, self.y, self.z)
        self.angle = Point(theta[0], theta[1], theta[2])

    def __str__(self):
        return f"Camera Info\n\tPos: {self.point}\n\tAngle: {self.angle}"

# Functions for 3d manipulations

def rotate_object(player_position, object_position, d_theta):
    # uses two 2d points and a change in rotation (radians) to return a point rotated about the player

    x = object_position[0] - player_position[0]
    y = math.fabs(object_position[1] - player_position[1])
    distance = math.sqrt(
        math.pow(x,2) + math.pow(y,2)
    )
    if x != 0: # avoiding a divide by 0 error
        theta = math.atan2(y, x)
    else:
        theta = -math.atan2(y, 1) # this negative is a little sus
    new_position = (math.cos(theta+d_theta)*distance+player_position[0], math.sin(theta+d_theta)*distance+player_position[1])
    return new_position

def perspective_projection(projected_point, camera_point, camera_orientation):
    # the algebreic representation of the matrix multiplication

    # redefining our list inputs into points/vectors with names that align with wikipedia
    a = Point(projected_point[0], projected_point[1], projected_point[2])
    c = camera_point
    theta = camera_orientation
    # now we need to find the 'd' values, aka a vector that will intersect with the image surface
    # before we find the d values, let's match the variable names on the page
    cx, cy, cz = math.cos(theta.x), math.cos(theta.y), math.cos(theta.z)
    sx, sy, sz = math.sin(theta.x), math.sin(theta.y), math.sin(theta.z)
    x, y, z = (a.x-c.x), (a.y-c.y), (a.z-c.z)
    # now let's find our 3 d values
    dx = cy*(sz*y + cz*x) - sy*z
    dy = sx*(cy*z + sy*(sz*y + cz*x)) + cx*(cz*y - sz*x)
    dz = cx*(cy*z + sy*(sz*y + cz*x)) - sx*(cz*y - sz*x)
    # now we need to find our 'b' values, which are the points projected to the screen.
    # size is the screen size, r is the 'recording surface'
    size_x, size_y = screen.get_width()//2, screen.get_height()//2
    recording_x, recording_y, recording_z = 3, 3, 10
    bx = (dx*size_x)/(dz*recording_x)*recording_z
    by = (dy*size_y)/(dz*recording_y)*recording_z
    return (bx+screen.get_width()//2,by+screen.get_height()//2)

def draw_pt(coords, color):
    # this is imply to help make it easier to quickly draw a point
    pygame.draw.circle(screen, color, coords, 2)

def draw_cube(camera):
    # draws a specific cube out using the global "camera" variable
    points_list = [
        perspective_projection((0,0,0), camera.point, camera.angle),
        perspective_projection((0,0,1), camera.point, camera.angle),
        perspective_projection((0,1,0), camera.point, camera.angle),
        perspective_projection((0,1,1), camera.point, camera.angle),
        perspective_projection((1,0,0), camera.point, camera.angle),
        perspective_projection((1,0,1), camera.point, camera.angle),
        perspective_projection((1,1,0), camera.point, camera.angle),
        perspective_projection((1,1,1), camera.point, camera.angle)
    ]
    for point in points_list:
        draw_pt(point, (255, 255, 255))
    for i in range(len(points_list)):
        for j in range(len(points_list)):
            if not i <= j:
                pygame.draw.line(screen, (255, 255, 255), points_list[i], points_list[j])

# general global camera
camera = Camera((0,0,-5), (0,0,0))

running = True
while running:
    screen.fill((0,0,0))
    draw_cube(camera)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_a: camera.point.x -= 0.5
                case pygame.K_d: camera.point.x += 0.5
                case pygame.K_w: camera.point.z += 0.5
                case pygame.K_s: camera.point.z -= 0.5
                case pygame.K_LEFT: camera.angle.y -= 0.05
                case pygame.K_RIGHT: camera.angle.y += 0.05
                case pygame.K_UP: camera.angle.x += 0.05
                case pygame.K_DOWN: camera.angle.x -= 0.05
    pygame.display.update()
    clock.tick(FPS)