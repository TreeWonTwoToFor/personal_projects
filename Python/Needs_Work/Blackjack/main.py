import random
import os
import time

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
        self.update_hand_value()

    def update_hand_value(self):
        sum = 0
        num_aces = 0
        for card in self.card_array:
            sum += card.return_card_value()
            if (card.value == "A"):
                num_aces += 1
        if (sum > 21 and num_aces >= 1):
            for aces in range(num_aces):
                sum -= 10
        self.value = sum


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
    print(f"${cash}")

input("enter last 4 digits of credit card number: ")
user_bankroll = int(input("Please enter a bankroll: "))
user_bet = int(input("How much do you want to bet? "))
card_deck, player_hand, dealer_hand = new_shoe([])
print_all_fancy(dealer_hand, player_hand, True, user_bankroll, user_bet)

running = True
while running:
    game_over = False
    user_input = input("Hit (H), or Stay (S)? ")
    if user_input.lower() == "h":
        os.system("cls")
        player_hand.card_array.append(card_deck.pop())
        print_all_fancy(dealer_hand, player_hand, True, user_bankroll, user_bet)
        player_hand.update_hand_value()
        if player_hand.value > 21:
            game_over = True
    elif user_input.lower() == "s":
        os.system("cls")
        game_over = True
        print_all_fancy(dealer_hand, player_hand, False, user_bankroll, user_bet)
        while dealer_hand.value < 17:
            time.sleep(1)
            dealer_hand.card_array.append(card_deck.pop())
            print_all_fancy(dealer_hand, player_hand, False, user_bankroll, user_bet)
            dealer_hand.update_hand_value()
    elif user_input.lower() == "exit":
        running = False
    if game_over:
        winning = True
        dealer_hand.update_hand_value()
        player_hand.update_hand_value()
        if player_hand.value > 21 or (player_hand.value < dealer_hand.value and dealer_hand.value <= 21):
            winning = False
        if player_hand.value == dealer_hand.value:
            print("It's a tie! Do you want to play again?")
        else:
            if winning:
                print("You win! Do you want to play again?")
                user_bankroll += user_bet
            else:
                print("You lose. Do you want to play again?")
                user_bankroll -= user_bet
        while True:
            play_again = input("(Y)es/(N)o/(C)hange bet> ")
            if play_again.lower() == "y":
                if (len(card_deck) > 10):
                    player_hand, dealer_hand = deal_hands(card_deck)
                else:
                    card_deck, player_hand, dealer_hand = new_shoe([])
                print_all_fancy(dealer_hand, player_hand, True, user_bankroll, user_bet)
                break
            elif play_again.lower() == "n" or play_again.lower() == "exit":
                running = False
                break
            elif play_again.lower() == "c":
                user_bet = int(input("How much do you want to bet? "))
                if (len(card_deck) > 10):
                    player_hand, dealer_hand = deal_hands(card_deck)
                else:
                    card_deck, player_hand, dealer_hand = new_shoe([])
                print_all_fancy(dealer_hand, player_hand, True, user_bankroll, user_bet)
                break

os.system('cls')