import numpy as np
from NeuralNetwork import Network
from copy import deepcopy as copy


# For each generation, we're going to have a set of steps that we'll follow, before having it step into the next generation.
# 0. create children for initial generation (create_initial_population)
# 1. run them through the simulation (not listed here)
# 2. give them a fitness score (not listed here)
# 3. picking the best candidates (pick_parents)
# 4. have those parents then create new children for the next generation (create_next_population/mutate_nn_layer)

def create_initial_population(pop_size, network_structure):
    population = []
    inital_fitness_score = 0
    for i in range(pop_size):
        population.append([Network(network_structure), inital_fitness_score])
    return population

def mutate_nn_layer(Z, growth_rate, mutation_strength):
    mask = (
        np.random.random(Z.shape)
        < growth_rate
    )

    Z += (
        mask *
        np.random.normal(
            0,
            mutation_strength,
            Z.shape
        )
    )

def create_next_population(parents, pop_size, growth_rate, mutation_strength):
    inital_fitness_score = 0
    for parent in parents:
        parent[1] = inital_fitness_score
    population = copy(parents)
    while len(population) < pop_size:
        for parent in parents:
            child = copy(parent[0])
            for i in range(len(child.weight_layers)):
                weight_layer = child.weight_layers[i]
                bias_layer = child.bias_layers[i]
                mutate_nn_layer(weight_layer, growth_rate, mutation_strength)
                mutate_nn_layer(bias_layer, growth_rate, mutation_strength)
            population.append([child, inital_fitness_score])
    return population[:pop_size]

def pick_parents(population, n):
    # just get the top n candidates. in the future, make it slightly more random
    population.sort(reverse=True, key=lambda individual : individual[1])
    return population[:n] 