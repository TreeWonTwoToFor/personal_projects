import random
import pygame

application_name = "DiceRoller"

pygame.font.init()

font = pygame.font.Font("../Comfortaa.ttf", 50)

background_color = (100, 100, 100)
text_color = (255,255,255)

class Dice:
    def __init__(self, num_sides):
        self.num_sides = num_sides

    def roll(self):
        return random.randint(1, self.num_sides)

def run(canvas_dict, desktop_instruction):
    canvas = canvas_dict[application_name].surface
    logic_output = logic()
    draw(canvas, logic_output)

def draw(canvas, logic_output):
    canvas.fill(background_color)
    canvas_size = canvas.get_size()
    text = font.render(str(logic_output), True, text_color)
    text_location = canvas_size[0]//2-text.get_size()[0]//2, canvas_size[1]//2-text.get_size()[1]//2
    canvas.blit(text, text_location)

def logic():
    dice_to_roll = [Dice(20)]
    total = 0
    for die in dice_to_roll:
        value = die.roll()
        total += value
    return total
