import os
import random
import plotly.express as px
import plotly.subplots as ps

graph_name = "1.html"
graph_num = 1

class hand:
    def __init__(self, deck):
        self.hand = []
        self.visible_hand = []
        self.value = 0
        self.visible_value = 0
        self.deck = deck
        self.generate_hand()
        self.score_hand()

    def generate_hand(self):
        for i in range(4):
            self.hand.append(self.deck.pop())
            if i < 2:
                self.visible_hand.append(self.hand[i])

    def score_hand(self):
        for card in self.hand:
            self.value += card
        for card in self.visible_hand:
            self.visible_value += card

    def draw_card(self): # FIXME accidently gets more points than before. My guess is the index is pointing to the wrong card
        new_card = self.deck.pop()
        for i in range(len(self.visible_hand)):
            if self.visible_hand[i] > new_card:
                self.visible_hand[i] = new_card
                self.hand[i] = new_card
        self.score_hand()

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
    global my_deck, player_hand
    my_deck = make_deck(True)
    random.shuffle(my_deck)
    player_hand = hand(my_deck)

def change():
    global player_hand, graph_name, graph_num
    player_hand.draw_card()
    graph_num += 1
    graph_name = str(graph_num) + ".html"

def run():
    data = []
    for i in range(10): # number of times game is simulated
        setup()
        data.append(player_hand.visible_value)
    data.sort()
    data_dict = count_occurrence(data)
    print(data_dict)
    fig = px.line(x=data_dict.keys(), y=data_dict.values())
    fig.write_html(graph_name, auto_open=True)

setup()
run()
change()
run()