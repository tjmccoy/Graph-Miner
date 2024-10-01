import random


def extract_edges(file_path):
    """
    Extracts edges from a graph file
    :param file_path: The path to the file containing the graph's edges. Each line of the file represents an edge,
                      with two space-separated integers representing the nodes that the edge connects
    :return: A list of tuples where each tuple represents an edge in the form (node1, node2)
    """
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
    """
    Creates an adjacency list of a graph from a list of edges
    :param edges: A list of tuples representing edges in the form (node1, node2)
    :return: A dictionary representing the adjacency list of the graph, where each key is a node and the value
             is a list of nodes that are neighboring it
    """
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
    """
    Determines if all target nodes are connected within a given subgraph
    :param subgraph: A dict representing the adjacency list of the subgraph
    :param target_nodes: A set of nodes to be used for checking connectivity within the subgraph
    :return: True if all target nodes are connected or False otherwise
    """
    # BFS to check connectivity of target_nodes within subgraph
    target_nodes = set(target_nodes)  # Ensure target_nodes is a set

    if not target_nodes:
        return True  # an empty set is connected -> i.e., vacuously true

    start_node = target_nodes.pop()  # Pick a node from target_nodes
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
    """
    Calculates the fitness of an individual based on connectivity and the number of edges used
    :param individual: A bit string representing the inclusion or exclusion of edges in the subgraph
    :param edges: A list of tuples representing edges in the form (node1, node2)
    :param target_nodes: The set of nodes that must be connected in the subgraph
    :return: The fitness score of the individual, which is the sum of included edges. Higher penalties (1000) are given
             if target nodes are not connected
    """
    # Initialize an empty dictionary to represent the subgraph that will be created
    # based on the edges selected by the individual's genome.
    subgraph = {}

    # loop over each bit in every individual, where 1 = included in subgraph and 0 = not included in subgraph
    for i, included in enumerate(individual):
        if included:    # if the edge is included,
            node1, node2 = edges[i]  # get the two nodes connected by this edge

            if node1 not in subgraph:   # if node1 is not already in the subgraph, initialize it with an empty list
                subgraph[node1] = []
            if node2 not in subgraph:   # if node2 is not already in the subgraph, initialize it with an empty adj. list
                subgraph[node2] = []

            subgraph[node1].append(node2)   # add node2 to the adjacency list of node1
            subgraph[node2].append(node1)   # add node2 to the adjacency list of node2
            # we add both since this is an undirected graph

    # check if all nodes in target_nodes are connected in the subgraph
    if not is_connected(subgraph, target_nodes):
        return 1000  # high penalty for not connecting all nodes in target_nodes

    # fitness is the number of edges included (to minimize), if all target_nodes are connected within the subgraph
    return sum(individual)


def create_individual(edge_count):
    """
    Creates a random individual for the population
    :param edge_count: The total number of edges in the graph
    :return: A list of binary values, where 1 means an edge is included in the individual's subgraph,
             and 0 means it is excluded
    """
    # randomly populates a bit string of length edge_count, representing included and excluded edges
    return [random.choice([0, 1]) for _ in range(edge_count)]


def selection(population, fitness_scores, n=5):
    """
    This function chooses n random individuals from the population and returns the best fit one.
    This is used to select parents to carry on their genes within the genetic algorithm.
    We used Tournament Selection in order to implement this function, you can read more about it
    here: https://en.wikipedia.org/wiki/Tournament_selection
    :param population: a list of the individuals that exist within the population
    :param fitness_scores: a list of the fitness scores of the individuals within the population
    :param n: the number of individuals to randomly choose from the population
    :return: parent, the best individual from the n randomly selected
    """
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
    """
    Performs crossover between two parents to produce two children at a randomly generated slice index
    :param parent1: The first parent individual (bit list)
    :param parent2: The second parent individual (bit list)
    :return: Two children (bit lists) created by crossing over genes from the parents.
    """
    # choose a random point in the individual string and crossover genes
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    # return the two crossed children
    return child1, child2


def mutate(individual, mutation_rate=0.01):
    """
    Iterates over the individual (bit list) and with each bit, there is a 1% chance of the bit flipping.
    :param individual: a bit list representation of edges included/excluded
    :param mutation_rate: the probability of a mutation occurring
    :return:
    """
    # iterate through the given individual and let a mutation occur, if the 1% chance occurs
    for i in range(len(individual)):
        if random.random() < mutation_rate:  # randomly generates a number in the interval of [0,1]
            individual[i] = 1 - individual[i]   # flip bit (1 - 0 = 1, 1 - 1 = 0)


def genetic_algorithm(edges, target_nodes, population_size=100, generations=100, mutation_rate=0.01):
    """
    Runs a genetic algorithm to find a subgraph that connects all target nodes with the fewest edges

    :param edges: A list of tuples representing the edges of the graph, where each tuple is in the form (node1, node2)
    :param target_nodes: A list or set of nodes that must be connected in the final subgraph
    :param population_size: The number of individuals in the population (default = 100)
    :param generations: The number of generations the algorithm will run (default = 100)
    :param mutation_rate: The probability of mutating each bit in an individual's genome (default is 0.01)
    :return: The individual (a bit list) representing the best subgraph found by the genetic algorithm. A '1' in the
                list means the corresponding edge is included in the subgraph, and '0' means it is excluded
    """
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
        print(f"Generation {generation}: Best fitness = {best_fitness}")

    # return best solution
    best_idx = pop_fitness_scores.index(min(pop_fitness_scores))
    return population[best_idx]


def main():
    # run the genetic algorithm
    edges = extract_edges('hw3_cost239.txt')
    graph = create_adjacency_list(edges)
    print(graph)

    target_nodes = {1, 3, 5, 7, 9, 11, 13, 15, 17}
    best_solution = genetic_algorithm(edges, target_nodes)

    # print the best subgraph solution
    print("Best subgraph found:")
    for i, included in enumerate(best_solution):
        if included:
            print(edges[i])

    # print the best subgraph solution
    best_edges = []
    for i, included in enumerate(best_solution):
        if included:
            best_edges.append(edges[i])  # collect the edges of the best solution

    return best_edges  # return the best edges for visualization


if __name__ == "__main__":
    main()
