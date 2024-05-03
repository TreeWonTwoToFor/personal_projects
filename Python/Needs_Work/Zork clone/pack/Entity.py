class entity:
    def __init__(self, name, x, y, action_list):
        self.name = name
        self.x = x
        self.y = y
        self.action_list = action_list

    def do_action(self, player_input, player_x, player_y):
        if player_x == self.x and player_y == self.y:
            for action in self.action_list:
                if player_input == action[0]:
                    return action[1]
        else:
            return "You can't do that to the " + self.name