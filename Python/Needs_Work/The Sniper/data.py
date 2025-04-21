def join_list(list, spacer, is_multiline=False):
    if is_multiline:
        return '```'+spacer.join(map(str, list))+'```'
    else:
        return spacer.join(map(str, list))

def load_leaderboard():
    leaderboard = open("leaderboard.json", 'r')
    