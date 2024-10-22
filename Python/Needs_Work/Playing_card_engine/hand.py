from card import Card
from deck import Deck

class Hand:
    def __init__(self, card_list):
        self.card_list = card_list
        self.size = len(card_list)
        
    def print(self): 
        for card in self.card_list:
            if card.face_up:
                print(f"[{card.output()}] ", end="")
            else:
                print("[  ]", end="")
        print()

    def return_list(self):
        return self.card_list

    def sort(self, sort_style: int = 0):
        match sort_style:
            case 0: # sorting by purely value
                value_list, out_list = [], [None]*self.size
                for i in range(self.size):
                    value_list.append((self.card_list[i].value, i))
                for j in range(self.size):
                    for i in range(self.size-1):
                        if value_list[i][0] > value_list[i+1][0]:
                            temp = value_list[i]
                            value_list[i] = value_list[i+1]
                            value_list[i+1] = temp
                for i in range(self.size):
                    out_list[i] = self.card_list[value_list[i][1]]
                self.card_list = out_list

    def add_cards(self, second_hand):
        print(type(self.card_list), type(second_hand.card_list))
        self.card_list = self.card_list + second_hand.card_list


if __name__ == "__main__":
    card_deck = Deck()
    card_deck.shuffle()
    hand = Hand(card_deck.draw(12))
    hand.print()
    hand.sort()
    hand.print()
