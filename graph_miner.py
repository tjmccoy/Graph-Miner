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


graph = create_adjacency_list(extract_edges('hw3_cost239.txt'))
print(graph)
