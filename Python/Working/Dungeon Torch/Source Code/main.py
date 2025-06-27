import pygame
import random
import Entity
import Room

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 720))

# constants
FPS = 60
tile_edge = 2
tile_size = 68
door_list = [
    (4,0),(5,0),
    (4,9),(5,9),
    (0,4),(9,4),
    (0,5),(9,5)]
map_size = 4
map_tile_size = 75
starting_torches = 4
new_movement = False

# images
torch = pygame.image.load(".\\assets\\torch.png")
torch = pygame.transform.scale(torch, (50, 50))

ring = pygame.image.load(".\\assets\\ruby_ring.png")
ring_small = pygame.transform.scale(ring, (64, 64))
sword = pygame.image.load(".\\assets\\sword.png")
sword_small = pygame.transform.scale(sword, (64, 64))
book = pygame.image.load(".\\assets\\grimoire.png")
book_small = pygame.transform.scale(book, (64, 64))
orb = pygame.image.load(".\\assets\\tree_ball.png")
orb_small = pygame.transform.scale(orb, (64, 64))

treasure_image = pygame.image.load(".\\assets\\treasure_slots.png")
treasure_image = pygame.transform.scale(treasure_image, (275, 275))

item_list = [ring_small, sword_small, book_small, orb_small]

# music
main_theme = pygame.mixer.music.load(".\\assets\\main_song.mp3")
pygame.mixer.music.set_volume(0.5)

held_keys = [0, 0, 0, 0] # W, A, S, D

def entity_update():
    for entity in entity_list:
        if not entity.alive:
            entity_list.remove(entity)
        else:
            entity.draw(screen, tile_size, 20)

def enemy_move():
    for entity in entity_list:
        if not entity.is_player:
            direction_list = ['u', 'l', 'd', 'r']
            entity.move_enemy(direction_list[random.randint(0, 3)], tile_size)

def spawn_enemy():
    enemy_type = random.randint(0, 0) # TODO for future enemies, add more to this random value
    spawn_point = (random.randint(3,6), random.randint(3,6))
    entity_list.append(Entity.Entity(spawn_point[0], spawn_point[1], (255, 0, 0)))

def spawn_treasure(treasure_image):
    spawn_point = (1, 1)
    entity_list.append(Entity.Entity(spawn_point[0], spawn_point[1], None, treasure_image))

def player_state():
    for entity in entity_list:
        if not player == entity:
            if player.distance(entity) == 0:
                player.alive = False
                pygame.mixer.music.pause()

def player_attack():
    global torches, treasure_count
    for entity in entity_list:
        if player:
            player.sword_timer = 10
        if not player == entity and player.distance(entity) == 1:
            target_tile = player.tile_in_direction()
            if entity.x == target_tile[0] and entity.y == target_tile[1]:
                old_treasure_count = treasure_count
                output = entity.die(torches, screen, treasure_count)
                torches = output[0]
                treasure_count = output[1]
                if output[1] == old_treasure_count:
                    current_room().has_enemy = False
                else:
                    current_room().treasure = None

def map_draw(first_run, room_change):
    if room_change != None or first_run:
        room = current_room()
        if room.visited == False:
            pygame.draw.rect(screen, room.color, pygame.Rect(
                843+room.x*map_tile_size, 43+room.y*map_tile_size, map_tile_size-6, map_tile_size-6))

def draw_tile_overlay():
    for i in range(680//tile_size):
        for j in range(680//tile_size):
            x = 20 + i*tile_size
            y = 20 + j*tile_size
            pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(x, y, tile_size, tile_size), tile_edge)

def draw_torches_ui(n_torches):
    pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(700, 280, 70, 160))
    pygame.draw.rect(screen, (255, 255, 100), pygame.Rect(820, 20, 340, 340), 4)
    pygame.draw.rect(screen, (100, 100, 255), pygame.Rect(720, 360, 540, 340), 4)
    torch_font = pygame.font.Font('.\\assets\\PixelatedFont.ttf', 50)
    text = torch_font.render(f' : {n_torches} ', True, (255, 255, 255), (60, 60, 60))
    textRect = text.get_rect()
    textRect.center = (850, 425)
    screen.blit(text, textRect)
    screen.blit(torch, (750, 400))

def get_room(x, y):
    return room_map[y][x]

def current_room():
    return get_room(room_pos[0], room_pos[1])

def update_nearby_rooms():
    if room_pos[0] > 0:
        get_room(room_pos[0]-1, room_pos[1]).door_states[3] = 1
    if room_pos[0] < map_size-1:
        get_room(room_pos[0]+1, room_pos[1]).door_states[1] = 1
    if room_pos[1] > 0:
        get_room(room_pos[0], room_pos[1]-1).door_states[2] = 1
    if room_pos[1] < map_size-1:
        get_room(room_pos[0], room_pos[1]+1).door_states[0] = 1

game_running = "start"
running = True
while running:
    if game_running == "running":
        player_alive = False
        for entity in entity_list:
            if entity.is_player: player_alive = True
        if not player_alive:
            game_running = "start"
        # event getter
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        running = False
                    case pygame.K_w: held_keys[0] = 1
                    case pygame.K_a: held_keys[1] = 1
                    case pygame.K_s: held_keys[2] = 1
                    case pygame.K_d: held_keys[3] = 1
                    case pygame.K_j: player_attack()
            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_w: held_keys[0] = 0
                    case pygame.K_a: held_keys[1] = 0
                    case pygame.K_s: held_keys[2] = 0
                    case pygame.K_d: held_keys[3] = 0
        is_moving = 0
        for i in range(len(held_keys)):
            is_moving += held_keys[i]
        if is_moving == 0:
            player.move_timer = 15
        # update player position
        room_change = None
        if player.alive:
            if new_movement:
                if held_keys[0]: 
                    if player.move('u', tile_size, door_list) != None: 
                        room_change = player.direction
                if held_keys[1]: 
                    if player.move('l', tile_size, door_list) != None: 
                        room_change = player.direction
                if held_keys[2]: 
                    if player.move('d', tile_size, door_list) != None: 
                        room_change = player.direction
                if held_keys[3]: 
                    if player.move('r', tile_size, door_list) != None: 
                        room_change = player.direction
            else:
                treasure = None
                blocked_positions = []
                for entity in entity_list: 
                    if entity.is_treasure: 
                        treasure = entity
                if treasure != None:
                    blocked_positions.append((treasure.x, treasure.y))
                if held_keys[0]: 
                    can_move = True
                    for position in blocked_positions:
                        if (player.x, player.y-1) == position:
                            can_move = False
                    if can_move and player.move_enemy('u', tile_size, door_list) != None: 
                        room_change = player.direction
                    elif not can_move:
                        player.direction = 'u'
                elif held_keys[1]: 
                    can_move = True
                    for position in blocked_positions:
                        if (player.x-1, player.y) == position:
                            can_move = False
                    if can_move and player.move_enemy('l', tile_size, door_list) != None: 
                        room_change = player.direction
                    elif not can_move:
                        player.direction = 'l'
                elif held_keys[2]: 
                    can_move = True
                    for position in blocked_positions:
                        if (player.x, player.y+1) == position:
                            can_move = False
                    if can_move and player.move_enemy('d', tile_size, door_list) != None: 
                        room_change = player.direction
                    elif not can_move:
                        player.direction = 'd'
                elif held_keys[3]: 
                    can_move = True
                    for position in blocked_positions:
                        if (player.x+1, player.y) == position:
                            can_move = False
                    if can_move and player.move_enemy('r', tile_size, door_list) != None: 
                        room_change = player.direction
                    elif not can_move:
                        player.direction = 'r'

        # room update
        if room_change != None:
            for entity in entity_list:
                if not entity.is_player:
                    entity_list.remove(entity)
            used_torch = False
            action = current_room().change_room(room_change, torches)
            update_nearby_rooms()
            if action == "remove torch": 
                torches -= 1
                used_torch = True
            if action != "cannot move":
                if action == "You are free":
                    game_running = "escape"
                    pygame.mixer.stop()
                    ending_theme = pygame.mixer.music.load(".\\assets\\ending.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(2)
                else:
                    match room_change:
                        case 'u': 
                            if room_pos[1] > 0: 
                                if used_torch:
                                    current_room().door_states[0] = 1
                                room_pos[1] -= 1
                                current_room().door_states[2] = 1
                                player.y = 9
                        case 'l': 
                            if room_pos[0] > 0: 
                                if used_torch:
                                    current_room().door_states[1] = 1
                                room_pos[0] -= 1
                                current_room().door_states[3] = 1
                                player.x = 9
                        case 'd': 
                            if room_pos[1] < map_size-1: 
                                if used_torch:
                                    current_room().door_states[2] = 1
                                room_pos[1] += 1
                                current_room().door_states[0] = 1
                                player.y = 0
                        case 'r': 
                            if room_pos[0] < map_size-1: 
                                if used_torch:
                                    current_room().door_states[3] = 1
                                room_pos[0] += 1
                                current_room().door_states[1] = 1
                                player.x = 0
                    if current_room().has_enemy:
                        spawn_enemy()
                    if current_room().treasure != None:
                        spawn_treasure(current_room().treasure)

        if torches == 0:
            room = current_room()
            if room.y-1 < map_size and (not get_room(room.x, room.y-1).has_enemy): 
                get_room(room.x, room.y-1).has_enemy = True
            elif room.y+1 < map_size and (not get_room(room.x, room.y+1).has_enemy): 
                get_room(room.x, room.y+1).has_enemy = True
            elif room.x-1 < map_size and (not get_room(room.x-1, room.y).has_enemy): 
                get_room(room.x-1, room.y).has_enemy = True
            elif room.x+1 < map_size and (not get_room(room.x+1, room.y).has_enemy): 
                get_room(room.x+1, room.y).has_enemy = True

        map_draw(first_run, room_change)
        draw_torches_ui(torches)
        current_room().draw(screen, tile_size)
        enemy_move()
        player_state()
        current_room().visited = True
        if new_movement:
            draw_tile_overlay()
            entity_update()
        else:
            entity_update()
            draw_tile_overlay()
        first_run = False
        if treasure_count == 4:
            get_room(0,0,).door_states[0] = 3
    elif game_running == "start":
        # initialized stuff
        held_keys = [0, 0, 0, 0] 
        # entity setup
        player = Entity.Entity(4, 4, (0, 255, 0))
        player.is_player = True
        entity_list = [player]
        # room setup
        have_escape_door = False
        room_pos = [map_size//2, map_size//2]
        room_map = []
        for i in range(map_size):
            row = []
            for j in range(map_size):
                new_room = Room.Room(j, i)
                if i == 0: new_room.door_states[0] = 2
                if j == 0: new_room.door_states[1] = 2
                if i == map_size-1: new_room.door_states[2] = 2
                if j == map_size-1: new_room.door_states[3] = 2
                row.append(new_room)
            room_map.append(row)
        for treasure in item_list:
            looking = True
            while looking:
                x = random.randint(0, map_size-1)
                y = random.randint(0, map_size-1)
                room = get_room(x,y)
                if room.treasure == None and room != current_room():
                    room.treasure = treasure
                    looking = False
        room_map[0][0].door_states[0] = 4
        current_room().has_enemy = False
        treasure_count = 0
        torches = starting_torches
        first_run = True
        # menu buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        running = False
                    case pygame.K_SPACE:
                        game_running = "running"
                        pygame.mixer.music.play(-1)
        # text
        screen.fill((60, 60, 60))
        start_font = pygame.font.Font('.\\assets\\PixelatedFont.ttf', 80)
        text = start_font.render(f'Dungeon Torch', True, (255, 255, 255), (60, 60, 60))
        textRect = text.get_rect()
        textRect.center = (1280//2, 250)
        screen.blit(text, textRect)
        torch = pygame.transform.scale(torch, (150, 150))
        torch = pygame.transform.flip(torch, True, False)
        screen.blit(torch, (70, 175))
        torch = pygame.transform.flip(torch, True, False)
        screen.blit(torch, (1050, 175))
        torch = pygame.transform.scale(torch, (50, 50))
        

        start_font = pygame.font.Font('.\\assets\\PixelatedFont.ttf', 24)
        all_text = ["WASD to move, J to attack and interact.", "Use torches to light up rooms,", "Find hidden treasures,", "Try to escape!", "Press Space to Start."]
        height = 400
        for string in all_text:
            text = start_font.render(string, True, (255, 255, 255), (60, 60, 60))
            textRect = text.get_rect()
            textRect.center = (1280//2, height)
            height += 50
            screen.blit(text, textRect)

        if game_running == "running":
            screen.fill((60,60,60))
            screen.blit(treasure_image, (965, 380))
    elif game_running == "escape":
        screen.fill((0, 255, 100))
        end_font = pygame.font.Font('.\\assets\\PixelatedFont.ttf', 64)
        all_text = ["You Escaped!", "Press Escape to quit.", "Made by TreeWonTwoToFor"]
        height = 250
        for string in all_text:
            text = end_font.render(string, True, (0, 0, 0), (0, 255, 100))
            textRect = text.get_rect()
            textRect.center = (1280//2, height)
            height += 75
            screen.blit(text, textRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        running = False

    clock.tick(FPS)
    pygame.display.update()