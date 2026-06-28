from Tools import DiceRoller
from Tools import BattleMap
from Tools import DefaultTool
from Tools import InitiativeTracker
from Desktop import Desktop

desktop = Desktop((1920, 1080))
tools = ["BattleMap", "DiceRoller", "DefaultTool", "InitiativeTracker"]
for tool in tools:
    desktop.request_canvas(tool)
# needs to be a seperate step to properly initialize canvas_dict
for tool in tools:
    match tool:
        case "InitiativeTracker": InitiativeTracker.run(desktop.canvas_dict)
        case "DefaultTool": DefaultTool.run(desktop.canvas_dict)
        case "DiceRoller": DiceRoller.run(desktop.canvas_dict)
        case "BattleMap": BattleMap.run(desktop.canvas_dict)

running = True
while running:
    instruction = desktop.logic()
    match instruction:
        case "stop":
            running = False
    desktop.draw()
    desktop.clock.tick(desktop.fps)