def extract_edges(file_path):
    edges = []

    with open(file_path, 'r') as file:
        for line in file:

            # Skip empty lines and lines starting with '//'
            if line.startswith('//') or line.strip() == "":
                continue

            line_content = line.split('//')[0].strip()

            if line_content:
                node1, node2 = map(int, line_content.split())
                edges.append((node1, node2))

    return edges


def create_adjacency_list(edges):
    adjacency_list = {}

    for node1, node2 in edges:
        if node1 not in adjacency_list:
            adjacency_list[node1] = []
        if node2 not in adjacency_list:
            adjacency_list[node2] = []

        adjacency_list[node1].append(node2)
        adjacency_list[node2].append(node1)

    return adjacency_list


graph = create_adjacency_list(extract_edges('hw3_cost239.txt'))
print(graph)
