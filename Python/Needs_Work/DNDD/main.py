from Tools import DiceRoller
from Tools import BattleMap
from Tools import DefaultTool
from Tools import InitiativeTracker
from Tools.RootEngine import Launcher as RootEngine
from Desktop import Desktop

possible_tools = {
    "BattleMap": {
        "module": BattleMap,
        "dropdown": [["Shape >", "Rectangle", "Circle"], ["Palette >", "Stone", "Paper"], "Close BattleMap"]
    }, 
    "DefaultTool": {
        "module": DefaultTool,
        "dropdown": ["Close DefaultTool"]
    }, 
    "InitiativeTracker": {
        "module": InitiativeTracker,
        "dropdown": ["Close InitiativeTracker"]
    }, 
    "DiceRoller": {
        "module": DiceRoller,
        "dropdown": ["Close DiceRoller"]
    }, 
    "RootEngine": {
        "module": RootEngine,
        "dropdown": ["Close RootEngine"]
    }
}

tools = []

def init():
    global desktop
    desktop = Desktop((1000,750))
    initial_tools = []
    # initialize each tool individually, so that it can properly manage canvases
    for tool in initial_tools:
        load_tool(tool)
    desktop.application_order.reverse()
    desktop.tool_reference_table = possible_tools

def main():
    update_tools()
    running = True
    while running:
        instruction = desktop.logic()
        if instruction == "stop":
            running = False
            continue
        elif instruction is not None:
            if instruction[0] == "mouse" or instruction[0] == "keyboard":
                # give the mouse input over to update
                update_tools(instruction)
            else:
                parent_app, app_instruction = instruction
                if type(app_instruction) == str and app_instruction.split(' ')[0] == "Close":
                    close_tool(parent_app)
                else:
                    match parent_app:
                        case "Desktop":
                            # we know that it's always going to be an open, until we decide to add more desktop options
                            load_tool(app_instruction)
                        case _:
                            possible_tools[parent_app]["module"].run(desktop.window_dict, app_instruction)
        else:
            # just do a nomral rerun of all tools for their frames
            update_tools()
        desktop.draw()
        desktop.clock.tick(desktop.fps)

def load_tool(tool_name):
    global desktop, tools
    tools.append(tool_name)
    # the try will fail if no application icon is properly initialized
    try:
        desktop.load_icon(tool_name, possible_tools[tool_name]["module"].application_icon)
    except:
        desktop.load_icon(tool_name)
    desktop.open_app(tool_name)

def close_tool(tool_name):
    global tools
    tools.remove(tool_name)
    desktop.close_app(tool_name)

def update_tools(desktop_logic=None):
    for tool_name in tools:
        possible_tools[tool_name]["module"].run(desktop.window_dict, desktop_logic)

if __name__ == "__main__":
    init()
    main()