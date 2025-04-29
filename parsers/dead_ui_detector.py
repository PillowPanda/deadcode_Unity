# parsers/dead_ui_detector.py

import networkx as nx
import matplotlib.pyplot as plt
import os

def load_ui_graph(gexf_path='outputs/ui_navigation_graph.gexf'):
    if not os.path.exists(gexf_path):
        raise FileNotFoundError(f"GEXF file not found: {gexf_path}")
    G = nx.read_gexf(gexf_path)
    return G

def find_entry_nodes(G, keywords=['MainMenu', 'Canvas', 'Home']):
    entry_nodes = []
    for node in G.nodes:
        for keyword in keywords:
            if keyword.lower() in node.lower():
                entry_nodes.append(node)
    if not entry_nodes:
        # fallback: pick nodes with no incoming edges
        entry_nodes = [n for n in G.nodes if G.in_degree(n) == 0]
    return entry_nodes

def detect_dead_ui(G, entry_nodes):
    reachable = set()
    for entry in entry_nodes:
        reachable.update(nx.descendants(G, entry))
        reachable.add(entry)
    all_nodes = set(G.nodes)
    dead_nodes = all_nodes - reachable
    return reachable, dead_nodes

def draw_ui_graph(G, reachable, dead_nodes, output_path='outputs/dead_ui_graph.png'):
    plt.figure(figsize=(24, 16))
    pos = nx.spring_layout(G, k=0.5, iterations=60)

    node_colors = []
    for node in G.nodes:
        if node in reachable:
            node_colors.append("lightgreen")
        else:
            node_colors.append("lightcoral")

    nx.draw(G, pos,
            node_color=node_colors,
            with_labels=True,
            font_size=6,
            node_size=500,
            edge_color="gray",
            arrows=True)

    plt.title("Dead UI Detection: Green = Reachable, Red = Dead")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.show()
    print(f"✅ Dead UI Graph saved to {output_path}")

def interactive_entry_selection(G):
    print("\n🔎 Available Entry Node Options (first 20 shown):")
    sample_nodes = list(G.nodes)[:20]
    for idx, node in enumerate(sample_nodes):
        print(f"{idx}: {node}")

    custom_keyword = input("\nEnter a keyword (or leave blank for default MainMenu/Canvas/Home): ").strip()
    if custom_keyword:
        entry_nodes = find_entry_nodes(G, [custom_keyword])
    else:
        entry_nodes = find_entry_nodes(G)
    
    if not entry_nodes:
        print("⚠️ No matching entry nodes found. Using fallback (nodes with no incoming edges).")
        entry_nodes = [n for n in G.nodes if G.in_degree(n) == 0]

    print(f"✅ Entry Nodes selected: {entry_nodes}")
    return entry_nodes

if __name__ == "__main__":
    gexf_path = 'outputs/ui_navigation_graph.gexf'
    G = load_ui_graph(gexf_path)

    entry_nodes = interactive_entry_selection(G)
    reachable, dead_nodes = detect_dead_ui(G, entry_nodes)

    print(f"[INFO] Total Nodes: {len(G.nodes)}")
    print(f"[INFO] Reachable Nodes: {len(reachable)}")
    print(f"[INFO] Dead Nodes: {len(dead_nodes)}")

    draw_ui_graph(G, reachable, dead_nodes)
