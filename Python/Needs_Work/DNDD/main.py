from Tools import DiceRoller
from Tools import BattleMap
from Tools import DefaultTool
from Tools import InitiativeTracker
from Tools.RootEngine import *
from Desktop import Desktop

possible_tools = ["BattleMap", "DefaultTool", "DiceRoller", "InitiativeTracker", "RootEngine"]

def init():
    global desktop, tools, tool_icons
    desktop = Desktop((1000, 750))
    # tools = ["RootEngine"]
    initial_tools = []
    # initialize each tool individually, so that it can properly manage canvases
    for tool in initial_tools:
        desktop.icons[tool] = "./icons/default_icon.png"
        desktop.request_window(tool)
    desktop.application_order.reverse()
    tools = initial_tools

def main():
    global tools
    update_tools()
    running = True
    while running:
        instruction = desktop.logic()
        if instruction == "stop":
            running = False
            continue
        elif instruction in possible_tools:
            tool = instruction
            tools.append(tool)
            desktop.icons[tool] = "./icons/default_icon.png"
            desktop.request_window(tool)
        elif instruction != None:
            # print("main func print", instruction)
            pass
        update_tools(instruction)
        desktop.draw()
        desktop.clock.tick(desktop.fps)

def update_tools(desktop_logic=None):
    for tool in tools:
        match tool:
            case "InitiativeTracker": InitiativeTracker.run(desktop.window_dict, desktop_logic)
            case "DefaultTool": DefaultTool.run(desktop.window_dict, desktop_logic)
            case "DiceRoller": DiceRoller.run(desktop.window_dict, desktop_logic)
            case "BattleMap": BattleMap.run(desktop.window_dict, desktop_logic)
            case "RootEngine": Launcher.run(desktop.window_dict, desktop_logic)

if __name__ == "__main__":
    init()
    main()