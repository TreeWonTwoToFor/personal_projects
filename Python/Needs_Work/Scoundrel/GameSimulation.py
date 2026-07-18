import random

class GameState:
    def __init__(self, health=20):
        self.room = []
        self.weapon = {
            "strength": 0,
            "last hit": None
        }
        self.health = health
        self.max_hp = health
        self.can_avoid = True

        self.is_tabbed = False
        self.negative_health = False

    def __str__(self):
        if self.is_tabbed:
            return f"HP: {self.health} | Weapon: {self.weapon['strength']} ({self.weapon["last hit"]})\n\t{self.room}"
        return f"HP: {self.health} | Weapon: {self.weapon['strength']} ({self.weapon["last hit"]})\n{self.room}"
    
    # returns the number of cards being drawn by the dungeon deck
    def do_turn(self, turn_type, turn_array, decision_array=[False, False, False]):
        match turn_type:
            case "avoid":
                # we need to put the four cards on the bottom of the deck, and draw a new hand. this should make it impossible to draw again until after another draw
                if self.can_avoid:
                    self.can_avoid = False # must face the next room
                    self.avoided_room = self.room
                    self.room = []
                    return 4 
                else:
                    return -2
            case "fight":
                self.can_avoid = True
                for idx in range(3):
                    i = turn_array[idx]
                    decision = decision_array[idx]
                    card = self.room[i]
                    match card[1]:
                        case "monster":
                            if self.weapon["strength"] != 0 and (self.weapon["last hit"] == None or self.weapon["last hit"] > card[0]) and decision:
                                self.health -= max(0, card[0]-self.weapon["strength"])
                                self.weapon["last hit"] = card[0]
                            else:
                                # either we picked to not use our weapon, it wasn't strong enough, or we didn't have one.
                                self.health -= card[0]
                            if self.health <= 0 and not self.negative_health:
                                return -1 # i.e. the player died
                        case "weapon":
                            self.weapon = {
                                "strength": card[0],
                                "last hit": None
                            }
                        case "potion":
                            self.health = min(self.max_hp, self.health + card[0])
                # if we made it out of the loop, the player is still alive, and needs to get new cards
                turn_array.sort(reverse=True)
                for i in turn_array:
                    self.room.remove(self.room[i])
                return 3
            
    def screen_for_weapon_hits(self, turn_array):
        projected_weapon = {
            "strength" : self.weapon["strength"],
            "last hit" : self.weapon["last hit"]
        }
        decision_list = [False, False, False]
        decision_index = 0
        for i in turn_array:
            card = self.room[i]
            match card[1]:
                case "monster":
                    if projected_weapon["strength"] != 0 and (projected_weapon["last hit"] == None or projected_weapon["last hit"] >= card[0]):
                        # the player has the option to hit, or to not hit.
                        decision_list[decision_index] = True
                        projected_weapon["last hit"] = card[0]
                case "weapon":
                    projected_weapon = {
                        "strength": card[0],
                        "last hit": None
                    }
            decision_index += 1
        return decision_list


class DungeonDeck:
    def __init__(self, deck_size=44):
        self.deck = []
        self.deck_size = deck_size
        self.generate_deck()
        random.shuffle(self.deck)
        self.deck = self.deck[:self.deck_size]

    def __len__(self):
        return len(self.deck)

    def generate_deck(self):
        card_types = ["weapon", "potion", "monster"]
        for type in card_types:
            if type == "monster":
                for i in range(2,15):
                    self.deck.append((i, type))
                    self.deck.append((i, type))
            else:
                for i in range(2,11):
                    self.deck.append((i, type))
    
    def draw_room(self, num_cards):
        if len(self.deck) >= num_cards:
            return [self.deck.pop() for i in range(num_cards)]
        else:
            raise ValueError("You Escaped!")
    
def game_logic(player_action, decision_list, state, deck):
    output = ""
    num_cards_to_draw = state.do_turn(*player_action, decision_list)
    try:
        match num_cards_to_draw:
            case -1:
                output = "died"
            case -2:
                output = "cannot avoid"
            case 3:
                state.room = state.room + deck.draw_room(3)
            case 4:
                deck.deck = state.avoided_room + deck.deck
                state.room = deck.draw_room(4)
    except:
        output = "escaped"
    return output

def main():
    my_deck = DungeonDeck()
    my_state = GameState()

    my_state.room = my_deck.draw_room(4)

    running = True
    while running:
        # printing game state
        print(my_state)
        print(f"Number of cards left: {len(my_deck)}")
        player_input = input("What do you do > ").lower()

        # primary player action
        player_action = None
        if player_input == "avoid":
            player_action = ("avoid", [])
        else:
            action_list = player_input.split(" ")
            for i in range(len(action_list)):
                action_list[i] = int(action_list[i])
            player_action = ("fight", action_list)

        # is there a weapon choice needed?
        decision_list = my_state.screen_for_weapon_hits(player_action[1])
        if any(decision_list):
            for i in range(len(decision_list)):
                card_number = player_action[1][i]
                if decision_list[i]:
                    decision = input(f"Use weapon on {card_number}? (y/n): ").lower()
                    if decision == 'y':
                        decision_list[i] = True
                    elif decision == 'n':
                        decision_list[i] = False
        # print(decision_list)

        logic_output = game_logic(player_action, decision_list, my_state, my_deck)
        match logic_output:
            case "died":
                running = False
                print("Sorry, you died!")
            case "escaped":
                running = False
                print("<<  You Escaped!  >>")
            case "cannot avoid":
                print("You are not allowed to avoid two rooms in a row.")
        print()

if __name__ == "__main__":
    main()