import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random

def main():
    # Streamlit UI elements
    # insert header brand with logo and link to website
    st.components.v1.html(
        """
        <style>
            .header-brand {
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .header-divider {
                height: 1px;
                margin-top: 5px;
                background-color: rgba(49, 51, 63, 0.2);
            }
        </style>

        <div class="header-brand">
            <strong>Project 300x250</strong>
            <a href="https://www.linkedin.com/in/peter-brendan" target="_blank">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="#0a66c2"
                    class="mercado-match"
                    width="32"
                    height="32"
                    focusable="false"
                >
                    <path
                        d="M20.5 2h-17A1.5 1.5 0 002 3.5v17A1.5 1.5 0 003.5 22h17a1.5 1.5 0 001.5-1.5v-17A1.5 1.5 0 0020.5 2zM8 19H5v-9h3zM6.5 8.25A1.75 1.75 0 118.3 6.5a1.78 1.78 0 01-1.8 1.75zM19 19h-3v-4.74c0-1.42-.6-1.93-1.38-1.93A1.74 1.74 0 0013 14.19a.66.66 0 000 .14V19h-3v-9h2.9v1.3a3.11 3.11 0 012.7-1.4c1.55 0 3.36.86 3.36 3.66z"
                    ></path>
                </svg>
            </a>
        </div>
        <div class="header-divider" />
        """,
        height=80,
    )
    st.title('Daily Floor Seasonality Model')
    st.info("**Calculate and apply the optimal floor adjustment for each day using our model. Select a day and input your initial floor value to get started.**")

    dsp_bid = 4.0

    def create_publisher_ssp_dsp_graph_conversion(num_ssps, dsp_bid):
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

    def create_publisher_ssp_dsp_graph_cheapest(num_ssps, dsp_bid):
        # Create a directed graph
        graph = nx.DiGraph()

        # Add nodes
        graph.add_node("Publisher", label="Publisher")

        # Add SSP nodes and edges with individual adjusted bids
        ssp_nodes = [f"SSP{i}" for i in range(1, num_ssps + 1)]
        for ssp_node in ssp_nodes:
            fee_percentage = random.uniform(0.025, 0.25)
            adjusted_bid = dsp_bid - (dsp_bid * fee_percentage)
            graph.add_node(ssp_node, label="SSP")
            graph.add_edge(ssp_node, "Publisher", label=f"Bid: ${adjusted_bid:.2f}")

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

    option = st.radio("Choose Path Type", ["Cheapest Path", "Conversion Path"])

    if option == "Conversion Path":
        num_ssps = st.sidebar.slider("Number of SSPs", 1, 10, 6)  # You can change this value to adjust the number of SSPs
        dsp_bid = st.sidebar.number_input("DSP Bid", min_value=1.0, value=5.0, step=0.1)  # Input for DSP bid with min value of 1.0
        graph = create_publisher_ssp_dsp_graph_conversion(num_ssps, dsp_bid)
        visualize_graph(graph)
    elif option == "Cheapest Path":
        num_ssps = st.sidebar.slider("Number of SSPs", 1, 10, 6)
        dsp_bid = st.sidebar.number_input("DSP Bid", min_value=1.0, value=5.0, step=0.1)
        graph = create_publisher_ssp_dsp_graph_cheapest(num_ssps, dsp_bid)
        visualize_graph(graph)

if __name__ == "__main__":
    main()
