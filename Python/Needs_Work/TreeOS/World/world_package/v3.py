import math
import pygame

debug = True
FPS = 60
resolution = (600, 600)

pygame.font.init()
font = pygame.font.Font("Comfortaa.ttf", 15)
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

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
        text = font.render(
            f"Ang: x: {(camera.angle.x*180/math.pi):.2f}, y: {(camera.angle.y*180/math.pi):.2f}, z: {(camera.angle.z*180/math.pi):.2f}", 
            True, (255, 255, 255))
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

    def fix_angles(self):
        if camera.angle.x > math.pi/2:
            camera.angle.x = math.pi/2-0.001
        elif camera.angle.x < -math.pi/2:
            camera.angle.x = -math.pi/2+0.001
        if camera.angle.y > math.pi:
            camera.angle.y -= math.pi*2
        if camera.angle.y < -math.pi:
            camera.angle.y += math.pi*2

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

def draw_from_lines(camera, line_list, offset=(0,0,0)):
    # line_list is just a list of pairs of 3d points
    for line in line_list:
        point_a = perspective_projection((line[0][0]+offset[0],line[0][1]+offset[1],line[0][2]+offset[2]), camera.point, camera.angle)
        point_b = perspective_projection((line[1][0]+offset[0],line[1][1]+offset[1],line[1][2]+offset[2]), camera.point, camera.angle)
        pygame.draw.line(screen, (255, 255, 255), point_a, point_b)

def draw_polygons(camera, p_list, offset=(0,0,0)):
    p_counter = 0
    while p_counter < len(p_list)-2:
        first = (p_list[p_counter][0]+offset[0], p_list[p_counter][1]+offset[1], p_list[p_counter][2]+offset[2]) 
        second = (p_list[p_counter+1][0]+offset[0], p_list[p_counter+1][1]+offset[1], p_list[p_counter+1][2]+offset[2]) 
        third = (p_list[p_counter+2][0]+offset[0], p_list[p_counter+2][1]+offset[1], p_list[p_counter+2][2]+offset[2]) 
        point_a = perspective_projection(first, camera.point, camera.angle)
        point_b = perspective_projection(second, camera.point, camera.angle)
        point_c = perspective_projection(third, camera.point, camera.angle)
        pygame.draw.line(screen, (255, 255, 255), point_a, point_b)
        pygame.draw.line(screen, (255, 255, 255), point_b, point_c)
        pygame.draw.line(screen, (255, 255, 255), point_c, point_a)
        p_counter += 1

def draw_circle(camera):
    angle_change = 10
    angle_conversion = math.pi/(180//angle_change)
    for i in range((360//angle_change)):
        point_a = perspective_projection((math.cos(i*angle_conversion), 1, math.sin((i)*angle_conversion)), camera.point, camera.angle)
        point_b = perspective_projection((math.cos((i+1)*angle_conversion), 1, math.sin((i+1)*angle_conversion)), camera.point, camera.angle)
        pygame.draw.line(screen, (255,255,255), point_a, point_b)

def draw_sphere(camera):
    angle_change = 10
    angle_conversion = math.pi/(180//angle_change)
    for i in range((360//angle_change)):
        point_a = perspective_projection((math.cos(i*angle_conversion), 1, math.sin((i)*angle_conversion)), camera.point, camera.angle)
        point_b = perspective_projection((math.cos((i+1)*angle_conversion), 1, math.sin((i+1)*angle_conversion)), camera.point, camera.angle)
        pygame.draw.line(screen, (255,255,255), point_a, point_b)
    for i in range((360//angle_change)):
        point_a = perspective_projection((0, math.cos(i*angle_conversion)+1, math.sin((i)*angle_conversion)), camera.point, camera.angle)
        point_b = perspective_projection((0, math.cos((i+1)*angle_conversion)+1, math.sin((i+1)*angle_conversion)), camera.point, camera.angle)
        pygame.draw.line(screen, (255,255,255), point_a, point_b)
    for i in range((360//angle_change)):
        point_a = perspective_projection((math.cos(i*angle_conversion), math.sin((i)*angle_conversion)+1, 0), camera.point, camera.angle)
        point_b = perspective_projection((math.cos((i+1)*angle_conversion), math.sin((i+1)*angle_conversion)+1, 0), camera.point, camera.angle)
        pygame.draw.line(screen, (255,255,255), point_a, point_b)


cube_lines = [
    ((0,0,0), (1,0,0)),
    ((1,0,0), (1,0,1)),
    ((1,0,1), (0,0,1)),
    ((0,0,1), (0,0,0)),
    ((0,1,0), (1,1,0)),
    ((1,1,0), (1,1,1)),
    ((1,1,1), (0,1,1)),
    ((0,1,1), (0,1,0)),
    ((0,0,0), (0,1,0)),
    ((1,0,0), (1,1,0)),
    ((0,0,1), (0,1,1)),
    ((1,0,1), (1,1,1))
]

cube_points = [
    (0,0,0),
    (0,1,0),
    (1,0,0),
    (1,1,0),
    (1,0,1),
    (1,1,1),
    (0,0,1),
    (0,1,1),
    (0,0,0),
    (0,1,0)
]

# general global camera
camera = Camera((0.5,0,0.5), (0,0,0))
w_held, a_held, s_held, d_held = False, False, False, False
left_held, right_held, up_held, down_held = False, False, False, False

running = True
while running:
    screen.fill((0,0,0))
    #draw_polygons(camera, cube_points, (0, 1, 0))
    #draw_from_lines(camera, sphere_lines, (0, 1, 0))
    draw_sphere(camera)
    camera.fix_angles()
    if debug: camera.show_pos()
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