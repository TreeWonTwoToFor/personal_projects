from card import Card
from deck import Deck
from hand import Hand

deck = Deck()
deck.shuffle()
column_list = [None]*7
heart_stack   = []
diamond_stack = []
spade_stack   = []
club_stack    = []

for i in range(7):
    column = Hand(deck.draw(i+1))
    column.return_list()[-1].face_up = True
    column_list[i] = column

for column in column_list:
    column.print()

print('-'*40)

# attempting print the screen as if you were laying the cards down like in solitare
counter = 0
for column in column_list:
    for i in range(len(column_list)):
        column = column_list[i+counter]
        print(f'[{column.return_list()[counter].output(2)}]', end=' ')
    counter += 1
    print()
