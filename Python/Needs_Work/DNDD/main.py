from Tools import DiceRoller
from Tools import BattleMap
from Tools import DefaultTool
from Tools import InitiativeTracker
from Tools.RootEngine import *
from Desktop import Desktop

desktop = Desktop((1000, 1000))
tools = ["RootEngine"]
# tools = ["DefaultTool", "BattleMap", "InitiativeTracker", "DiceRoller"]
# initialize each tool individually, so that it can properly manage canvases
for tool in tools:
    desktop.request_window(tool)

def update_tools(desktop_logic=None):
    for tool in tools:
        match tool:
            case "InitiativeTracker": InitiativeTracker.run(desktop.window_dict, desktop_logic)
            case "DefaultTool": DefaultTool.run(desktop.window_dict, desktop_logic)
            case "DiceRoller": DiceRoller.run(desktop.window_dict, desktop_logic)
            case "BattleMap": BattleMap.run(desktop.window_dict, desktop_logic)
            case "RootEngine": Launcher.run(desktop.window_dict, desktop_logic)

update_tools()
running = True
while running:
    instruction = desktop.logic()
    if instruction == "stop":
        running = False
    elif instruction != None:
        print(instruction)
        update_tools(instruction)
    desktop.draw()
    desktop.clock.tick(desktop.fps)