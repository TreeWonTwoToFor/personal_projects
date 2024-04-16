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