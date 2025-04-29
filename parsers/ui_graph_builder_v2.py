import networkx as nx
import matplotlib.pyplot as plt
from scene_parser_v4 import parse_all_prefabs

class UIGraphBuilder:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_ui_objects(self, ui_objects):
        for obj in ui_objects:
            from_node = obj.name
            if not obj.targets:
                self.graph.add_node(from_node, type='Button')
            else:
                for target in obj.targets:
                    self.graph.add_node(from_node, type='Button')
                    self.graph.add_node(target, type='Method')
                    self.graph.add_edge(from_node, target)

    def visualize_graph(self, output_path="outputs/ui_graph_v2.png"):
        plt.figure(figsize=(12, 10))
        pos = nx.spring_layout(self.graph, seed=42)

        button_nodes = [n for n, attr in self.graph.nodes(data=True) if attr.get('type') == 'Button']
        method_nodes = [n for n, attr in self.graph.nodes(data=True) if attr.get('type') == 'Method']

        nx.draw_networkx_nodes(self.graph, pos, nodelist=button_nodes, node_color='skyblue', node_size=500, label='Buttons')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=method_nodes, node_color='lightgray', node_size=500, label='Methods')
        nx.draw_networkx_edges(self.graph, pos, arrows=True)
        nx.draw_networkx_labels(self.graph, pos, font_size=8)

        plt.title("Unity UI Navigation Graph (Scene + Prefabs)")
        plt.legend()
        plt.axis('off')
        plt.savefig(output_path)
        plt.close()
        print(f"Graph saved to {output_path}")

    def print_graph_info(self):
        print("Nodes (UI States):", list(self.graph.nodes))
        print("Edges (Transitions):", list(self.graph.edges))

if __name__ == "__main__":
    prefab_root = "datasets/open-project-1-main/UOP1_Project/Assets/Prefabs/UI"
    ui_objects = parse_all_prefabs(prefab_root)

    builder = UIGraphBuilder()
    builder.add_ui_objects(ui_objects)
    builder.print_graph_info()
    builder.visualize_graph()

