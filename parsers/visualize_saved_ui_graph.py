# visualize_ui_transitions.py

import os
import yaml
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

UI_COMPONENTS = ['Button', 'Toggle', 'Dropdown', 'Slider', 'Canvas', 'EventTrigger']

# -- Helper Functions --
def extract_gameobject_name(obj_text):
    for line in obj_text.splitlines():
        if line.strip().startswith('m_Name:'):
            return line.split(':', 1)[1].strip()
    return None

def extract_method_name(obj_text):
    for line in obj_text.splitlines():
        if 'm_MethodName:' in line:
            return line.split(':', 1)[1].strip().replace('"', '')
    return None

def extract_target_name(obj_text):
    for line in obj_text.splitlines():
        if 'm_Target:' in line:
            return line.split(':', 1)[1].strip().replace('"', '')
    return None

# -- Parsing Files --
def parse_ui_nodes_and_edges(file_path):
    nodes = []
    edges = []
    file_label = os.path.basename(file_path)

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    raw_objects = content.split('--- !u!')

    for obj in raw_objects:
        if any(comp in obj for comp in UI_COMPONENTS):
            gameobject_name = extract_gameobject_name(obj) or "Unnamed"
            full_node_name = f"{file_label}::{gameobject_name}"
            nodes.append(full_node_name)

            if 'Button' in obj and 'm_OnClick:' in obj:
                method_name = extract_method_name(obj)
                target_name = extract_target_name(obj) or "UnknownTarget"

                if method_name:
                    edges.append((full_node_name, f"{file_label}::{target_name}", {'method': method_name}))

    return nodes, edges

# -- Build Graph --
def build_ui_graph(file_list):
    G = nx.DiGraph()
    for file in file_list:
        nodes, edges = parse_ui_nodes_and_edges(file)
        G.add_nodes_from(nodes)
        for edge in edges:
            G.add_edge(edge[0], edge[1], method=edge[2]['method'])
    return G

# -- Coloring Nodes --
def color_by_reachability(G, entry_keyword="MainMenu"):
    entry_nodes = [n for n in G.nodes if entry_keyword.lower() in n.lower()]
    reachable = set()

    for start in entry_nodes:
        reachable |= nx.descendants(G, start)
        reachable.add(start)

    node_colors = []
    for node in G.nodes:
        if node in reachable:
            node_colors.append("lightgreen")
        else:
            node_colors.append("lightcoral")
    return node_colors

# -- Visualization --
def visualize_graph(G, output_path='outputs/ui_transition_graph.png'):
    plt.figure(figsize=(24, 14))
    pos = nx.spring_layout(G, k=0.45, iterations=60)

    node_colors = color_by_reachability(G)
    edge_labels = {(u, v): d['method'] for u, v, d in G.edges(data=True)}

    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color="gray",
            node_size=500, font_size=7, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)

    plt.title("UI Interaction Graph with Methods")
    plt.savefig(output_path)
    plt.show()
    print(f"\u2705 Colored graph saved to {output_path}")

# -- Main --
if __name__ == "__main__":
    df = pd.read_csv('ui_analysis.csv')
    file_list = df['file'].tolist()

    G = build_ui_graph(file_list)
    visualize_graph(G)

    # Optional: save the graph for Gephi use
    nx.write_gexf(G, 'outputs/ui_transition_graph.gexf')
    nx.write_graphml(G, 'outputs/ui_transition_graph.graphml')
    print("\u2705 GEXF and GraphML saved for Gephi.")
