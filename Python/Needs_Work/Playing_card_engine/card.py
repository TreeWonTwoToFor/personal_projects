class Card:
    def __init__(self, value: int, suit: str) -> None:
        self.value = value
        self.suit = suit
        self.face_up = False
        self.get_rank()
        self.get_symbol()

    def get_rank(self) -> None:
        if self.value < 1 or self.value > 13:
            raise ValueError(f"Invalid card value of {self.value}")
        match self.value:
            case 1:
                self.rank = "A"
            case 11:
                self.rank = "J"
            case 12:
                self.rank = "Q"
            case 13:
                self.rank = "K"
            case _:
                self.rank = str(self.value)

    def get_symbol(self) -> None:
        match self.suit:
            case "heart":
                self.symbol = '♥'
            case "diamond":
                self.symbol = '♦'
            case "spade":
                self.symbol = '♠'
            case "club":
                self.symbol = '♣'
            case _:
                raise ValueError(f"{self.suit} is not a valid suit")

    def output(self, o_type: int=1) -> str:
        match o_type:
            case 1:
                return f"{self.rank}{self.symbol}"

if __name__ == "__main__":
    card_list = []
    for val in range(1, 14):
        match val % 4:
            case 0: card_list.append(Card(val, "heart"))
            case 1: card_list.append(Card(val, "diamond"))
            case 2: card_list.append(Card(val, "spade"))
            case 3: card_list.append(Card(val, "club"))
    for card in card_list:
        print(card.output())
