import pygame
import time
from os import system

pygame.init()

screenX = 1080
screenY = 720
bg_color = (255, 255, 255)
FPS = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode((screenX, screenY), pygame.RESIZABLE)
font = pygame.font.SysFont("Comfortaa", 50)

c_l = []
instruction_list = [
    "The quick brown fox jumps over the lazy dog.",
    "When I am happy, I laugh."
]
next_letter = ""
DAS, instruction, frame, offset = 0, 0, 0, 0
holding_back, holding_shift = False, False
to_type_list = list(instruction_list[instruction])
timer = 0
system("cls")

running = True
while running:
    screen.fill(bg_color)
    frame += 1
    if frame > 60:
        frame = 0
    character_string = ""
    to_type_string = ""
    next_letter = ""
    for letter in c_l:
        character_string += letter
    if frame/60 < 0.6:
        character_string += "|"
    for letter in to_type_list:
        to_type_string += letter
    if character_string.__len__() > 50:
        offset = (character_string.__len__()-50)*15
        if frame/60 < 0.6: offset -= 15
    text = font.render(character_string, True, (0,0,0))
    screen.blit(text, (20-offset, screenY-60))
    text = font.render(to_type_string, True, (0,0,0))
    screen.blit(text, (20, 20))
    text = font.render(str(round(timer, 2)), True, (0,0,0))
    screen.blit(text, (screenX/2, screenY/2))
    pygame.draw.line(screen, (0, 0, 200), (0, screenY-23), (screenX, screenY-23), 3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_a: next_letter = "a"
                case pygame.K_b: next_letter = "b"
                case pygame.K_c: next_letter = "c"
                case pygame.K_d: next_letter = "d"
                case pygame.K_e: next_letter = "e"
                case pygame.K_f: next_letter = "f"
                case pygame.K_g: next_letter = "g"
                case pygame.K_h: next_letter = "h"
                case pygame.K_i: next_letter = "i"
                case pygame.K_j: next_letter = "j"
                case pygame.K_k: next_letter = "k"
                case pygame.K_l: next_letter = "l"
                case pygame.K_m: next_letter = "m"
                case pygame.K_n: next_letter = "n"
                case pygame.K_o: next_letter = "o"
                case pygame.K_p: next_letter = "p"
                case pygame.K_q: next_letter = "q"
                case pygame.K_r: next_letter = "r"
                case pygame.K_s: next_letter = "s"
                case pygame.K_t: next_letter = "t"
                case pygame.K_u: next_letter = "u"
                case pygame.K_v: next_letter = "v"
                case pygame.K_w: next_letter = "w"
                case pygame.K_x: next_letter = "x"
                case pygame.K_y: next_letter = "y"
                case pygame.K_z: next_letter = "z"
                case pygame.K_PERIOD: next_letter = "."
                case pygame.K_COMMA: next_letter = ","
                case pygame.K_MINUS: next_letter = "-"
                case pygame.K_BACKSPACE: holding_back = True
                case pygame.K_SPACE: next_letter = " "
                case pygame.K_LSHIFT: holding_shift = True
                case pygame.K_ESCAPE: running = False
                case pygame.K_RETURN: 
                    c_l = []
                    timer = 0.0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE: holding_back = False
            if event.key == pygame.K_LSHIFT: holding_shift = False
    if holding_shift:
        next_letter = next_letter.upper()
    if next_letter != "":
        c_l.append(next_letter)
    if holding_back:
        DAS += 1
    if (DAS == 1 or (DAS > 30 and DAS % 15)) and len(c_l) > 0:
        c_l.pop()
    if not holding_back:
        DAS = 0
    if not(len(character_string) == 0 or character_string == "|"):
        timer += 0.016666
    if (to_type_string == character_string or to_type_string + "|" == character_string):
        instruction += 1
        c_l = []
        print(timer)
        timer = 0
        to_type_list = list(instruction_list[instruction])
    pygame.display.update()
    clock.tick(FPS)