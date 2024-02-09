import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random

def create_publisher_ssp_dsp_graph(num_ssps, dsp_bid):
    # Create a directed graph
    graph = nx.DiGraph()

    # Add nodes
    graph.add_node("Publisher", label="Publisher")

    # Add SSP nodes and edges with individual adjusted bids
    ssp_nodes = [f"SSP{i}" for i in range(1, num_ssps + 1)]
    positive_number = random.randint(1, num_ssps)  # Choose a specific SSP node to have a positive fee percentage
    for ssp_node in ssp_nodes:
        fee_percentage = random.randint(1, 9) if ssp_node == f"SSP{positive_number}" else 0

        adjusted_bid = dsp_bid * fee_percentage
        graph.add_node(ssp_node, label="SSP")
        graph.add_edge(ssp_node, "Publisher", label=f"Sale: ${adjusted_bid:.2f}")

        # Connect SSPs to the DSP with the original bid
        graph.add_edge("DSP", ssp_node, label=f"Bid: ${dsp_bid}")

    return graph

def visualize_graph(graph):
    # Manually specify positions for publisher, SSPs, and DSP
    pos = {
        "Publisher": (-1, 0),
    }
    for i, ssp_node in enumerate(graph.nodes):
        if ssp_node != "Publisher":
            pos[ssp_node] = (0, i - (len(graph.nodes)-1)/2)
    pos["DSP"] = (1, 0)

    edge_labels = nx.get_edge_attributes(graph, 'label')
    
    # Find the path with the highest bid from SSP to Publisher
    paths = nx.all_simple_paths(graph, source="DSP", target="Publisher")
    highest_bid_path = max(paths, key=lambda path: sum(float(graph[path[i]][path[i + 1]]['label'].split(": $")[1]) for i in range(len(path) - 1)))

    # Plotting the graph
    fig, _ = plt.subplots(figsize=(8, 6))

    # Set the color and thickness of the blue line
    edge_colors = ['black' for _ in graph.edges()]
    edge_widths = [2 if (u, v) in zip(highest_bid_path, highest_bid_path[1:]) else 1 for u, v in graph.edges()]
    edge_colors = [(0, 129/255, 251/255) if (u, v) in zip(highest_bid_path, highest_bid_path[1:]) else (0, 0, 0) for u, v in graph.edges()]

    # Draw edges with the highest bid path in blue, others in black
    nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(), edge_color=edge_colors, width=edge_widths)

    # Draw the nodes
    nx.draw_networkx_nodes(graph, pos, node_size=1000, node_color='lightblue')

    # Draw node labels
    nx.draw_networkx_labels(graph, pos)

    # Draw edge labels
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    plt.axis("off")
    st.pyplot(fig)

if __name__ == "__main__":
    num_ssps = st.sidebar.slider("Number of SSPs", 1, 10, 6)  # You can change this value to adjust the number of SSPs
    dsp_bid = st.sidebar.number_input("DSP Bid", min_value=1.0, value=4.0, step=0.1)  # Input for DSP bid with min value of 1.0
    graph = create_publisher_ssp_dsp_graph(num_ssps, dsp_bid)
    visualize_graph(graph)
