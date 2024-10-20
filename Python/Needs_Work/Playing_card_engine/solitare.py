from card import Card
from deck import Deck
from hand import Hand

deck = Deck()
deck.shuffle()
column_list   = [None]*7
heart_stack   = []
diamond_stack = []
spade_stack   = []
club_stack    = []

for i in range(7):
    column = Hand(deck.draw(i+1))
    column.return_list()[-1].face_up = True
    column_list[i] = column

def print_board():
    # ace stacks
    print(' '*12, end='')
    stack_list = [heart_stack, club_stack, diamond_stack, spade_stack]
    out_stack = []
    for stack in stack_list:
        if len(stack) != 0:
            out_stack.append(stack[-1])
        else:
            out_stack.append("empty")
    for card in out_stack:
        if card != "empty":
            print(card.output(3), end='')
        else:
            print('[  ]', end='')
    print('\n')
    # game board
    current_row = 0
    printing = True
    while printing:
        row_list = []
        for column in column_list:
            if len(column.return_list()) >= current_row + 1:
                card = column.return_list()[current_row]
                row_list.append(card.output(3))
        print("    "*current_row + "".join(row_list))
        current_row += 1
        if current_row > 6:
            printing = False

print_board()


