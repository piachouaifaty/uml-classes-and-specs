import networkx as nx
import matplotlib.pyplot as plt

def print_inheritance_hierarchy(inheritance_edges):
    """
    Pretty-print the inheritance tree using indentation.
    Assumes edges are in the format (child, parent).
    """
    print("\nBuilding inheritance graph...")
    G = nx.DiGraph()
    G.add_edges_from(inheritance_edges)

    print("Original edges (child --> parent):")
    for edge in inheritance_edges:
        print(f"  {edge[0]} → {edge[1]}")

    # Flip direction for traversal: parent --> child
    print("\nReversing graph for hierarchy traversal (parent --? child)...")
    G_view = G.reverse(copy=False)

    roots = [n for n in G_view.nodes if G_view.in_degree(n) == 0]
    print(f"\n[INFO] Detected hierarchy roots (no parents): {roots}")

    def print_subtree(node, depth=0):
        indent = "  " * depth
        print(f"{indent}↳ {node}")
        children = list(G_view.successors(node))
        if children:
            print(f"{indent}{node} has children: {children}")
        for child in children:
            print_subtree(child, depth + 1)

    for root in roots:
        print(f"\n=== Inheritance Tree Root: {root} ===")
        print_subtree(root)



def draw_inheritance_graph(inheritance_edges, model_name):
    """
    Draw a directed graph of inheritance edges (child → parent).
    """
    if not inheritance_edges:
        print(f"[INFO] No inheritance edges to draw for {model_name}")
        return

    G = nx.DiGraph()
    G.add_edges_from(inheritance_edges)

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(
        G, pos,
        with_labels=True,
        arrows=True,
        node_color="#dceefb",
        edge_color="#0369a1",
        node_size=2000,
        font_size=10,
        font_weight='bold'
    )
    plt.title(f"Inheritance Graph for {model_name}")
    plt.show()
