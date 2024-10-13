from deck import Deck
from hand import Hand 
import time
import os
import sys

num_cards = int(sys.argv[1])
counting_time = float(sys.argv[2])
num_decks = int(num_cards)//52

def main():
    hand_list = []
    for deck in range(num_decks):
        card_deck = Deck()
        card_deck.shuffle()
        for card in card_deck.draw(52):
            hand_list.append(card)
    hand = Hand(hand_list)
    count = 0
    for i in range(num_cards):
        os.system('clear')
        card = hand.return_list()[i]
        if card.value >= 10 or card.value == 1:
            count -= 1
        elif card.value <= 6:
            count += 1
        else:
            count += 0
        print(card.output())
        time.sleep(counting_time/num_cards)

    guess = input("What is the count?")
    if count == int(guess):
        print("You got it right!")
    else:
        print(f"Incorrect, the count was {count}")

running = True
while running:
    main()
    play_again = input("Do you want to play again (Y/N)? ")
    if play_again.lower() == 'y':
        pass
    elif play_again.lower() == 'n':
        running = False
