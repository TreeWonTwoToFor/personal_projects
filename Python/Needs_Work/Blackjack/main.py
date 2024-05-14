import os
import time
from functions_and_classes import print_all_fancy, new_shoe, deal_hands, hands_to_basic_strategy

###########################################################################
#                           Initial setup                                 #
###########################################################################
os.system('cls')
testing = True
if not testing:
    input("enter last 4 digits of credit card number: ")
    user_bankroll = int(input("Please enter a bankroll: "))
    user_bet = int(input("How much do you want to bet? "))
else:
    user_bankroll = 1000
    user_bet = 25
old_bet = user_bet
card_deck, player_hand, dealer_hand = new_shoe([])
print_all_fancy(dealer_hand, player_hand, True, user_bankroll, user_bet)
###########################################################################

logic_style = "new"
running = True
while running:
    # NEW LOGIC STYLE
    if logic_style == "new":
        # Basic setup
        dealer_hand.update_hand_value()
        dealer_upcard = dealer_hand.card_array[1].return_card_value()
        is_insurance_possible = (dealer_upcard == 11)
        need_player_decision = True
        insurance_status = ""

        os.system('cls')
        print_all_fancy(dealer_hand, player_hand, True, user_bankroll, user_bet)

        if not is_insurance_possible and dealer_hand.value == 21:
            need_player_decision = False

        # Handing the possible insurance
        if is_insurance_possible:
            need_insurance_decision = True
            while need_insurance_decision:
                want_insurance = input("Do you want to bet on insurance (Y/N)?")
                if want_insurance.lower() == "y":
                    need_player_decision, need_insurance_decision = False, False
                    insurance_bet = int(input("How much do you want to bet on insurance? "))
                    print(f'insurance: {insurance_bet}')
                    # FIXME: double check that insuarnce bet is below half of main bet + that it is a valid number
                    if dealer_hand.value == 21:
                        insurance_status = "player won"
                    else:
                        insurance_status = "player lost"
                    input()
                elif want_insurance.lower() == "n":
                    need_insurance_decision = False
                    insurance_status = "no insurance bet"
                    insurance_bet = 0
                else:
                    print("Need a valid input (Y/N).")
        
        # Player's turn
        while need_player_decision:
            os.system('cls')
            print_all_fancy(dealer_hand, player_hand, True, user_bankroll, user_bet)
            if player_hand.value >= 21:
                need_player_decision = False
                break
            hands_to_basic_strategy(player_hand, dealer_hand)
            user_input = input("Hit, Stay, or Double (H/S/D)? ")
            if user_input.lower() == "h":
                player_hand.card_array.append(card_deck.pop())
                player_hand.update_hand_value()
            elif user_input.lower() == "d":
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
            os.system('cls')
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
        if insurance_status is not "":
            match insurance_status:
                case "player won":
                    print("yippee")
                    user_bankroll += insurance_bet
                case "player lost" | "no insurance bet":
                    print("waaaahhhh")
                    user_bankroll -= insurance_bet
        if dealer_hand.value > 21 or (player_hand.value > dealer_hand.value and player_hand.value <= 21):
            player_won = True
        if player_hand.value == 21 and len(player_hand.card_array) == 2:
            three_two_pay = True
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
        else: # player must have lost
            user_bankroll -= user_bet
            print("You lost $" + str(user_bet) + ". Better luck next time.")
        user_bet = old_bet

        # Post hand 
        post_game = True
        while post_game:
            user_input = input("Do you want to play again, or change the bet (Y/N/C)? ").lower()
            if user_input == "y" or user_input == "c":
                if (len(card_deck) > 10):
                    player_hand, dealer_hand = deal_hands(card_deck)
                else:
                    card_deck, player_hand, dealer_hand = new_shoe([])
            if user_input == "y":
                post_game = False
            elif user_input == "n":
                post_game = False
                running = False
                break
            elif user_input == "c":
                user_bet = int(input("How much do you want to bet? "))
                post_game = False
            else:
                print("Please enter a valid input")

    # OLD LOGIC STYLE
    if logic_style == "old":
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