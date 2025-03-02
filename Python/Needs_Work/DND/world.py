import pygame

FPS = 120
clock = pygame.time.Clock()

screen = pygame.display.set_mode((750, 750), pygame.RESIZABLE)

grid = 100
grid_scroll_speed = 5
current_position = [0,0]

def draw_lines():
    screen.fill((255,255,255))
    x = 0
    while (x < screen.get_size()[0]):
        x += grid
        top = (x + current_position[0],current_position[1])
        side = (current_position[0],x + current_position[1])
        pygame.draw.line(screen, (0,0,0), top, (top[0],screen.get_size()[1]+current_position[1]), 3)
        pygame.draw.line(screen, (0,0,0), side, (screen.get_size()[0],side[1]), 3)
        pygame.draw.circle(screen, (255,0,0), top, (10))
        pygame.draw.circle(screen, (255,0,0), side, (10))


def update():
    global grid
    draw_lines()
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                pygame.quit()
            case pygame.MOUSEWHEEL:
                if event.y == 1: # scroll up
                    if grid < 100:
                        grid += grid_scroll_speed
                elif event.y == -1: # scroll down
                    if grid > 25:
                        grid -= grid_scroll_speed
            case pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    current_position[0] -= 10
        
    clock.tick()
    pygame.display.update()
