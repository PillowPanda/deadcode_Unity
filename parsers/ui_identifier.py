import os
import yaml
import csv
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

# -----------------------------------
# Phase 1: Identify UI Components
# -----------------------------------

UI_COMPONENTS = ['Button', 'Toggle', 'Dropdown', 'Slider', 'Canvas', 'EventTrigger']

TRANSITION_KEYWORDS = ['LoadScene', 'SetActive', 'Play', 'Trigger']

def find_unity_files(folder):
    unity_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.prefab') or file.endswith('.unity'):
                full_path = os.path.join(root, file)
                print(f"[DEBUG] Found Unity file: {full_path}")
                unity_files.append(full_path)
    return unity_files

def parse_file_for_ui(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        data = f.read()

    raw_objects = data.split('--- !u!')
    ui_elements = []

    for obj in raw_objects:
        for comp in UI_COMPONENTS:
            if comp in obj:
                ui_elements.append(comp)

    return ui_elements

def analyze_dataset(dataset_folder, output_csv='ui_analysis.csv'):
    files = find_unity_files(dataset_folder)
    results = []

    for file in files:
        ui_elements = parse_file_for_ui(file)
        file_type = 'prefab' if file.endswith('.prefab') else 'unity'
        directory_level = len(os.path.relpath(file, dataset_folder).split(os.sep)) - 1

        if ui_elements:
            results.append({
                'file': file,
                'ui_element_count': len(ui_elements),
                'ui_element_types': list(set(ui_elements)),
                'file_type': file_type,
                'directory_level': directory_level
            })

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['file', 'ui_element_count', 'ui_element_types', 'file_type', 'directory_level']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Analysis complete! Found {len(results)} files with UI elements.")

# -----------------------------------
# Phase 2: Build Graph from UI Files
# -----------------------------------

def parse_ui_nodes_and_edges(file_path):
    nodes = []
    edges = []
    file_label = os.path.basename(file_path)

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    raw_objects = content.split('--- !u!')

    for obj in raw_objects:
        for comp in UI_COMPONENTS:
            if comp in obj:
                node_name = f"{file_label}::{comp}"
                nodes.append(node_name)

                for keyword in TRANSITION_KEYWORDS:
                    if keyword in obj:
                        edges.append((node_name, f"{keyword}_Target"))

    return nodes, edges

def build_ui_graph(file_list):
    G = nx.DiGraph()
    for file in file_list:
        nodes, edges = parse_ui_nodes_and_edges(file)
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
    return G

def color_by_reachability(G, entry_keyword="MainMenu"):
    entry_nodes = [n for n in G.nodes if entry_keyword in n]
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

def visualize_graph(G, output_path='outputs/ui_graph_colored.png'):
    plt.figure(figsize=(24, 14))
    pos = nx.spring_layout(G, k=0.45, iterations=50)

    node_colors = color_by_reachability(G)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color="gray",
            node_size=500, font_size=7, arrows=True)
    plt.title("UI Navigation Graph: Reachable vs Unreachable UI")
    plt.savefig(output_path)
    plt.show()
    print(f"\u2705 Colored graph saved to {output_path}")

# -----------------------------------
# Main Runner
# -----------------------------------

if __name__ == "__main__":
    dataset_folder = "datasets/open-project-1-main/"   # Adjust path as needed
    analyze_dataset(dataset_folder)  # This creates ui_analysis.csv

    df = pd.read_csv('ui_analysis.csv')
    file_list = df['file'].tolist()

    G = build_ui_graph(file_list)
    visualize_graph(G)

        # Save graph to GEXF
    gexf_output_path = 'outputs/ui_graph.gexf'
    nx.write_gexf(G, gexf_output_path)
    print(f"✅ GEXF file for Gephi saved: {gexf_output_path}")

    # (Optional) Save also to GraphML
    graphml_output_path = 'outputs/ui_graph.graphml'
    nx.write_graphml(G, graphml_output_path)
    print(f"✅ GraphML file also saved: {graphml_output_path}")
