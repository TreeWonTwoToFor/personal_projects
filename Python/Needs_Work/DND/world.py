import pygame

FPS = 120
clock = pygame.time.Clock()

screen = pygame.display.set_mode((750, 750), pygame.RESIZABLE)

grid = 100
grid_scroll_speed = 5

def draw_lines():
    screen.fill((255,255,255))
    x = 0
    while (x < screen.get_size()[0]):
        x += grid
        pygame.draw.line(screen, (0,0,0), (x,0), (x,screen.get_size()[1]), 3)
        pygame.draw.line(screen, (0,0,0), (0,x), (screen.get_size()[0],x), 3)

def update():
    global grid
    draw_lines()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEWHEEL:
            if event.y == 1: # scroll up
                if grid < 100:
                    grid += grid_scroll_speed
            elif event.y == -1: # scroll down
                if grid > 25:
                    grid -= grid_scroll_speed
    clock.tick()
    pygame.display.update()
