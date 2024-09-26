import igraph as ig
import matplotlib.pyplot as plt

# Define the edges based on the provided information
edges = [
    (0, 1), (0, 2), (2, 8), (8, 18), (17, 18), (16, 17), (15, 16), (7, 15), (5, 7), (5, 6),
    (6, 11), (10, 11), (9, 10), (9, 12), (12, 14), (13, 14), (1, 13), (1, 3), (3, 4), (2, 4),
    (1, 2), (1, 5), (2, 5), (1, 11), (5, 11), (2, 7), (7, 8), (8, 13), (8, 15), (8, 17),
    (11, 15), (11, 13), (13, 15), (13, 16), (1, 9), (10, 12), (12, 13)
]

# Create a graph using the defined edges
g = ig.Graph(edges=edges)

# Label the vertices from 0 to 18
g.vs["label"] = list(range(g.vcount()))

# Visualize the graph
layout = g.layout("fr")
visual_style = {
    "vertex_size": 20,
    "vertex_label": g.vs["label"],
    "layout": layout,
    "bbox": (400, 400),
    "margin": 40
}

# Save the graph to an image file
ig.plot(g, **visual_style, target='graph_output.png')

# Display the image using matplotlib
img = plt.imread('graph_output.png')
plt.imshow(img)
plt.axis('off')  # Hide the axes
plt.show()
