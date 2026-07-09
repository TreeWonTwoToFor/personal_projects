from Tools import DiceRoller
from Tools import BattleMap
from Tools import DefaultTool
from Tools import InitiativeTracker
from Tools.RootEngine import Launcher as RootEngine
from Desktop import Desktop

possible_tools = {
    "BattleMap": BattleMap, 
    "DefaultTool": DefaultTool, 
    "DiceRoller": DiceRoller, 
    "InitiativeTracker": InitiativeTracker, 
    "RootEngine": RootEngine
}

tools = []

def init():
    global desktop
    desktop = Desktop((1000, 750))
    initial_tools = []
    # initialize each tool individually, so that it can properly manage canvases
    for tool in initial_tools:
        load_tool(tool)
    desktop.application_order.reverse()

def main():
    update_tools()
    running = True
    while running:
        instruction = desktop.logic()
        if instruction == "stop":
            running = False
            continue
        elif instruction != None:
            if type(instruction) == str:
                if instruction.split(' ')[0] == "Open":
                    tool = instruction.split(' ')[1]
                    load_tool(tool)
                if instruction.split(' ')[0] == "Close":
                    close_tool(instruction.split(' ')[1])
            # print("main func print", instruction)
            pass
        update_tools(instruction)
        desktop.draw()
        desktop.clock.tick(desktop.fps)

def load_tool(tool_name):
    global desktop, tools
    tools.append(tool_name)
    # the try will fail if no application icon is properly initialized
    try:
        desktop.load_icon(tool_name, possible_tools[tool_name].application_icon)
    except:
        desktop.load_icon(tool_name)
    desktop.open_app(tool_name)

def close_tool(tool_name):
    global tools
    tools.remove(tool_name)

def update_tools(desktop_logic=None):
    for tool in tools:
        possible_tools[tool].run(desktop.window_dict, desktop_logic)

if __name__ == "__main__":
    init()
    main()