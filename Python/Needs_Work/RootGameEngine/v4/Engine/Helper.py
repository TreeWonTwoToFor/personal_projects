import math
import pygame

def array_dp(array_a, array_b):
    if len(array_a) != len(array_b): 
        raise ValueError(f"cannot perform dp between {array_a} and {array_b}")
    dp = sum([array_a[i] * array_b[i] for i in range(len(array_a))])
    return dp

def vector_magnitude(vector):
    value = math.sqrt(sum([x ** 2 for x in vector]))
    if value == 0:
        return 0.001
    return value

# General drawing functions
def draw_pt(screen, coords, color):
    pygame.draw.circle(screen, color, coords, 2)

def draw_3d_point(screen, point, color, camera):
    new_point = perspective_projection(
        screen, point, camera)[0]
    draw_pt(screen, new_point, color)

def draw_3d_line(screen, point_a, point_b, color, camera):
    new_point_a = perspective_projection(
        screen, point_a, camera)[0]
    new_point_b = perspective_projection(
        screen, point_b, camera)[0]
    draw_pt(screen, new_point_a, color)
    draw_pt(screen, new_point_b, color)
    pygame.draw.line(screen, color, new_point_a, new_point_b)

def perspective_projection(screen, projected_point, camera):
    screen_resolution = screen.get_size()
    # redefining our list inputs into points/vectors with names that align with wikipedia
    a = projected_point
    c = camera.point
    theta = camera.angle
    # now we need to find the 'd' values, aka a vector that will intersect with the image surface
    # before we find the d values, let's match the variable names on the page
    cx, cy, cz = math.cos(theta[0]), math.cos(theta[1]), math.cos(theta[2])
    sx, sy, sz = math.sin(theta[0]), math.sin(theta[1]), math.sin(theta[2])
    x, y, z = (a[0]-c[0]), (a[1]-c[1]), (a[2]-c[2])
    # now let's find our 3 d values
    dx = cy*(sz*y + cz*x) - sy*z
    dy = sx*(cy*z + sy*(sz*y + cz*x)) + cx*(cz*y - sz*x)
    dz = cx*(cy*z + sy*(sz*y + cz*x)) - sx*(cz*y - sz*x)
    if dz <= 0:
        dz = 0.001
    # now we need to find our 'b' values, which are the points projected to the screen.
    # size is the screen size, r is the 'recording surface'
    size_x, size_y = screen_resolution[0]//2, screen_resolution[1]//2
    recording_x, recording_y, recording_z = screen_resolution[0]//100, screen_resolution[1]//100, 10
    bx = (dx*size_x)/(dz*recording_x)*recording_z
    by = (dy*size_y)/(dz*recording_y)*recording_z
    # bx and by need to be centered to the screen instead of 0,0
    # dz included for depth buffering
    return ((bx+size_x,size_y-by), dz)
