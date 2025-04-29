import networkx as nx

class UIGraphBuilder:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_ui_objects(self, ui_objects):
        """
        ui_objects: List of UnityUIObject from scene_parser_v3
        """
        for obj in ui_objects:
            from_node = obj.name
            # If no targets, just add the button node
            if not obj.targets:
                self.graph.add_node(from_node)
            else:
                for target in obj.targets:
                    # Add an edge for each target the button triggers
                    self.graph.add_edge(from_node, target)

    def visualize_graph(self, output_path="outputs/ui_graph.png"):
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.graph, seed=42)
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
        plt.title("Unity UI Navigation Graph")
        plt.savefig(output_path)
        plt.close()
        print(f"Graph saved to {output_path}")

    def print_graph_info(self):
        print("Nodes (UI States):", list(self.graph.nodes))
        print("Edges (Transitions):", list(self.graph.edges))

# Example usage
if __name__ == "__main__":
    from scene_parser_v3 import parse_unity_yaml

    path = "datasets/open-project-1-main/UOP1_Project/Assets/Scenes/Menus/MainMenu.unity"  # Adjust to your actual file
    ui_objects = parse_unity_yaml(path)

    builder = UIGraphBuilder()
    builder.add_ui_objects(ui_objects)
    builder.print_graph_info()
    builder.visualize_graph()
