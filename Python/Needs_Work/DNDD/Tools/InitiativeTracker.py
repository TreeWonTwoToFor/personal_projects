application_name = "InitiativeTracker"

def run(canvas_dict, desktop_instruction):
    canvas = canvas_dict[application_name].surface
    logic_output = logic()
    draw(canvas, logic_output)

def draw(canvas, logic_output):
    canvas.fill([255,0,0])

def logic():
    pass