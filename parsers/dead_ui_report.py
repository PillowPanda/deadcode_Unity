# parsers/dead_ui_report.py

import csv
from parsers.ui_reachability_analyzer import find_reachable_ui_nodes, find_dead_ui_nodes

def generate_dead_ui_report(gexf_path, output_csv_path):
    import networkx as nx

    # Load the graph
    G = nx.read_gexf(gexf_path)

    # Identify entry points based on naming heuristics
    entry_nodes = [n for n in G.nodes if 'Canvas' in n or 'MainMenu' in n or 'Persistent' in n]

    # Compute reachable and dead nodes
    reachable_nodes = find_reachable_ui_nodes(G, entry_nodes)
    dead_nodes = find_dead_ui_nodes(G, entry_nodes)

    # Write report
    with open(output_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['UI Element', 'Status'])

        for node in sorted(reachable_nodes):
            writer.writerow([node, 'reachable'])

        for node in sorted(dead_nodes):
            writer.writerow([node, 'dead'])

    print(f"✅ Dead UI report written to: {output_csv_path}")
