from pack import NameGenerator as name_gen
from pack import Zone
from pack import Entity
import os

os.system('cls')

player_x = 1
player_y = 1
map_size = (4,4)

Zone.make_map(map_size)
Zone.block_zone(Zone.get_zone(0,0))
Zone.block_zone(Zone.get_zone(3,0))
Zone.block_zone(Zone.get_zone(3,1))
Zone.block_zone(Zone.get_zone(3,2))
Zone.block_zone(Zone.get_zone(0,3))
Zone.block_zone(Zone.get_zone(1,3))
Zone.block_zone(Zone.get_zone(2,3))

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

rock = Entity.entity("rock", 1, 0, [("move", "You pushed the rock. I'm not sure why, because it didn't do anything.")])
pizza = Entity.entity("pizza", 2, 0, [("eat", "You take a bite of the pizza. It tastes quite greasy")])
person = Entity.entity("guy", 0, 1, [("talk", "'Hello! My name is Ramoth. I'm just here.'")])
lake = Entity.entity("lake", 1, 1, [("swim", "You take a dive into the lake. It's quite chilly, but also refreshing.")])
stick = Entity.entity("stick", 2, 1, [("break", "You broke the stick")])
tree = Entity.entity("tree", 0, 2, [("climb", "You climbed up the tree and can see around. However, you can't see that much.")])
house = Entity.entity("house", 1, 2, [("enter", "You enter the house.")])
chest = Entity.entity("chest", 2, 2, [("open", "You open the chest to see - well nothing. Better luck next time!")])

house.make_building(Zone.get_zone(3,3))

possible_moves = ["north", "n", "south", "s", "east", "e", "west", "w"]
possible_actions = ["grab", "break", "move", "eat", "talk", "swim", "climb", "enter", "open"]
entity_list = [rock, pizza, person, lake, stick, tree, house, chest]

for i in range(len(entity_list)):
    current_entity = entity_list[i]
    x,y = current_entity.x, current_entity.y
    Zone.get_zone(x,y).object_list.append(current_entity)

Zone.get_zone(3,3).description = "This is a mostly empty room with a table and chair, waiting for you."

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
    if len(player_input_list):
        if player_input_list[0] in possible_actions:
            if len(player_input_list) > 1:
                match player_input_list[1]:
                    case "rock":
                        outcome = rock.do_action(player_input_list[0], player_x, player_y)
                    case "pizza":
                        outcome = pizza.do_action(player_input_list[0], player_x, player_y)
                    case "person":
                        outcome = person.do_action(player_input_list[0], player_x, player_y)
                    case "lake":
                        outcome = lake.do_action(player_input_list[0], player_x, player_y)
                    case "stick":
                        outcome = stick.do_action(player_input_list[0], player_x, player_y)
                    case "tree":
                        outcome = tree.do_action(player_input_list[0], player_x, player_y)
                    case "house":
                        outcome = house.do_action(player_input_list[0], player_x, player_y)
                        house.enter_building(player_x, player_y)
                    case "chest":
                        outcome = chest.do_action(player_input_list[0], player_x, player_y)
                    case _:
                        outcome = "Invalid object. Press Enter to continue. "
            else:
                outcome = "No item selected. Press Enter to continue. "
        elif player_input_list[0] == "look":
            Zone.get_zone(player_x, player_y).print_desc()
    if player_input == "exit":
        os.system('cls')
        running = False
        break