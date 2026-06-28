from Tools import DiceRoller
from Tools import BattleMap
from Desktop import Desktop

desktop = Desktop((1920, 1080))

# DiceRoller.run(desktop.request_canvas())
BattleMap.run(desktop.request_canvas())

running = True
while running:
    instruction = desktop.logic()
    match instruction:
        case "stop":
            running = False
    desktop.draw()
    desktop.clock.tick(desktop.fps)