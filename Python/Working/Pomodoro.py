import pygame
import time

pygame.init()

text_color = (46, 84, 62)
bg_color = (237, 164, 207)

screenX = 300
screenY = 200
FPS = 60
clock = pygame.time.Clock()

pygame.display.set_caption("Pomodoro Timer")
screen = pygame.display.set_mode((screenX, screenY), pygame.RESIZABLE)

font = pygame.font.SysFont("Comfortaa", 100)

pomodoro_timer = 0
start_time, current_time = time.time(), 0
display_time = 0
work_options = [25*60+1, 5*60+1]

def color_swap():
    global text_color, bg_color
    third = list(text_color)
    text_color = bg_color
    bg_color = third

running = True
while running:
    screen.fill(bg_color)
    current_time = time.time()
    display_time = int(work_options[0] - (current_time - start_time))
    if display_time < 0:
        text = font.render("0:00", True, text_color)
        text_rect = text.get_rect(center=screen.get_rect().center)
        screen.blit(text, text_rect)
    else:
        minutes = display_time//60
        seconds = display_time%60
        seconds_string = str(seconds)
        if len(seconds_string) == 1: seconds_string = "0" + seconds_string
        text = font.render(str(minutes) + ":" + seconds_string, True, text_color)
        text_rect = text.get_rect(center=screen.get_rect().center)
        screen.blit(text, text_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # print(mouse_pos)
            # color_swap()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and display_time < 0:
                start_time = time.time()
                work_options.reverse()
                color_swap()
    pygame.display.update()
    clock.tick(FPS)