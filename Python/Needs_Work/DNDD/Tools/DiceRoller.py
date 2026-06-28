import random
import pygame

pygame.font.init()

font = pygame.font.Font(".../../../Comfortaa.ttf", 50)

class Dice:
    def __init__(self, num_sides):
        self.num_sides = num_sides

    def roll(self):
        return random.randint(1, self.num_sides)

def run(canvas):
    logic_output = logic()
    draw(canvas, logic_output)

def draw(canvas, logic_output):
    canvas.fill([100]*3)
    canvas_size = canvas.get_size()
    text_location = canvas_size[0]//2, canvas_size[1]//2
    text = font.render(str(logic_output), True, (255, 255, 255))
    canvas.blit(text, text_location)

def logic():
    dice_to_roll = [Dice(20)]
    total = 0
    for die in dice_to_roll:
        value = die.roll()
        print(value)
        total += value
    return total