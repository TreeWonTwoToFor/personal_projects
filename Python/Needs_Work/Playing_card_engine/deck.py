from card import Card
import random

class Deck:
    def __init__(self) -> None:
        self.list = []
        self.generate()
        self.size = 52
        
    def generate(self) -> None:
        for suit in ["heart", "diamond", "spade", "club"]:
            for val in range(13):
                self.list.append(Card(val+1, suit))  

    def shuffle(self) -> None:
        random.shuffle(self.list)

    def pop(self) -> Card:
        self.size -= 1
        return self.list.pop(0)

    def draw(self, num: int) -> list:
        # this will output a list of cards, not names
        out_list = []
        for i in range(num):
            out_list.append(self.pop())
        return out_list

if __name__ == "__main__":
    card_deck = Deck()
    card_deck.shuffle()
    hand = card_deck.draw(7)
    for card in hand:
        print(card.output())
