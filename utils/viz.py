import networkx as nx
import matplotlib.pyplot as plt


def on_key_press(event):
    if event.key == 'r':
        plt.gcf().axes[0].autoscale()
        plt.gcf().canvas.draw()


def visualize_genome_adjacency_graph(s1, s2, grey_edges, black_edges, plot_title):
    if not s1 and not s2 and not grey_edges and not black_edges:
        plt.figure(figsize=(6, 4))
        plt.title(plot_title)
        plt.text(0.5, 0.5, "Empty Graph", ha='center', va='center')
        plt.axis('off')
        plt.show()
        return
    # Create a new graph
    G = nx.Graph()

    # Add vertices
    G.add_nodes_from(s1 + s2)

    # Add edges
    G.add_edges_from(grey_edges)
    G.add_edges_from(black_edges)

    # Create a custom layout
    pos = {}
    y_offset = 0.5  # Increased offset to separate the two genome lines visually
    x_scale = max(len(s1), len(s2)) / 10  # Scale factor for x-axis

    # Position vertices of genome 1
    for i, v in enumerate(s1):
        pos[v] = (i * x_scale, y_offset)

    # Position vertices of genome 2
    for i, v in enumerate(s2):
        pos[v] = (i * x_scale, -y_offset)

    # Calculate figure size based on number of vertices
    fig_width = max(12, len(s1) / 2)
    fig_height = max(6, fig_width / 2)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, nodelist=s1, node_color='lightblue', node_size=300, ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=s2, node_color='lightgreen', node_size=300, ax=ax)

    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)

    # Draw grey edges
    nx.draw_networkx_edges(G, pos, edgelist=grey_edges, edge_color='grey', width=1, ax=ax)

    # Draw black edges
    nx.draw_networkx_edges(G, pos, edgelist=black_edges, edge_color='black', width=1, ax=ax)

    ax.set_title(plot_title)
    ax.axis('off')

    # Set axis limits with some padding
    x_values, y_values = zip(*pos.values())
    x_padding = (max(x_values) - min(x_values)) * 0.1
    y_padding = (max(y_values) - min(y_values)) * 0.1
    ax.set_xlim(min(x_values) - x_padding, max(x_values) + x_padding)
    ax.set_ylim(min(y_values) - y_padding, max(y_values) + y_padding)

    plt.tight_layout()

    # Enable zooming and panning
    plt.gcf().canvas.mpl_connect('key_press_event', on_key_press)

    plt.show()
