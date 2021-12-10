import random
import matplotlib.pyplot as plt


def fitness(ant_path, items, number_bins):
    bin_totals = bin_values(ant_path, items, number_bins)
    return max(bin_totals) - min(bin_totals)


def bin_values(ant_path, items, number_bins):
    bins = [0 for _ in range(number_bins)]
    index2 = 0
    for choice in ant_path:
        bins[choice] += items[index2]
        index2 += 1
    return bins


def single_ant_solution(items, pheromones, number_bins):
    path_list = []
    for item in range(len(items)):
        possible_bins = calculate_next_node(pheromones, item)
        next_node = random.choices([index for index in range(number_bins)], possible_bins)[0]
        path_list.append(next_node)
    return path_list


def calculate_next_node(pheromones: list, item: int):
    new_value_store = pheromones[item]
    total_list = []
    total_pheromones = 0
    for pheromone in new_value_store:
        total_pheromones += pheromone
    for pheromone in new_value_store:
        total_list.append(pheromone / total_pheromones)
    return total_list


def ant_solutions(items, pheromones, number_ants, number_bins):
    ant_paths = []
    fitness_values = []
    for i in range(number_ants):
        ant_paths.append(single_ant_solution(items, pheromones, number_bins))
        fitness_values.append(fitness(ant_paths[i], items, number_bins))
    return ant_paths, fitness_values


def update_pheromones(ant_paths, fitness_values, evaporation_rate, number_ants, pheromones):
    for index in range(number_ants):
        ant_path = ant_paths[index]
        fitness_value = fitness_values[index]
        for pheromone_index, pheromone in enumerate(pheromones):
            pheromone[ant_path[pheromone_index]] += (100 / fitness_value)
    for bin_p in pheromones:
        for value in bin_p:
            value *= evaporation_rate
    return pheromones


def find_best_fitness(fitness_values):
    return min(fitness_values)


def draw_good_graph(f, iterations):
    new_values = []
    minimum = f[0]
    for val in f:
        if val < minimum:
            minimum = val
        new_values.append(minimum)
    plt.plot([index for index in range(iterations)], new_values)
    plt.show()


def draw_graph(f, iterations):
    plt.plot([index for index in range(iterations)], f)
    plt.show()


def ant_colony_optimisation(number_ants, evaporation_rate, number_bins, items):
    number_items = len(items)
    pheromones = [[random.random() for _ in range(number_bins)] for _ in range(number_items)]
    f = []
    s = []
    iterations = 10000 // number_ants
    fitness_values = []
    for i in range(iterations):
        ant_paths, fitness_values = ant_solutions(items, pheromones, number_ants, number_bins)
        update_pheromones(ant_paths, fitness_values, evaporation_rate, number_ants, pheromones)
        f.append(find_best_fitness(fitness_values))
        s.append(sum(fitness_values) / len(fitness_values))
    print('Average:', sum(fitness_values) / len(fitness_values))
    print('Best:', find_best_fitness(fitness_values))
    plt.plot([index for index in range(iterations)], f)
    plt.show()
    plt.plot([index for index in range(iterations)], s)
    plt.show()
    draw_good_graph(f, iterations)
    return find_best_fitness(fitness_values)


if __name__ == "__main__":
    ant_colony_optimisation(100, 0.9, 50, [(index + 1) ^ 2 for index in range(500)])
