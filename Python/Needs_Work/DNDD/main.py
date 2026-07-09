from Tools import DiceRoller
from Tools import BattleMap
from Tools import DefaultTool
from Tools import InitiativeTracker
from Tools.RootEngine import *
from Desktop import Desktop

def init():
    global desktop, tools, tool_icons
    desktop = Desktop((750, 750))
    # tools = ["RootEngine"]
    tools = ["DefaultTool", "BattleMap", "InitiativeTracker", "DiceRoller"]
    # initialize each tool individually, so that it can properly manage canvases
    for tool in tools:
        desktop.icons[tool] = "./icons/default_icon.png"
        desktop.request_window(tool)
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