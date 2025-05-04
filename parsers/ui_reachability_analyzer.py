# parsers/ui_reachability_analyzer.py

import networkx as nx

def find_reachable_ui_nodes(G, entry_nodes):
    """
    Given a graph G and entry nodes, return all nodes reachable from those entries.
    """
    reachable = set()
    for entry in entry_nodes:
        if G.has_node(entry):
            reachable |= nx.descendants(G, entry)
            reachable.add(entry)
    return reachable

def find_dead_ui_nodes(G, entry_nodes):
    """
    Given a graph G and entry nodes, return nodes that are not reachable from those entries.
    """
    all_nodes = set(G.nodes())
    reachable = find_reachable_ui_nodes(G, entry_nodes)
    return all_nodes - reachable

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python ui_reachability_analyzer.py <gexf_file> <entry_node_index,...>")
        exit(1)

    gexf_path = sys.argv[1]
    entry_nodes = sys.argv[2].split(',')

    G = nx.read_gexf(gexf_path)
    reachable = find_reachable_ui_nodes(G, entry_nodes)
    dead = find_dead_ui_nodes(G, entry_nodes)

    print(f"Reachable UI nodes: {len(reachable)}")
    print(f"Dead UI nodes: {len(dead)}")
