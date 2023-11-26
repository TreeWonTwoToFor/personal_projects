import pygame
import game_logic

green = (34, 238, 85)
black = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Cookie Clicker")
font = pygame.font.Font("Comfortaa.ttf", 32)

def take_input(input_text, x, y):
    global text, textRect
    text =  font.render(input_text, True, green, black)
    textRect = text.get_rect()
    textRect.move_ip(x,y)

take_input("something", 100, 100)

visual_terminal = game_logic.terminal

running = True
while running:
    screen.fill(black)
    screen.blit(text, textRect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                output = visual_terminal.read_text("cookies")
                take_input(str(output), 0, 0)
            elif event.key == pygame.K_e:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed(num_buttons=3)[0] == True:
                if pygame.mouse.get_pos()[0] > 1080/2: 
                    visual_terminal.read_text("click")
    pygame.display.update()