import random

deck_contents = {
    "Tempura": 14,
    "Sashimi": 14,
    "Dumpling": 14,
    "Maki Roll - 1": 6,
    "Maki Roll - 2": 12,
    "Maki Roll - 3": 8,
    "Nigiri - Egg": 5,
    "Nigiri - Salmon": 10,
    "Nigiri - Squid": 5,
    "Pudding": 10,
    "Wasabi": 6,
    "Chopsticks": 4,
}

class Player:
    def __init__(self, hand, table=[], pudding=[]):
        self.hand = hand
        self.table = table
        self.pudding = pudding
        self.maki = 0
        self.score = 0

    def play_card(self, card_index):
        card = self.hand.pop(card_index)
        self.table.append(card)

    def update_score(self):
        card_table = []
        num_table = []
        # count the number of times each card appears
        for card in self.table:
            if card not in card_table:
                card_table.append(card)
                num_table.append(1)
            else:
                num_table[card_table.index(card)] += 1
        # add to self.score based on the card, and it's number
        for card in card_table:
            card_num = num_table[card_table.index(card)]
            card_name_list = card.split()
            wasabi_count = 0
            match card_name_list[0]:
                case "Pudding":
                    self.pudding += 1
                case "Wasabi":
                    wasabi_count += 1
                case "Maki": # "Maki Roll - #####"
                    self.maki += int(card_name_list[3])
                case "Tempura":
                    self.score += (card_num//2)*5
                case "Sashimi":
                    self.score += (card_num//3)*10
                case "Dumpling": # 1 3 6 10 15
                    match card_num:
                        case 0: self.score += 0
                        case 1: self.score += 1
                        case 2: self.score += 3
                        case 3: self.score += 6
                        case 4: self.score += 10
                        case 5: self.score += 15
                        case _: self.score += 15
                case "Nigiri":
                    if wasabi_count:
                        wasabi_count -= 1
                        mult = 3
                    else:
                        mult = 1
                    match card_name_list[2]: # "Nigiri - #####"
                        case "Egg": self.score += 1*mult
                        case "Salmon": self.score += 2*mult
                        case "Squid": self.score += 3*mult
            print(f"{card} - {num_table[card_table.index(card)]}")
        print(num_table, card_table)

def create_card_deck():
    deck = []
    for card in deck_contents:
        for i in range(deck_contents[card]):
            deck.append(card)
    return deck

card_deck = create_card_deck()
random.shuffle(card_deck)
player_a = Player([])
player_b = Player([])
for i in range(10):
    player_a.hand.append(card_deck.pop())
    player_b.hand.append(card_deck.pop())
print(player_a.hand)
for i in range(10):
    player_a.play_card(0)
player_a.update_score()