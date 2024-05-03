from pack import NameGenerator as name_gen
from pack import Zone
from pack import Entity
import os

os.system('cls')

player_x = 0
player_y = 0
map_size = (3,3)

Zone.make_map(map_size)

def move_player(player_input):
    global player_x, player_y
    x, y = player_x, player_y
    if player_input in possible_moves:
        print(player_input)
        match player_input:
            case "north" | "n":
                y -= 1
            case "south" | "s":
                y += 1
            case "east" | "e":
                x += 1
            case "west" | "w":
                x -= 1
        if x >= 0 and x <= map_size[0]-1 and y >= 0 and y <= map_size[1]-1 and not Zone.get_zone(x,y).description == "blocked":
            player_x, player_y = x, y

possible_moves = ["north", "n", "south", "s", "east", "e", "west", "w"]
possible_actions = ["grab", "break"]

stick = Entity.entity("stick", 2, 2, [("grab", "You picked up the stick"), ("break", "You broke the stick")])

outcome = ""
running = True
while running:
    os.system('cls')
    Zone.give_scene(Zone.get_zone(player_x, player_y))
    if outcome != "":
        print(outcome)
    outcome = ""
    player_input = input("What do you do? ").lower()
    player_input_list = player_input.split()
    move_player(player_input)
    if player_input_list[0] in possible_actions:
        if player_input_list[1] == "stick":
            outcome = stick.do_action(player_input_list[0], player_x, player_y)
    if player_input == "exit":
        os.system('cls')
        running = False
        break