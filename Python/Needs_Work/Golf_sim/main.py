import os
import random
import plotly.express as px

class hand:
    def __init__(self, deck):
        self.hand = []
        self.deck = deck
        self.value = 0
        self.generate_hand()
        self.score_hand()

    def generate_hand(self):
        for i in range(4):
            self.hand.append(self.deck.pop())

    def score_hand(self):
        for card in self.hand:
            self.value += card

def make_deck(has_jokers):
    my_deck = []
    for i in range(1, 14):
        for j in range(4):
            value_to_add = i
            if i == 11 or i == 12:
                value_to_add = 10
            elif i == 13:
                value_to_add = 0
            my_deck.append(value_to_add)
    if has_jokers:
        for i in range(2): my_deck.append(-1)
    my_deck.sort()
    return my_deck

def count_occurrence(a):
  k = {}
  for j in a:
    if j in k:
      k[j] +=1
    else:
      k[j] =1
  return k

def setup():
    global my_deck, player1_deck
    my_deck = make_deck(True)
    random.shuffle(my_deck)
    player1_deck = hand(my_deck)

def run():
    data = []
    for i in range(10000): # number of times game is simulated
        setup()
        data.append(player1_deck.value)
    data.sort()
    data_dict = count_occurrence(data)
    fig = px.line(x=data_dict.keys(), y=data_dict.values())
    fig.write_html('output_graph.html', auto_open=True)

setup()
run()