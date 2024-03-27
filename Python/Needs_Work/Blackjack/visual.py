import pygame

pygame.init()

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Blackjack")

shoe_card = pygame.Rect(10, 10, 100, 150)
card = pygame.Rect(375, 325, 100, 150)

table_green = (30, 150, 50)
off_white = (220, 220, 220)
card_backing = (60, 100, 250)
outline = (25, 25, 25)
chip_red = (200, 50, 50)
box_yellow = (200, 200, 0)


font = pygame.font.Font('Comfortaa-VariableFont_wght.ttf', 50)
text = font.render('J', True, (255, 0, 0), off_white)
textRect = text.get_rect()
textRect.center = card.center

def draw_card(card, isDown):
    inner_rect = pygame.Rect(card.x+5, card.y+5, card.width-10, card.height-10)
    pygame.draw.rect(screen, outline, card)
    if isDown:
        pygame.draw.rect(screen, card_backing, inner_rect)
    else:
        pygame.draw.rect(screen, off_white, inner_rect)
    
def draw_chips():
    pygame.draw.ellipse(screen, outline, pygame.Rect(50, 450, 100, 75))
    pygame.draw.ellipse(screen, chip_red, pygame.Rect(55, 455, 90, 65))

def draw_boxes():
    # betting box
    pygame.draw.rect(screen, box_yellow, pygame.Rect(37, 207, 125, 125))
    pygame.draw.rect(screen, table_green, pygame.Rect(50, 220, 100, 100))
    # shoe
    pygame.draw.rect(screen, outline, pygame.Rect(0, 5, 60, 160))


running = True
while running:
    screen.fill(table_green)
    draw_card(shoe_card, True)
    draw_card(card, False)
    draw_chips()
    draw_boxes()
    screen.blit(text, textRect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()