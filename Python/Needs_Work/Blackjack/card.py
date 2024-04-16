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