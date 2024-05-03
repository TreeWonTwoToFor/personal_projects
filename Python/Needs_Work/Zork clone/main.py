from pack import NameGenerator as name_gen
from pack import Zone
import os

os.system('cls')

player_x = 0
player_y = 0
map_size = (5,5)

Zone.make_map(map_size)

running = True
while running:
    os.system('cls')
    Zone.give_scene(Zone.get_zone(player_x, player_y))
    player_direction = input("Where do you want to move? ")
    if player_direction == "north" and player_y > 0:
        player_y -= 1
    elif player_direction == "south" and player_y < map_size[1]-1:
        player_y += 1
    elif player_direction == "west" and player_x > 0:
        player_x -= 1
    elif player_direction == "east" and player_x < map_size[0]-1:
        player_x += 1
    elif player_direction == "exit":
        os.system('cls')
        running = False
        break
    else:
        print("inavlid input")