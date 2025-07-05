import random
import time
import os
import keyboard
import math

def create_board():
    game_board = []
    # 10x20 board
    for i in range(10):
        column = []
        for j in range(20):
            column.append('_')
        game_board.append(column)
    return game_board

def print_board(game_board, lines_cleared, score):
    os.system('clear')
    text = " "*6 + "TETRIS\n"
    special_values = [f"Score: {score}", f"Lines Cleared: {lines_cleared}"]
    special_rows = range(len(special_values))
    for i in range(20):
        for column in game_board:
            if column[i] == "_": 
                text += ". "
            else:
                text += "□ "
        if i in special_rows:
            text += special_values[i]
        text += '\n'
    print(text)

def random_piece():
    piece_number = random.randint(0,6)
    piece_list = ['i', 't', 'o', 'j', 'l', 's', 'z']
    return piece_list[piece_number]

def spawn_piece(game_board, piece_letter):
    player_died = False
    spawn_location = (3, 0)
    # where are the tiles?
    piece_tiles = []
    match piece_letter:
        case 'i':
            for i in range(4): piece_tiles.append((spawn_location[0]+i, spawn_location[1]))
        case 'o':
            for i in range(2):
                for j in range(2):
                    piece_tiles.append((spawn_location[0]+i+1, spawn_location[1]+j))
        case 't':
            for i in range(3):
                piece_tiles.append((spawn_location[0]+i, spawn_location[1]))
            piece_tiles.append((spawn_location[0]+1, spawn_location[1]+1))
        case 'z':
            for i in range(4):
                piece_tiles.append((spawn_location[0]+(i-i//2), spawn_location[1]+i//2))
        case 's':
            for i in range(4):
                piece_tiles.append((spawn_location[0]+(i-i//2), spawn_location[1]+(1-i//2)))
        case 'l':
            for i in range(3):
                piece_tiles.append((spawn_location[0]+i, spawn_location[1]))
            piece_tiles.append((spawn_location[0], spawn_location[1]+1))
        case 'j':
            for i in range(3):
                piece_tiles.append((spawn_location[0]+i, spawn_location[1]))
            piece_tiles.append((spawn_location[0]+2, spawn_location[1]+1))
    # can we put the tiles on the board?
    for tile in piece_tiles:
        if game_board[tile[0]][tile[1]] != '_':
            player_died = True
            break
        game_board[tile[0]][tile[1]] = '*'
    return player_died

def get_piece_tiles(game_board):
    piece_tile_list = []
    for i in range(len(game_board)):
        column = game_board[i]
        for j in range(len(column)):
            tile = column[j]
            if tile == '*':
                piece_tile_list.append((i,j))
    return piece_tile_list

def drop(game_board):
    piece_tile_list = get_piece_tiles(game_board)
    can_drop = True
    for tile in piece_tile_list:
        if tile[1] == 19:
            can_drop = False
        elif game_board[tile[0]][tile[1]+1] == '@':
            can_drop = False
    if can_drop:
        # move all tiles down one
        piece_tile_list.reverse() # prevents overriding tiles
        for tile in piece_tile_list:
            game_board[tile[0]][tile[1]] = '_'
            game_board[tile[0]][tile[1]+1] = '*'
    else:
        for tile in piece_tile_list:
            game_board[tile[0]][tile[1]] = '@'
    return not can_drop

def move(game_board, direction):
    piece_tile_list = get_piece_tiles(game_board)
    can_move = True
    if direction == 'left':
        for tile in piece_tile_list:
            if tile[0] == 0:
                can_move = False
            elif game_board[tile[0]-1][tile[1]] == '@':
                can_move = False
        if can_move:
            # move all tiles left one
            for tile in piece_tile_list:
                game_board[tile[0]][tile[1]] = '_'
                game_board[tile[0]-1][tile[1]] = '*'
    elif direction == 'right':
        for tile in piece_tile_list:
            if tile[0] == 9:
                can_move = False
            elif game_board[tile[0]+1][tile[1]] == '@':
                can_move = False
        if can_move:
            # move all tiles right one
            piece_tile_list.reverse()
            for tile in piece_tile_list:
                game_board[tile[0]][tile[1]] = '_'
                game_board[tile[0]+1][tile[1]] = '*'

def rotate(game_board, piece_type):
    if piece_type == 'o': return
    original_tiles = get_piece_tiles(game_board)
    # finding orientation + pivot position
    orientation = None
    match piece_type:
        case 'i':
            if original_tiles[0][0] != original_tiles[1][0]:
                orientation = 'horizontal'
            else:
                orientation = 'vertical'
        case 't':
            # get the average point to find "center of mass"
            average_x_value = 0
            average_y_value = 0
            for tile in original_tiles:
                average_x_value += tile[0]
                average_y_value += tile[1]
            average_x_value = average_x_value / 4
            average_y_value = average_y_value / 4
            # use C.O.M. to find where imbalance is
            if average_x_value == original_tiles[1][0]:
                # point up/down?
                if math.isclose(average_y_value-original_tiles[1][1], 0.25):
                    orientation = "up" # direction of the 'hole'
                else:
                    orientation = "down"
            else:
                # point left/right
                if average_x_value > original_tiles[1][0]:
                    orientation = "left"
                else:
                    orientation = "right"
            match orientation:
                case "up": pivot = original_tiles[1]
                case "left": pivot = original_tiles[1]
                case "down": pivot = original_tiles[2]
                case "right": pivot = original_tiles[2]
        case 's' | 'z':
            height_list = []
            for tile in original_tiles:
                if tile[1] not in height_list:
                    height_list.append(tile[1])
            if len(height_list) == 3:
                orientation = 'tall'
            else:
                orientation = 'wide'
        case 'j' | 'l':
            pivot = original_tiles[0]
            height_list = []
            for tile in original_tiles:
                if tile[1] not in height_list: height_list.append(tile[1])
            if len(height_list) == 2:
                # horizontal
                average_x_value = 0
                for tile in original_tiles:
                    average_x_value += tile[0]
                average_x_value = average_x_value / 4
                # determining which side the peice leans towards
                if (average_x_value - pivot[0]) < (original_tiles[3][0]-average_x_value):
                    orientation = 'left'
                else:
                    orientation = 'right'
            else:
                # vertical
                average_x_value = 0
                for tile in original_tiles:
                    average_x_value += tile[0]
                average_x_value = average_x_value / 4
                # determining which side the peice leans towards
                if (average_x_value - pivot[0]) > (original_tiles[3][0]-average_x_value):
                    orientation = 'down'
                else:
                    orientation = 'up'
            
    # getting the relative tile positions
    relative_tiles = []
    match piece_type:
        case 'i':
            match orientation:
                case "horizontal": relative_tiles = [(1,1), (0,0), (-1,-1), (-2,-2)]
                case "vertical":   relative_tiles = [(2,2), (1,1), (0,0), (-1,-1)]
        case 't':
            match orientation:
                case 'up':    relative_tiles = [(0,0), (0,0), (0,0), (-1,-1)]
                case 'right': relative_tiles = [(0,0), (0,0), (0,0), (1,-1)]
                case 'down':  relative_tiles = [(1,1), (0,0), (0,0), (0,0)]
                case 'left':  relative_tiles = [(-1,1), (0,0), (0,0), (0,0)]
        case 'z':
            match orientation:
                case "wide": relative_tiles = [(2, 0), (0, 0), (0, 0), (0, -2)]
                case "tall": relative_tiles = [(0, 0), (0, 0), (0, 2), (-2, 0)]
        case 's':
            match orientation:
                case 'wide': relative_tiles = [(2, 0), (0,0), (0, -2), (0, 0)]
                case 'tall': relative_tiles = [(0, 2), (0, 0), (0, 0), (-2, 0)]
        case 'j':
            match orientation:
                case 'left':  relative_tiles = [(2,0), (1,-1), (0,0), (-1,1)]
                case 'up':    relative_tiles = [(1,1), (0,0), (-1,-1), (0, 2)]
                case 'right': relative_tiles = [(1,-1), (0,0), (-1,1), (-2,0)]
                case 'down':  relative_tiles = [(0,-2), (1,1), (0,0), (-1, -1)]
        case 'l':
            match orientation:
                case 'left':  relative_tiles = [(1,-1), (0,-2), (0,0), (-1,1)]
                case 'down':  relative_tiles = [(2,0), (1,1), (0,0), (-1,-1)]
                case 'right': relative_tiles = [(1,-1), (0,0), (0,2), (-1,1)]
                case 'up':    relative_tiles = [(1,1), (0,0), (-1,-1), (-2,0)]

    # turning relative positions back into global ones
    global_tiles = []
    for i in range(4):
        global_tiles.append((original_tiles[i][0]+relative_tiles[i][0],
                             original_tiles[i][1]+relative_tiles[i][1]))

    # checking global validity
    can_rotate = True
    for tile in global_tiles:
        if tile[0] < 0 or tile[0] >= 10:
            can_rotate = False
        elif tile[1] < 0 or tile[1] >= 20:
            can_rotate = False
        elif game_board[tile[0]][tile[1]] == "@":
            can_rotate = False
    if can_rotate:
        for tile in original_tiles:
            game_board[tile[0]][tile[1]] = '_'
        for tile in global_tiles:
            game_board[tile[0]][tile[1]] = '*'


def clear_line(game_board):
    lines_cleared = 0
    for i in range(20):
        full_row = True
        for column in game_board:
            if full_row and column[i] != '@':
                full_row = False
        if full_row:
            lines_cleared += 1
            for column in game_board:
                column.pop(i)
                column.insert(0, '_')
    return lines_cleared

if __name__ == '__main__':
    # game setup
    game_board = create_board()
    current_piece = random_piece()
    spawn_piece(game_board, current_piece)
    lines_cleared = 0
    score = 0
    score_table = [0, 40, 100, 300, 1200]
    # initialize counters 
    counter = 0
    counter_max = 15
    right_counter = 0
    left_counter = 0
    rotate_counter = 0
    # main loop
    running = True
    while running:
        if keyboard.is_pressed('left'):
            left_counter += 1
        elif keyboard.is_pressed('right'):
            right_counter += 1
        elif keyboard.is_pressed('f'):
            rotate_counter += 1
        elif keyboard.is_pressed('ESC'):
            running = False
            break

        if counter >= counter_max:
            counter = 0
            if right_counter >= counter_max//3:
                move(game_board, 'right')
                right_counter = 0
            elif left_counter >= counter_max//3:
                move(game_board, 'left')
                left_counter = 0
            if rotate_counter >= counter_max//3:
                rotate(game_board, current_piece)
                rotate_counter = 0
            print_board(game_board, lines_cleared, score)
            need_piece = drop(game_board)
            if need_piece:
                new_lines = clear_line(game_board)
                lines_cleared += new_lines
                score += score_table[new_lines]
                current_piece = random_piece()
                if spawn_piece(game_board, current_piece):
                    running = False
                    print("You lost!")
        time.sleep(0.02)
        counter += 1
