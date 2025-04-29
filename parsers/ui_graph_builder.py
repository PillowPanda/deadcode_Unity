import os
import yaml
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def parse_ui_elements(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = f.read()
    
    raw_objects = data.split('--- !u!')
    ui_objects = []

    for obj in raw_objects:
        if 'Button' in obj or 'Dropdown' in obj or 'Toggle' in obj or 'Slider' in obj:
            lines = obj.splitlines()
            for line in lines:
                if 'm_Name:' in line:
                    name = line.split(':',1)[1].strip()
                    if name:
                        ui_objects.append(name)
    return ui_objects

def build_ui_graph(file_list):
    G = nx.DiGraph()
    
    for filepath in file_list:
        filename = os.path.basename(filepath)
        ui_objects = parse_ui_elements(filepath)
        print(f"[DEBUG] {filename}: {len(ui_objects)} UI Objects")

        for obj in ui_objects:
            G.add_node(obj, file=filename)
            # Example linking: (This can be improved later)
            if 'Button' in obj or 'button' in obj.lower():
                G.add_edge(obj, filename)  # Button -> file
    return G

def visualize_graph(G, output_path='outputs/ui_graph_colored_v2.png'):
    plt.figure(figsize=(20, 20))
    pos = nx.spring_layout(G, seed=42)

    reachable_nodes = set()
    for node in G.nodes:
        if G.in_degree(node) > 0 or G.out_degree(node) > 0:
            reachable_nodes.add(node)

    colors = []
    for node in G.nodes:
        if node in reachable_nodes:
            colors.append('lightblue')
        else:
            colors.append('lightcoral')

    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=100)
    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='->')
    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.axis('off')
    plt.title('UI Graph (Reachable vs Unreachable Nodes)', fontsize=16)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"\u2705 Colored graph saved to {output_path}")

def export_graph_gephi(G, output_path='outputs/ui_graph_v2.gexf'):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    nx.write_gexf(G, output_path)
    print(f"\u2705 GEXF file for Gephi saved: {output_path}")

if __name__ == "__main__":
    # Corrected: Read only UI files from analysis csv
    df = pd.read_csv('ui_analysis.csv')
    df_ui = df[df['ui_element_count'] > 0]
    file_list = df_ui['file'].tolist()

    G = build_ui_graph(file_list)
    visualize_graph(G)
    export_graph_gephi(G)
