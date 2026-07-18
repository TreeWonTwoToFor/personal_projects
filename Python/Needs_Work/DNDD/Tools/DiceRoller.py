import random
import pygame

application_name = "DiceRoller"
application_icon = "./icons/dice_icon.png"

background_color = (100, 100, 100)
canvas = None
clicking = False

pygame.font.init()
font_size = 50
font = pygame.font.Font("../Comfortaa.ttf", font_size)
text_color = (255,255,255)
button_color = (50,50,50)

class Dice:
    def __init__(self, num_sides):
        self.num_sides = num_sides

    def __str__(self):
        return str(self.num_sides)

    def roll(self):
        return random.randint(1, self.num_sides)

def run_once():
    global total, dice_to_roll, button_dict
    total = 0
    dice_to_roll = []
    button_dict = {}

def run(window_dict, desktop_instruction):
    global canvas
    canvas = window_dict[application_name].surface
    if desktop_instruction is not None:
        event_type, event_details = desktop_instruction[0], desktop_instruction[1]
    else:
        event_type = None
        event_details = [None]
    logic(event_type, event_details)
    draw()

def draw():
    canvas.fill(background_color)
    canvas_size = canvas.get_size()
    # write down the total value
    text = font.render(str(total), True, text_color)
    text_location = canvas_size[0]//2-text.get_size()[0]//2, canvas_size[1]//2-text.get_size()[1]//2
    canvas.blit(text, text_location)
    # write down the current dice list
    dice_dict = {}
    for die in dice_to_roll:
        # defaults to 0 if the key isn't currently in use
        dice_dict[die.num_sides] = dice_dict.get(die.num_sides, 0) + 1
    # setting up some parameters
    gap = 10
    button_size = 50
    line_height = 10
    text_x = 10
    button_x = 100
    for die in list(dice_dict):
        # text
        text = font.render(f"D{str(die)}s: {dice_dict[die]}", True, text_color)
        canvas.blit(text, (text_x, line_height))
        # buttons
        plus_location = (max(text.get_width()+gap, canvas_size[0]-gap*2-button_size*2), line_height)
        minus_location = (max(text.get_width()+gap*2+button_size, canvas_size[0]-gap-button_size), line_height)
        button_dict[die] = (pygame.rect.Rect(*plus_location, button_size, button_size),
                                      pygame.rect.Rect(*minus_location, button_size, button_size))
        pygame.draw.rect(canvas, button_color, button_dict[die][0])
        pygame.draw.rect(canvas, button_color, button_dict[die][1])
        text = font.render('+', True, text_color)
        canvas.blit(text, (plus_location[0]+button_size//4, plus_location[1]))
        text = font.render('-', True, text_color)
        canvas.blit(text, (minus_location[0]+button_size//4, minus_location[1]))
        # move down a row
        line_height += font_size + 5

def logic(event_type, event_details):
    global total, dice_to_roll, clicking
    if event_details[-1] != application_name:
        return
    match event_type:
        case "mouse":
            if event_details[0] == "not clicking":
                clicking = False
            else:
                buttons_pressed = event_details[0]
                mouse_pos = event_details[1]
                if not mouse_in_window(mouse_pos):
                    return None
                if not clicking: 
                    clicking = True
                    button_clicked = False
                    for button_sides in list(button_dict):
                        buttons = button_dict[button_sides]
                        plus, minus = buttons[0], buttons[1]
                        if inside_rect(plus, mouse_pos):
                            button_clicked = True
                            dice_to_roll.append(Dice(button_sides))
                            return
                        elif inside_rect(minus, mouse_pos):
                            button_clicked = True
                            for die in dice_to_roll:
                                if die.num_sides == button_sides:
                                    dice_to_roll.remove(die)
                                    if die not in dice_to_roll:
                                        button_dict.pop(die.num_sides)
                                    return
                            return
                    total = 0
                    if not button_clicked:
                        # roll the dice!
                        for die in dice_to_roll:
                            value = die.roll()
                            total += value
        case "keyboard down":
            pass
        case "keyboard up":
            pass
        case _:
            submenu_path = [x.strip() for x in event_type.split(">")]
            match submenu_path[0]:
                case "Add Dice":
                    dice_kind = submenu_path[1]
                    number_of_sides = int(dice_kind[1:])
                    dice_to_roll.append(Dice(number_of_sides))
                case "Remove Dice":
                    dice_kind = submenu_path[1]
                    number_of_sides = int(dice_kind[1:])
                    for die in dice_to_roll:
                        if die.num_sides == number_of_sides:
                            dice_to_roll.remove(die)
                            return
                case _:
                    print("Event called:", event_type)

# general utility functions

def mouse_in_window(mouse_position):
    canvas_size = canvas.get_size()
    if mouse_position[0] > 0 and mouse_position[0] <= canvas_size[0]:
        if mouse_position[1] > 0 and mouse_position[1] <= canvas_size[1]:
            return True
    return False

def inside_rect(rectangle, xy):
        x, y = xy[0], xy[1]
        if x >= rectangle.left and x <= rectangle.right:
            if y >= rectangle.top and y <= rectangle.bottom:
                return True
        return False
