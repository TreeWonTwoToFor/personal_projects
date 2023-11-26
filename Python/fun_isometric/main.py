import math
import pygame
import os
import time

os.system('cls')

pygame.init()
screen = pygame.display.set_mode((1000, 850), pygame.RESIZABLE)

display_style = 0
start_pos = (0, 0)
pan_active = False
pan_speed = 1
x_diff = 0
y_diff = 0

cube_x = screen.get_width()/2
cube_y = screen.get_height()/2
plane_x = cube_x
plane_y = cube_y

black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 70)
blue = (0, 0, 200)

hex_len = 50
hex_width = abs(hex_len*math.sin(30))

def draw_pt(color, x, y):
    pygame.draw.circle(screen, color, [x, y], 5, 20)

def draw_ln(color, x1, y1, x2, y2):
    pygame.draw.line(screen, color, [x1, y1], [x2, y2], 3) 

def draw_poly(color, x1, y1, x2, y2, x3, y3, x4, y4):
    pygame.draw.polygon(screen, color, [[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

def draw_hex(color, x, y, shaded):
    pain_len = math.sin(30)
    hex_array = [[x, y], [x, y+hex_len], [x, y-hex_len], [x+(hex_len*pain_len), y-(hex_len*0.5)], [x-(hex_len*pain_len), y-(hex_len*0.5)], [x+(hex_len*pain_len), y+(hex_len*0.5)], [x-(hex_len*pain_len), y+(hex_len*0.5)]]
    ln_array = [[1,2], [1,4], [1,5], [2,6], [2,7], [3,4], [3,5], [4,6], [5,7]]
    for i in range(0, len(ln_array)):
        pt1 = ln_array[i][0]-1
        pt2 = ln_array[i][1]-1
        draw_ln(color, hex_array[pt1][0], hex_array[pt1][1], hex_array[pt2][0], hex_array[pt2][1])
    if shaded:
        draw_poly((86, 171, 58), hex_array[0][0], hex_array[0][1], 
              hex_array[4][0], hex_array[4][1], 
              hex_array[2][0], hex_array[2][1], 
              hex_array[3][0], hex_array[3][1]) # top
        draw_poly((202, 126, 42), hex_array[0][0], hex_array[0][1], 
              hex_array[1][0], hex_array[1][1], 
              hex_array[5][0], hex_array[5][1], 
              hex_array[3][0], hex_array[3][1]) # left
        draw_poly((141, 86, 20), hex_array[0][0], hex_array[0][1], 
              hex_array[1][0], hex_array[1][1], 
              hex_array[6][0], hex_array[6][1], 
              hex_array[4][0], hex_array[4][1]) # right

def screen_test(row, col, x, y, shaded):
    for j in range(0, row):
        if j%2 == 0:
            for i in range(0, col):
                draw_hex(black, x+(i*2)*(hex_width), y+hex_len*1.5*j, shaded)
        else:
            for i in range(0, col-1):
                draw_hex(black, x+(i*2+1)*(hex_width), y+hex_len*1.5*j, shaded)

def draw_back_to_front(color, row, x, y, shaded):
    for j in range(0, row):
        difference = int(j/2)
        for i in range(0, row-(2*difference)):
            btf_equation_y = y + (hex_len*(1.5*i))+ 3*difference*hex_len
            btf_equation_x = x + i * hex_width 
            draw_hex(color, btf_equation_x, btf_equation_y, shaded)
            btf_equation_x = x - i * hex_width
            draw_hex(color, btf_equation_x, btf_equation_y, shaded)

def anime():
    for i in range(1,100):
        global hex_len
        time.sleep(0.05)
        screen.fill(green)
        hex_len = i
        draw_hex(black, screen.get_width()/2, screen.get_height()/2)
        pygame.display.update()

def cube(color, x_count, y_count, z_count, plane, shaded):
    if plane:
        x_count = 100
        y_count = 100
        z_count = 1
    x = screen.get_width()/2
    y = screen.get_height()/2- (hex_len*y_count/2) + (hex_len*z_count)
    draw_hex(color, x, y, shaded)
    for k in range(0, x_count):
        for j in range(0, y_count):
            for i in range(0, z_count):
                imod = i*hex_len
                jmod = j*hex_len
                kmod = k*hex_len
                xjmod = j*hex_width
                xkmod = k*hex_width
                draw_hex(color, x+xjmod-xkmod, y-imod+jmod*0.5+kmod*0.5, shaded)

running = True
while running:
    hex_width = abs(hex_len*math.sin(30))
    screen.fill(black)
    if display_style == 0: # one cube
        draw_hex(black, cube_x, cube_y, 1)
    elif display_style == 1: # grid
        screen_test(50, 50, 0, 0, 1)
    elif display_style == 2: # triangle
        draw_back_to_front(black, 7, screen.get_width()/2, hex_len, 1)
    elif display_style == 3: # cube/plane
        cube(black, 5, 5, 5, 0, 1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            if event.dict.get('y') > 0:
                hex_len = hex_len**1.02
            else:
                hex_len = hex_len**(1/1.02)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and display_style < 3:
                display_style += 1
            if event.button == 3 and display_style > 0:
                display_style -= 1
            if event.button == 2:
                pan_active = True
                last_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                pan_active = False
    if pan_active == True:
        current_pos = pygame.mouse.get_pos()
        x_diff = current_pos[0]-last_pos[0]
        y_diff = current_pos[1]-last_pos[1]
        cube_x += x_diff
        cube_y += y_diff
        plane_x += x_diff
        plane_y += y_diff
        last_pos = pygame.mouse.get_pos()
    pygame.display.update()