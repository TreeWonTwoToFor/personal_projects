from Tools import DiceRoller
from Tools import BattleMap
from Tools import DefaultTool
from Tools import InitiativeTracker
from Tools import TextEditor
from Desktop import Desktop

possible_tools = {
    "BattleMap": {
        "module": BattleMap,
        "dropdown": [["Shape >", "Rectangle", "Circle"], ["Palette >", "Stone", "Paper", "Forest"], "Close BattleMap"]
    }, 
    "DiceRoller": {
        "module": DiceRoller,
        "dropdown": [["Add Dice >", "d4", "d6", "d8", "d10", "d12", "d20"], 
                     ["Remove Dice >", "d4", "d6", "d8", "d10", "d12", "d20"], "Close DiceRoller"]
    }, 
    "TextEditor": {
        "module": TextEditor,
        "dropdown": ["Close TextEditor"]
    },
    # "DefaultTool": {
    #     "module": DefaultTool,
    #     "dropdown": [["Hello, >", "World!"], "Close DefaultTool"]
    # }, 
    # "InitiativeTracker": {
    #     "module": InitiativeTracker,
    #     "dropdown": ["Close InitiativeTracker"]
    # }
}

tools = []

def init():
    global desktop
    desktop = Desktop((1000,750), possible_tools)
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
            if instruction[0].split(" ")[0] in ["mouse", "keyboard"]:
                # give user input over to update
                update_tools(instruction)
            else:
                parent_app, app_instruction = instruction
                if type(app_instruction) == str and app_instruction.split(' ')[0] == "Close":
                    close_tool(parent_app)
                else:
                    match parent_app:
                        case "Desktop":
                            # we know that it's always going to be an open, until we decide to add more desktop options
                            app_name = app_instruction.split(" ")[-1]
                            load_tool(app_name)
                        case _:
                            # we can just feed the app the dropdown option that's been selected
                            run_tool(parent_app, [app_instruction, [parent_app]])
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
    # run initialization for that tool
    possible_tools[tool_name]["module"].run_once()

def close_tool(tool_name):
    global tools
    tools.remove(tool_name)
    desktop.close_app(tool_name)

def run_tool(app, instruction):
    possible_tools[app]["module"].run(desktop.window_dict, instruction)

def update_tools(desktop_logic=None):
    for tool_name in tools: 
        # maybe this could be changed s.t. it only feeds a non-None instruction to the specfic tool?
        run_tool(tool_name, desktop_logic)

if __name__ == "__main__":
    init()
    main()
