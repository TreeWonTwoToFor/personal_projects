import random
import os

os.system('cls')

class card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def return_card(self):
        return self.value + " of " + self.suit
    
    def return_card_value(self):
        out = 0
        match self.value:
            case "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                out = int(self.value)
            case "T" | "J" | "Q" | "K":
                out = 10
            case "A":
                out = 11 # should check if hand is above 21 with an Ace, then chop it by 10
        return out

class hand:
    def __init__(self, card_array):
        self.card_array = card_array
        self.value = self.return_hand_value()

    def return_hand_value(self):
        sum = 0
        num_aces = 0
        for card in self.card_array:
            sum += card.return_card_value()
            if (card.value == "A"):
                num_aces += 1
        if (sum > 21 and num_aces >= 1):
            for aces in range(num_aces):
                sum -= 10
                if (sum <= 21):
                    return sum
        return sum


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
        match card.suit:
            case "diamond":
                first_letter = "♦"
            case "spade":
                first_letter = "♠"
            case "heart":
                first_letter = "♥"
            case "club":
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

def start_game(deck, p_hand, d_hand):
    create_deck(deck)
    random.shuffle(deck)
    deal(p_hand, deck)
    deal(d_hand, deck)
    return (deck, hand(p_hand), hand(d_hand))

card_deck, player_hand, dealer_hand = start_game([], [], [])
print_hand_fancy(dealer_hand.card_array, True)
print("\n\n")
print_hand_fancy(player_hand.card_array, False)