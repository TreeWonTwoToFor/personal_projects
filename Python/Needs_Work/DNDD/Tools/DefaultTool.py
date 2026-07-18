application_name = "DefaultTool"
application_icon = "./icons/default_icon.png"

background_color = (255,255,255)
canvas = None

clicking = False

def run_once():
    # any initialization should go in there, in order to keep the state fresh every time the tool is opened.
    pass

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

def logic(event_type, event_details):
    global clicking
    if event_details[-1] != application_name:
        return
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
                    print("Buttons and pos:", buttons_pressed, mouse_pos)
                clicking = True
        case "keyboard down":
            key_pressed = event_details[0]
            match key_pressed:
                case _:
                    print("Key pressed:", key_pressed)
        case "keyboard up":
            key_pressed = event_details[0]
            match key_pressed:
                case _:
                    print("Key released:", key_pressed)
        case _:
            # here can be a list of the specific submenu options inside the dropdown for this app.
            submenu_path = [x.strip() for x in event_type.split(">")]
            print(submenu_path)
            match event_type:
                case _:
                    print("Event called:", event_type)

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
