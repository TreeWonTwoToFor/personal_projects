import pygame
import copy

application_name = "TextEditor"
application_icon = "./icons/notepad_icon.png"

background_color = (255,255,255)
canvas = None

clicking = False

pygame.font.init()
font_size = 24
line_gap = 3
font = pygame.font.Font("../Comfortaa.ttf", font_size)
text_color = (0,0,0)

symbol_key_dict = {
    '1': '!',
    '2': '@',
    '3': '#',
    '4': '$',
    '5': '%',
    '6': '^',
    '7': '&',
    '8': '*',
    '9': '(',
    '0': ')',
    '-': '_',
    '=': '+',
    '[': '{',
    ']': '}',
    ';': ':',
    "'": '"',
    ',': "<",
    ".": ">",
    '/': '?',
    '\\': '|'
}

def run_once():
    # any initialization should go in there, in order to keep the state fresh every time the tool is opened.
    global text_list, held_keys, delayed_auto_type
    text_list = [""]
    held_keys = []
    delayed_auto_type = 0

def run(window_dict, desktop_instruction):
    global canvas
    canvas = window_dict[application_name].surface
    if desktop_instruction is not None:
        event_type, event_details = desktop_instruction[0], desktop_instruction[1]
    else:
        event_type = None
        event_details = [None]
    logic_output = logic(event_type, event_details)
    draw(logic_output)

def draw(logic_output):
    canvas.fill(background_color)
    line_height = 10
    text = None
    for line in text_list:
        text = font.render(line, True, text_color)
        canvas.blit(text, (10, line_height))
        line_height += text.get_height() + line_gap
    # draw the cursor
    cursor = font.render("_", True, text_color)
    if text != None:
        canvas.blit(cursor, (text.get_width()+10, line_height-text.get_height()-line_gap))
    else:
        canvas.blit(cursor, (10, 10))

def logic(event_type, event_details):
    global clicking, text_list, held_keys, old_held_keys, delayed_auto_type
    old_held_keys = copy.deepcopy(held_keys)
    if event_details[-1] == application_name:
        match event_type:
            case "mouse":
                if event_details[0] == "not clicking":
                    clicking = False
                else:
                    buttons_pressed = event_details[0]
                    mouse_pos = event_details[1]
                    # print("Default tool event details:", event_details)
                    if not mouse_in_window(mouse_pos):
                        return None
                    # otherwise, perform mouse logic
                    if not clicking: # is this the initial click?
                        pass
                    clicking = True
            case "keyboard down":
                key_pressed = event_details[0]
                if key_pressed not in held_keys:
                    held_keys.append(key_pressed)
            case "keyboard up":
                key_pressed = event_details[0]
                if key_pressed in held_keys:
                    held_keys.remove(key_pressed)
            case _:
                # here can be a list of the specific submenu options inside the dropdown for this app.
                submenu_path = [x.strip() for x in event_type.split(">")]
                print(submenu_path)
                match event_type:
                    case _:
                        # currently has no other options, so it goes unusued
                        print("Event called:", event_type)
    # handling held keys
    pressed_new_key = False
    if len(old_held_keys) > 0 and len(held_keys) > 0:
        if old_held_keys[-1] == held_keys[-1]:
            # the last key to be pressed is the same as the last one
            pass
        else:
            pressed_new_key = True
    else:
        if len(held_keys) > 0:
            pressed_new_key = True
        else:
            # we're not holding any keys
            delayed_auto_type = 0
    if pressed_new_key:
        delayed_auto_type = 1
    elif delayed_auto_type > 0:
        delayed_auto_type += 1

    if delayed_auto_type > 0 and delayed_auto_type % 25 == 1:
        key_pressed = held_keys[-1]
        match key_pressed:
            case "return":
                text_list.append("")
            case "backspace":
                if len(text_list) == 1 and len(text_list[0]) == 0:
                    return
                if len(text_list[-1]) == 0:
                    text_list.pop()
                else:
                    if "left ctrl" in held_keys or "right ctrl" in held_keys:
                        num_chars = len(text_list[-1].split(" ")[-1]) + 1
                        text_list[-1] = text_list[-1][:-num_chars]
                    else:
                        text_list[-1] = text_list[-1][:-1]
            case "space":
                text_list[-1] = text_list[-1] + " "
            case "tab":
                # tab default length is 4 characters
                text_list[-1] = text_list[-1] + "    "
            case _:
                if len(key_pressed) == 1:
                    if "left shift" not in held_keys and "right shift" not in held_keys:
                        text_list[-1] = text_list[-1] + key_pressed
                    else:
                        if key_pressed.isalpha():
                            text_list[-1] = text_list[-1] + key_pressed.upper()
                        else:
                            text_list[-1] = text_list[-1] + symbol_key_dict[key_pressed]

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
