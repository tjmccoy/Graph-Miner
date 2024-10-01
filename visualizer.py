import igraph as ig
import matplotlib.pyplot as plt
from graph_miner import main

# Get the best solution from the genetic algorithm
best_edges = main()  # Execute the genetic algorithm and return the best edges

# Define all edges ensuring they only connect nodes 0 to 17
all_edges = [
    (0, 1), (0, 2), (2, 8), (8, 17), (16, 17), (15, 16), (7, 15), (5, 7), (5, 6),
    (6, 11), (10, 11), (9, 10), (9, 12), (12, 14), (13, 14), (1, 13), (1, 3), (3, 4), (2, 4),
    (1, 2), (1, 5), (2, 5), (1, 11), (5, 11), (2, 7), (7, 8), (8, 13), (8, 15), (8, 16),
    (11, 15), (11, 13), (13, 15), (13, 16), (1, 9), (10, 12), (12, 13)
]

# Create a graph using only the valid edges
g = ig.Graph(edges=all_edges)

# Label the vertices from 0 to 17
g.vs["label"] = list(range(g.vcount()))  # Labels from 0 to 17

# Visualize the graph
visual_style = {
    "vertex_size": 20,
    "vertex_label": g.vs["label"],
    "layout": g.layout("fr"),
    "bbox": (400, 400),
    "margin": 40
}

# Highlight relevant nodes and edges
highlighted_edges = [edge for edge in best_edges]
highlighted_nodes = set()

for edge in highlighted_edges:
    highlighted_nodes.update(edge)

# Prepare the colors for the edges and vertices
g.es["color"] = "black"  # Default color for all edges
g.vs["color"] = "lightblue"  # Default color for all vertices

# Highlight the edges and vertices in the best solution
for edge in highlighted_edges:
    g.es[g.get_eid(edge[0], edge[1])]["color"] = "red"  # Highlight edges
for node in highlighted_nodes:
    g.vs[node]["color"] = "yellow"  # Highlight nodes

# Save the graph to an image file
ig.plot(g, **visual_style, target='best_solution_graph.png')

# Display the image using matplotlib
img = plt.imread('best_solution_graph.png')
plt.imshow(img)
plt.axis('off')  # Hide the axes
plt.show()
