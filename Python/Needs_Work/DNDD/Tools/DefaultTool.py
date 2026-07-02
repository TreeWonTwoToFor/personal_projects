application_name = "DefaultTool"

background_color = (255,255,255)
canvas = None

def run(window_dict, desktop_instruction):
    global canvas
    canvas = window_dict[application_name].surface
    if desktop_instruction is not None:
        event_type, event_details = desktop_instruction[0], desktop_instruction[1]
    else:
        event_type, event_details = None, None
    logic_output = logic(event_type, event_details)
    draw(logic_output)

def draw(logic_output):
    canvas.fill(background_color)

def logic(event_type, event_details):
    match event_type:
        case "mouse":
            buttons_pressed = event_details[0]
            mouse_pos = None
            locations = event_details[1]
            for location in locations:
                if location[0] == application_name:
                    mouse_pos = location[1]
            if not mouse_in_window(mouse_pos):
                return None
            # otherwise, perform mouse logic
            print(buttons_pressed, mouse_pos)
        case "keyboard":
            pass

def mouse_in_window(mouse_position):
    canvas_size = canvas.get_size()
    if mouse_position[0] > 0 and mouse_position[0] <= canvas_size[0]:
        if mouse_position[1] > 0 and mouse_position[1] <= canvas_size[1]:
            return True
    return False