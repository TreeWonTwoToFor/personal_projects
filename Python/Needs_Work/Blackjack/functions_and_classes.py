import random
import os

###########################################################################
#                              Classes                                    #
###########################################################################
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
        self.update_hand_value()

    def update_hand_value(self):
        sum = 0
        num_aces = 0
        for card in self.card_array:
            sum += card.return_card_value()
            if (card.value == "A"):
                num_aces += 1
        while (sum > 21 and num_aces >= 1):
            sum -= 10
            num_aces -= 1
        self.value = sum

    def has_ace(self):
        for card in self.card_array:
            if card.return_card_value() == 11:
                return True
        return False
###########################################################################

###########################################################################
#                             Functions                                   #
###########################################################################
def deal(hand, deck):
    for i in range(2):
        last_card = len(deck)-1
        hand.append(deck[last_card])
        deck.pop()

def print_hand_fancy(hand, is_dealer):
    card_string1 = ""
    card_string2 = ""
    card_string3 = ""
    card_string4 = ""
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
            card_string1 += ("-----")
            card_string2 += ("|   |")
            card_string3 += ("|   |")
            card_string4 += ("-----")
        else:
            card_string1 += ("-----")
            card_string2 += ("|" + first_letter[0].upper() + "  |")
            card_string3 += ("|  " + card.value + "|")
            card_string4 += ("-----")
        count += 1
    print(card_string1 + "\n" + card_string2 + "\n" + card_string3 + "\n" + card_string4)

def create_deck(deck):
    suit_list = ["diamond", "heart", "spade", "club"]
    value_list = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
    for i in range(4):
        for j in range(13):
            
            deck.append(card(suit_list[i], value_list[j]))

def new_shoe(deck):
    p_hand = []
    d_hand = []
    create_deck(deck)
    random.shuffle(deck)
    deal(p_hand, deck)
    deal(d_hand, deck)
    return (deck, hand(p_hand), hand(d_hand))

def deal_hands(deck):
    p_hand = []
    d_hand = []
    deal(p_hand, deck)
    deal(d_hand, deck)
    return (hand(p_hand), hand(d_hand))

def print_all_fancy(d_hand, p_hand, d_up, cash, bet):
    os.system("cls")
    print_hand_fancy(d_hand.card_array, d_up)
    print(f"""
    {bet}
    """)
    print_hand_fancy(p_hand.card_array, False)
    cent = cash % 1
    if cent == 0:
        cent = ".00"
    else:
        cent = "0"
    print(f"${cash}{cent}")
    print(p_hand.value)

def hands_to_basic_strategy(player_hand, dealer_hand):
    output = ""
    if dealer_hand.card_array[1].return_card_value() == 11:
        output += "A: "
    else:
        output += str(dealer_hand.card_array[1].return_card_value()) + ": "
    if player_hand.has_ace():
        if player_hand.card_array[0].return_card_value() == 11:
            output += "A, " + str(player_hand.card_array[1].return_card_value())
        else:
            output += "A, " + str(player_hand.card_array[0].return_card_value())
    elif player_hand.card_array[0].return_card_value() == player_hand.card_array[1].return_card_value():
        output += str(player_hand.card_array[0].return_card_value()) + ", " + str(player_hand.card_array[0].return_card_value())
    else:
        output += str(int(player_hand.card_array[0].return_card_value()) + int(player_hand.card_array[1].return_card_value()))
    print(output)

    