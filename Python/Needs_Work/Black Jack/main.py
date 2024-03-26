import random
import os

os.system('cls')

class card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def return_card(self):
        return self.value + " of " + self.suit

def deal(hand, deck):
    for i in range(2):
        last_card = len(deck)-1
        hand.append(deck[last_card])
        deck.pop()

def print_hand_basic(hand_name, hand):
    print(hand_name + "\n###############")
    for card in hand:
        print(card.return_card())
    print()

def print_hand_fancy(hand, is_dealer):
    count = 0
    for card in hand:
        if card.suit == "diamond":
            first_letter = "♦"
        elif card.suit == "heart":
            first_letter = "♥"
        elif card.suit == "spade":
            first_letter = "♠"
        else: # must be a club
            first_letter = "♣"
        if is_dealer and count == 0:
            print("-----")
            print("|   |")
            print("|   |")
            print("-----")
        else:
            print("-----")
            print("|" + first_letter[0].upper() + "  |")
            print("|  " + card.value + "|")
            print("-----")
        count += 1

def create_deck(deck):
    suit_list = ["diamond", "heart", "spade", "club"]
    value_list = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
    for i in range(4):
        for j in range(13):
            deck.append(card(suit_list[i], value_list[j]))

card_deck = []
player_hand = []
dealer_hand = []

create_deck(card_deck)
random.shuffle(card_deck)
deal(player_hand, card_deck)
deal(dealer_hand, card_deck)
print_hand_fancy(dealer_hand, True)
print("\n\n")
print_hand_fancy(player_hand, False)