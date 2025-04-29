# 🛠 Goal: Build a **Better Unity UI Dead Code Identifier and Navigator**
# Phase 1: Design a more accurate static analyzer and lightweight navigation graph builder

import os
import re
import networkx as nx
import matplotlib.pyplot as plt

# --- Settings ---
UI_COMPONENTS = ['Button', 'Toggle', 'Dropdown', 'Slider', 'Canvas', 'EventTrigger']
INTERACTION_EVENTS = ['onClick', 'onValueChanged', 'onSelect', 'onDeselect']
METHOD_CALL_PATTERN = re.compile(r"m_MethodName: (\w+)")

# --- Core Functions ---

def find_unity_files(root_folder):
    unity_files = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.prefab') or file.endswith('.unity'):
                unity_files.append(os.path.join(root, file))
    return unity_files


def parse_ui_connections(file_path):
    nodes = []
    edges = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    raw_objects = content.split('--- !u!')

    for obj in raw_objects:
        component_found = None
        for comp in UI_COMPONENTS:
            if comp in obj:
                match_name = re.search(r'm_Name: (.+)', obj)
                if match_name:
                    component_name = match_name.group(1).strip()
                    full_name = f"{os.path.basename(file_path)}::{component_name}"
                    nodes.append(full_name)
                    component_found = full_name
                    break  # Only one UI type per object

        if component_found:
            # Try to find event-based method connections
            for interaction in INTERACTION_EVENTS:
                if interaction in obj:
                    method_matches = METHOD_CALL_PATTERN.findall(obj)
                    for method in method_matches:
                        edges.append((component_found, method))

    return nodes, edges


def build_navigation_graph(unity_files):
    G = nx.DiGraph()
    for file in unity_files:
        nodes, edges = parse_ui_connections(file)
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
    return G


def visualize_graph(G, save_path='outputs/ui_navigation_graph.png'):
    plt.figure(figsize=(20, 12))
    pos = nx.spring_layout(G, k=0.6, iterations=60)
    nx.draw(G, pos, with_labels=True, node_size=500, font_size=7, arrows=True)
    plt.title("Static UI Navigation Graph")
    plt.savefig(save_path)
    plt.show()
    print(f"✅ Graph saved at {save_path}")


# --- Main Pipeline ---

def main(root_folder):
    unity_files = find_unity_files(root_folder)
    G = build_navigation_graph(unity_files)

    # Save graph
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    nx.write_graphml(G, 'outputs/ui_navigation.graphml')
    nx.write_gexf(G, 'outputs/ui_navigation.gexf')

    visualize_graph(G)


if __name__ == "__main__":
    # Change path if needed
    project_path = "datasets/open-project-1-main/"
    main(project_path)
