import numpy as np
import csv
from copy import deepcopy as copy
import GameSimulation as Scoundrel
from EvolutionAlgo import *
import math
import multiprocessing
import time

# parameters for the NN and evolution algorithm
network_structure = [13, 10, 10, 5]
population_size = 1000
games_per_generation = 50
number_of_generations = 5000
number_of_parents = population_size//20
growth_rate = 0.05
mutation_strength = 0.2

num_threads = 4


# Fitness Function
# we need to be able to score our network based on how well it does in specific test runs
# there's a bunch of different ways to do this, so it'll take some experimentation to find what works in the long run. 
# I do have a bunch of ideas as to what will be useful though, so we can start with that
#   lower number of cards, higher health value, being able to avoid, having a high value weapon (both str and last hit being high)
def fitness_function(game_state, card_deck):
    # the score works on a range from 1 to 100
    # inverse relationship, so less cards in the deck is good
    return 100 * (game_state.health / game_state.max_hp)

    dungeon_score = 50 * (1 - (len(card_deck) / card_deck.deck_size))

    health_score = 25 * (game_state.health / 20)

    weapon_strength = game_state.weapon["strength"]
    weapon_last_hit = game_state.weapon["last hit"]
    if weapon_last_hit == None: 
        if weapon_strength != 0:
            weapon_last_hit = max(15, weapon_strength+1)
        else:
            weapon_last_hit = 0
    weapon_score = 20 - 20 * (weapon_last_hit / 15)

    avoidance_score = 5 if game_state.can_avoid else 0

    return dungeon_score + health_score + weapon_score + avoidance_score


def ai_plays_scoundrel(deck, state, network, current_generation_number=-1, printing=False):
    type_dictionary = {
        "monster": 0,
        "weapon": 1,
        "potion": 2
    }
    playing = True
    # while state.health > 0 and playing:
    while playing:
        # feed the NN input data
        network_input = np.array([len(deck),
                                    state.health, 
                                    1 if state.can_avoid else 0,
                                    state.weapon["strength"],
                                    15 if state.weapon["last hit"] == None else state.weapon["last hit"],
                                    state.room[0][0],
                                    state.room[1][0],
                                    state.room[2][0],
                                    state.room[3][0],
                                    type_dictionary[state.room[0][1]],
                                    type_dictionary[state.room[1][1]],
                                    type_dictionary[state.room[2][1]],
                                    type_dictionary[state.room[3][1]]]).reshape(13,1)
        if printing:
            print(f"\tCards left: {len(deck)} | {state}")
        # get the output from the NN
        network_output = network.forward(network_input).flatten().tolist() # numpy array back to python
        # decide what the ai is going to do based on it's outputs
        player_action = None
        if network_output[0] > 0 and state.can_avoid:
            # the ai wants to avoid the room
            player_action = ("avoid", [])
        else:
            action_list = []
            network_card_weights = network_output[1:]
            for j in range(3):
                # we pick the highest activation, and then rule it out by giving a very large negative number
                player_pick = max(network_card_weights)
                action_list.append(network_card_weights.index(player_pick))
                network_card_weights[network_card_weights.index(player_pick)] = -9999999999
            player_action = ("fight", action_list)
        decision_list = state.screen_for_weapon_hits(player_action[1])
        if printing: print('\t',player_action, [round(x, 2) for x in network_output])
        
        # run the game based on the ai choices
        logic_output = Scoundrel.game_logic(player_action, decision_list, state, deck)
        match logic_output:
            case "died":
                # they ran out of health, but because our fitness function is based on hp,
                #   we want all of the bots to be rankedo even footing, rather than
                #   which one died by the least amount in any specific room
                pass
            case "escaped":
                if printing:
                    print("escaped")
                if state.health > 0:
                    return 1 # we won, so count this game as a win!
                else:
                    return 0 
            case "cannot avoid":
                # ai tries to avoid when it can't. handled by output mapping into scoundrel
                pass
        # if printing and state.health > 0: 
        #     print()
    return 0

def visual_ai_play(network):
    deck_instance = Scoundrel.DungeonDeck()
    state_instance = Scoundrel.GameState()
    state_instance.negative_health = True
    state_instance.room = deck_instance.draw_room(4)
    state_instance.is_tabbed = True
    ai_plays_scoundrel(deck_instance, state_instance, network, printing=True)

def run_thread(decks, networks, games_per_generation, generation):
    number_of_winners = 0
    # losing 30 health over 500 generations equates to being at 20 hp at generation 500.
    health = 20
    if generation <= 500:
        health = int(50 - 30/500 * generation)
    for i in range(games_per_generation):
        initial_deck = decks[i]
        initial_state = Scoundrel.GameState(health=health)
        initial_state.negative_health = True # we want all bots to be ranked equally
        for j in range(len(networks)):
            player, player_fitness = networks[j]
            deck_instance = copy(initial_deck)
            state_instance = copy(initial_state)
            state_instance.room = deck_instance.draw_room(4)
            number_of_winners += ai_plays_scoundrel(deck_instance, state_instance, player, generation)
            # step 2: give them a fitness score
            ai_score = fitness_function(state_instance, deck_instance)
            networks[j][1] = player_fitness + ai_score
    return number_of_winners, networks

def run_generation(population, games_per_generation, generation):
    global number_of_winners
    number_of_winners = 0
    decks = [Scoundrel.DungeonDeck() for game in range(games_per_generation)]
    # here we create our threads to split the games across multiple threads
    #   so, each thread receives all of the decks, and gets pop/threads number of networks
    networks_per_thread = len(population)//num_threads # assume that it's evenly divisible
    thread_args = []
    for i in range(num_threads):
        start = i*networks_per_thread
        end = (i+1)*networks_per_thread
        networks = population[start:end]
        thread_args.append([copy(decks), networks, games_per_generation, generation])
    # now that we've constructed all of our arguments for each thread, we run them, and tally up the scores
    population = []
    with multiprocessing.Pool(num_threads) as p:
        output = p.starmap(run_thread, thread_args)
        for x in output:
            number_of_winners += x[0]
            population = population + x[1]
    return number_of_winners, population

def training_time(start_time, end_time):
    reported_time = round(time.time()-training_started, 2)
    reported_time_type = "seconds"
    if reported_time / 360 > 1:
        reported_time = reported_time / 360
        reported_time_type = "hours"
    elif reported_time / 60 > 1:
        reported_time = reported_time / 60
        reported_time_type = "minutes"
    print(f"Finished training. Time elapsed: {reported_time} {reported_time_type}")

if __name__ == "__main__":
    # here is the start of the actual running of the AI!
    training_started = time.time()
    training_data = []
    grand_champion = [None, -math.inf]
    generation_champion = None
    population = create_initial_population(population_size, network_structure)
    for generation in range(1, number_of_generations+1):
        number_of_wins, population = run_generation(population, games_per_generation, generation)
        max_fitness = games_per_generation*100
        generation_champion = pick_parents(population, 1)[0]
        if generation_champion[1] > grand_champion[1]:
            grand_champion_network = generation_champion[0]
            grand_champion_fitness = generation_champion[1]
            grand_champion = [grand_champion_network, grand_champion_fitness]
        champion_fitness = round(generation_champion[1], 2)
        grand_champion_fitness = round(grand_champion[1], 2)
        total_fitness = 0
        for player in population:
            total_fitness += player[1]
        average_fitness = round(total_fitness/population_size, 2)
        print(f"""Generation {generation} ({round(generation/number_of_generations*100, 2)}%):
        \tGrand Champion: {grand_champion_fitness}
        \tChampion: {champion_fitness}
        \tAverage: {average_fitness}
        \tWins: {number_of_wins} ({round(100*number_of_wins/(games_per_generation*population_size), 2)}%)""")
        print('\t' + '-'*15)
        data_point = [generation, champion_fitness, average_fitness, number_of_wins]
        visual_ai_play(generation_champion[0])
        training_data.append(data_point)
        parents = pick_parents(population, number_of_parents)
        population = create_next_population(parents, population_size, growth_rate, mutation_strength)
    training_time(training_started, time.time())

    # write out the resulting data to a csv file, s.t. it can be viewed later + analyzed
    with open('result_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(training_data)

    with open('result_config.txt', 'w', newline='') as file:
        config_dict = {
            "population_size": population_size,
            "games per generation": games_per_generation,
            "total number of generations": number_of_generations,
            "parents taken per generation": number_of_parents,
            "growth rate": growth_rate,
            "mutation strength": mutation_strength
        }
        config = f"Network layer structure: {network_structure}\nConfig:\n"
        for key in config_dict.keys():
            config = config + '\t' + key + ": " + str(config_dict[key]) + '\n'
        file.write(config)

    # now that we've finished our training, we want to see a player in action!
    print(f'\nChampion Fitness: {grand_champion[1]}')
    visual_ai_play(grand_champion[0])
    grand_champion[0].write_to_file()