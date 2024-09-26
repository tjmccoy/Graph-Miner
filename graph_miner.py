import random


def extract_edges(file_path):
    edges = []

    # open the file containing the graph's edges
    with open(file_path, 'r') as file:
        for line in file:

            # Skip empty lines and comments
            if line.startswith('//') or line.strip() == "":
                continue

            # remove inline comments and trailing whitespace from line
            line_content = line.split('//')[0].strip()

            # if there is content after stripping,
            if line_content:
                node1, node2 = line_content.split()     # split the nodes into two separate variables
                node1, node2 = int(node1), int(node2)   # cast as integers from strings
                edges.append((node1, node2))            # append as a tuple to edges

    return edges


def create_adjacency_list(edges):
    adjacency_list = {}

    for node1, node2 in edges:  # iterate through each edge

        # if node1 isn't in the adjacency list, add it with an empty list
        if node1 not in adjacency_list:
            adjacency_list[node1] = []
        # if node2 isn't in the adjacency list, add it with an empty list
        if node2 not in adjacency_list:
            adjacency_list[node2] = []

        # add node2 to node1's adjacency list and vice versa since it is an undirected graph
        adjacency_list[node1].append(node2)
        adjacency_list[node2].append(node1)

    return adjacency_list


def is_connected(subgraph, target_nodes):
    # BFS to check connectivity of M nodes
    target_nodes = set(target_nodes)  # Ensure target_nodes is a set

    if not target_nodes:
        return True  # an empty set is connected -> i.e., vacuously true

    start_node = target_nodes.pop()  # Pick an arbitrary node from target_nodes
    visited = set()
    stack = [start_node]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for neighbor in subgraph.get(node, []):
                if neighbor not in visited:
                    stack.append(neighbor)

    return target_nodes.issubset(visited)


def fitness(individual, edges, target_nodes):
    # create subgraph from individual
    subgraph = {}
    for i, included in enumerate(individual):
        if included:
            node1, node2 = edges[i]
            if node1 not in subgraph:
                subgraph[node1] = []
            if node2 not in subgraph:
                subgraph[node2] = []
            subgraph[node1].append(node2)
            subgraph[node2].append(node1)

    # check if all nodes in target_nodes are connected in the subgraph
    if not is_connected(subgraph, target_nodes):
        return 1000  # high penalty for not connecting all nodes in target_nodes

    # fitness is the number of edges included (to minimize)
    return sum(individual)


def create_individual(edge_count):
    return [random.choice([0, 1]) for _ in range(edge_count)]


def selection(population, fitness_scores, n=5):
    selected = []

    # choose n random individuals from population with their fitness scores
    for _ in range(n):
        i = random.randint(0, len(population) - 1)
        selected.append((population[i], fitness_scores[i]))

    # get the individual with the minimum fitness from the selected individuals
    best_individual = min(selected, key=lambda x: x[1])

    # extract the individual and return it
    parent = best_individual[0]
    return parent


def crossover(parent1, parent2):
    # choose a random point from idx 1 to end of individual string, and crossover genes
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    # return the two crossed children
    return child1, child2


def mutate(individual, mutation_rate=0.01):
    for i in range(len(individual)):
        if random.random() < mutation_rate:  # randomly generates a number in the interval of [0,1]
            individual[i] = 1 - individual[i]   # flip bit (1 - 0 = 1, 1 - 1 = 0)


def genetic_algorithm(edges, target_nodes, population_size=100, generations=100, mutation_rate=0.01):
    # initialize edge count to length of edges read from txt file
    edge_count = len(edges)

    # initialize population
    population = [create_individual(edge_count) for _ in range(population_size)]

    # evaluate initial population
    pop_fitness_scores = [fitness(individual, edges, target_nodes) for individual in population]

    # evolution loop
    for generation in range(generations):
        new_population = []

        for _ in range(population_size // 2):
            parent1 = selection(population, pop_fitness_scores)
            parent2 = selection(population, pop_fitness_scores)

            # crossover
            child1, child2 = crossover(parent1, parent2)

            # mutate
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)

            # add to new population
            new_population.extend([child1, child2])

        # replace old population with new population
        population = new_population

        # calculate fitness scores for each individual in the new population
        pop_fitness_scores = [fitness(individual, edges, target_nodes) for individual in population]

        # for testing purposes:
        best_fitness = min(pop_fitness_scores)
        best_idx = pop_fitness_scores.index(min(pop_fitness_scores))
        print(f"Generation {generation}: Best fitness = {best_fitness} String: {population[best_idx]}")


    # return best solution
    best_idx = pop_fitness_scores.index(min(pop_fitness_scores))
    return population[best_idx]

def main():
    # Run the genetic algorithm
    edges = extract_edges('hw3_cost239.txt')
    graph = create_adjacency_list(edges)
    print(graph)

    target_nodes = {1, 3, 5, 7, 9, 11, 13, 15, 17}
    best_solution = genetic_algorithm(edges, target_nodes)

    # Print the best subgraph solution
    print("Best subgraph found:")
    for i, included in enumerate(best_solution):
        if included:
            print(edges[i])


if __name__ == "__main__":
    main()
