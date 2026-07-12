import random
import pygame

application_name = "DiceRoller"
application_icon = "./icons/dice_icon.png"

background_color = (100, 100, 100)
canvas = None
clicking = False

pygame.font.init()
font = pygame.font.Font("../Comfortaa.ttf", 50)
text_color = (255,255,255)

class Dice:
    def __init__(self, num_sides):
        self.num_sides = num_sides

    def __str__(self):
        return str(self.num_sides)

    def roll(self):
        return random.randint(1, self.num_sides)

def run_once():
    global total, dice_to_roll
    total = 0
    dice_to_roll = [Dice(20)]  

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
    text_location = [10, 10]
    for die in list(dice_dict):
        text = font.render(f"D{str(die)}s: {dice_dict[die]}", True, text_color)
        canvas.blit(text, text_location)
        text_location[1] += 55

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
                    # roll the dice!
                    total = 0
                    for die in dice_to_roll:
                        value = die.roll()
                        total += value
                clicking = True
        case "keyboard":
            key_pressed = event_details[0]
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
                        continue
                case _:
                    print("Event called:", event_type)

def mouse_in_window(mouse_position):
    canvas_size = canvas.get_size()
    if mouse_position[0] > 0 and mouse_position[0] <= canvas_size[0]:
        if mouse_position[1] > 0 and mouse_position[1] <= canvas_size[1]:
            return True
    return False