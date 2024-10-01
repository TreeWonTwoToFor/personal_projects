import os
import time
from functions_and_classes import *

###########################################################################
#                           Initial setup                                 #
###########################################################################
clear_type = "clear"
os.system(clear_type)
testing = True
if not testing:
    user_bankroll = int(input("Please enter a bankroll: "))
    user_bet = int(input("How much do you want to bet? "))
else:
    user_bankroll = 1000
    user_bet = 25
old_bet = user_bet
card_deck, player_hand, dealer_hand = new_shoe([])
print_all_fancy(dealer_hand, player_hand, True, user_bankroll, user_bet)
###########################################################################

running = True
while running:
    # Basic setup
    dealer_hand.update_hand_value()
    dealer_upcard = dealer_hand.card_array[1].return_card_value()
    is_insurance_possible = (dealer_upcard == 11) and player_hand.value != 21
    need_player_decision = True
    can_double = True
    insurance_status = ""

    os.system(clear_type)
    print_all_fancy(dealer_hand, player_hand, True, user_bankroll, user_bet)

    if not is_insurance_possible and dealer_hand.value == 21:
        need_player_decision = False

    # Handing the possible insurance
    if is_insurance_possible:
        need_insurance_decision = True
        want_insurance = input("Do you want to bet on insurance (Y/N)?")
        while need_insurance_decision:
            if want_insurance.lower() == "y":
                need_insurance_decision = False
                insurance_bet = int(input("How much do you want to bet on insurance? "))
                if insurance_bet <= user_bet/2:
                    print(f'insurance: {insurance_bet}')
                    if dealer_hand.value == 21:
                        insurance_status = "player won"
                        need_player_decision = False
                    else:
                        insurance_status = "player lost"
                    input()
                else:
                    print("Please place a valid bet (0 if you don't want insurance)")
                    need_player_decision, need_insurance_decision = True, True
            elif want_insurance.lower() == "n":
                need_insurance_decision = False
                insurance_status = "no insurance bet"
                insurance_bet = 0
                if dealer_hand.value == 21:
                    need_player_decision = False
            else:
                print("Need a valid input.")
                want_insurance = input("Do you want to bet on insurance (Y/N)?")

    # Player's turn
    while need_player_decision:
        os.system(clear_type)
        print_all_fancy(dealer_hand, player_hand, True, user_bankroll, user_bet)
        if insurance_status == "player lost":
             print("You lost the insurance bet. You lost $" + str(insurance_bet))
        if player_hand.value >= 21:
            need_player_decision = False
            break
        hands_to_basic_strategy(player_hand, dealer_hand)
        if can_double:
            user_input = input("Hit, Stay, or Double (H/S/D)? ")
        else:
            user_input = input("Hit, or Stay (H/S)?")
        if user_input.lower() == "h":
            can_double = False
            player_hand.card_array.append(card_deck.pop())
            player_hand.update_hand_value()
        elif user_input.lower() == "d" and can_double:
            old_bet = user_bet
            user_bet = user_bet * 2
            player_hand.card_array.append(card_deck.pop())
            player_hand.update_hand_value()
            need_player_decision = False
            # make sure this bet and only one card rule works
        elif user_input.lower() == "s":
            need_player_decision = False
            break

    # Dealer's turn
    dealer_playing = True
    while dealer_playing:
        os.system(clear_type)
        print_all_fancy(dealer_hand, player_hand, False, user_bankroll, user_bet)
        if player_hand.value >= 21:
            dealer_playing = False
            break
        if dealer_hand.value >= 17:
            dealer_playing = False
            break
        else: # the dealer still needs to hit
            dealer_hand.card_array.append(card_deck.pop())
            dealer_hand.update_hand_value()
        time.sleep(1)

    # Deciding the winner
    player_won = False
    three_two_pay = False
    is_tie = False
    if player_hand.value == 21 and len(player_hand.card_array) == 2:
        three_two_pay = True
    else:
        if insurance_status is not "":
            match insurance_status:
                case "player won":
                    print("You won the insurance bet!")
                    user_bankroll += insurance_bet * 2
                case "player lost":
                    print("You lost the insurance bet. You lost $" + str(insurance_bet))
                    user_bankroll -= insurance_bet
        if dealer_hand.value > 21 or (player_hand.value > dealer_hand.value and player_hand.value <= 21):
            player_won = True
        if player_hand.value == dealer_hand.value and player_hand.value <= 21:
            is_tie = True

    # Handling the bet
    if three_two_pay:
        winnings = user_bet * 1.5
        user_bankroll += winnings
        print("Congrats! You won $" + str(winnings) + " due to a natural!")
    elif player_won:
        user_bankroll += user_bet
        print("Congrats! You won $" + str(user_bet) + "!")
    elif is_tie:
        print("Due to a tie, your bet has been pushed.")
    elif insurance_status == "player won":
        print("You have protected your main bet with insurance!")
    else: # player must have lost
        user_bankroll -= user_bet
        print("You lost the hand ($" + str(user_bet) + "). Better luck next time.")
    user_bet = old_bet

    # Post hand 
    post_game = True
    while post_game:
        user_input = input("Do you want to play again, or change the bet (Y/N/C)? ").lower()
        if user_input == "y" or user_input == "c" or user_input == "":
            if (len(card_deck) > 10):
                player_hand, dealer_hand = deal_hands(card_deck)
            else:
                card_deck, player_hand, dealer_hand = new_shoe([])
        if user_input == "y" or user_input == "":
            post_game = False
        elif user_input == "n" or user_input == "exit":
            post_game = False
            running = False
            break
        elif user_input == "c":
            user_bet_wish = input("How much do you want to bet? ")
            while False:
                try:
                    user_bet = int(user_bet_wish)
                    break
                except:
                    print("Please enter a valid input")
            post_game = False
        else:
            print("Please enter a valid input")

os.system(clear_type)
