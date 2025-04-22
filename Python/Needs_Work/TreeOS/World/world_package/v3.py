import math
import pygame

screen = pygame.display.set_mode((600, 600))
FPS = 60
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font("Comfortaa.ttf", 15)

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"Point Info: {self.x, self.y, self.z}"

class Camera:
    def __init__(self, xyz, theta):
        self.point = Point(xyz[0], xyz[1], xyz[2])
        self.angle = Point(theta[0], theta[1], theta[2])

    def __str__(self):
        return f"Camera Info\n\tPos: {self.point}\n\tAngle: {self.angle}"
    
    def show_pos(self):
        text = font.render(f"Pos: x: {camera.point.x:.2f}, y: {camera.point.y:.2f}, z: {camera.point.z:.2f}", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (20, 10)
        screen.blit(text, textRect.center)
        text = font.render(f"Ang: x: {camera.angle.x:.2f}, y: {camera.angle.y:.2f}, z: {camera.angle.z:.2f}", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (20, 30)
        screen.blit(text, textRect.center)

    def move(self, theta, amount=0.02):
        direction = math.pi/2 - self.angle.y + theta
        # calculate the triangle of movement based on our angle theta in radians
        dx = math.cos(direction)
        dz = math.sin(direction)
        # change the position based on that change times the length of our difference
        self.point.x += dx * amount
        self.point.z += dz * amount

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
    if dz <= 0:
        dz = 0.001
    # now we need to find our 'b' values, which are the points projected to the screen.
    # size is the screen size, r is the 'recording surface'
    size_x, size_y = screen.get_width()//2, screen.get_height()//2
    recording_x, recording_y, recording_z = screen.get_width()//100, screen.get_height()//100, 10
    bx = (dx*size_x)/(dz*recording_x)*recording_z
    by = (dy*size_y)/(dz*recording_y)*recording_z
    return (bx+size_x,by+size_y)

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
camera = Camera((0.5,0,-1), (0,0,0))
w_held, a_held, s_held, d_held = False, False, False, False
left_held, right_held, up_held, down_held = False, False, False, False

running = True
while running:
    screen.fill((0,0,0))
    draw_cube(camera)
    camera.show_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_w: w_held = True 
                case pygame.K_s: s_held = True 
                case pygame.K_a: a_held = True  
                case pygame.K_d: d_held = True 
                case pygame.K_LEFT: left_held = True 
                case pygame.K_RIGHT: right_held = True 
                case pygame.K_UP: up_held = True  
                case pygame.K_DOWN: down_held = True 
                case pygame.K_ESCAPE: running = False
        if event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_w: w_held = False
                case pygame.K_s: s_held = False 
                case pygame.K_a: a_held = False
                case pygame.K_d: d_held = False
                case pygame.K_LEFT: left_held = False
                case pygame.K_RIGHT: right_held = False 
                case pygame.K_UP: up_held = False
                case pygame.K_DOWN: down_held = False 
    if w_held: camera.move(0)
    if s_held: camera.move(math.pi)
    if a_held: camera.move(math.pi/2)
    if d_held: camera.move(-math.pi/2)
    if up_held: camera.angle.x += 0.02
    if down_held: camera.angle.x -= 0.02
    if left_held: camera.angle.y -= 0.02
    if right_held: camera.angle.y += 0.02
    pygame.display.update()
    clock.tick(FPS)