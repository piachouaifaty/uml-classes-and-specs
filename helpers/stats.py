import os
import pandas as pd
import networkx as nx
from .parsers import parse_yuml_model
from collections import Counter

def compute_model_stats(model_name, yuml_df):
    """
    Compute UML statistics for a given model:
    - Total number of blocks (classes + relationships)
    - Inheritance tree depth
    - Most frequent relationship type (across all individual types: inheritance, composition, etc.)

    Parameters:
        model_name (str): UML model name (e.g., "Make", "RelationalDBSchema")
        yuml_df (pd.DataFrame): DataFrame that maps model names to .yuml file paths

    Returns:
        dict: Statistics summary including:
            - num_classes: int
            - num_inheritance: int
            - num_associations: int (all types combined)
            - association_types: dict (e.g., {'composition': 2, 'aggregation': 1})
            - num_blocks: int
            - tree_depth: int
            - most_frequent_label: str
    """

    # --- Load and validate .yuml file ---
    row = yuml_df[yuml_df["model"] == model_name]
    if row.empty:
        raise ValueError(f"No .yuml file found for model '{model_name}'")

    file_path = row.iloc[0]["file_path"]

    # --- Parse model content from yuml ---
    # Returns: set of class names, list of (child, parent), and list of (src, dst, rel_type)
    classes, inheritance, associations = parse_yuml_model(file_path, verbose=False)

    # --- Build inheritance graph and compute max depth (if valid DAG) ---
    G = nx.DiGraph()
    G.add_edges_from(inheritance)
    if nx.is_directed_acyclic_graph(G) and len(G) > 0:
        tree_depth = nx.dag_longest_path_length(G)
    else:
        tree_depth = 0

    # --- Count each association type separately (flat) ---
    # e.g., {"composition": 2, "aggregation": 1}
    assoc_types = [rel_type for _, _, rel_type in associations]
    assoc_type_counts = Counter(assoc_types)

    # --- Flatten all relationship types into one dictionary ---
    # Includes inheritance as one of the competing types
    label_counts = assoc_type_counts.copy()
    label_counts["inheritance"] = len(inheritance)

    # --- Determine the most frequent relationship type overall ---
    most_frequent_label = label_counts.most_common(1)[0][0] if label_counts else None

    # --- Core stats ---
    num_classes = len(classes)
    num_inheritance = len(inheritance)
    num_associations = sum(assoc_type_counts.values())  # total edge count (excluding inheritance)
    num_blocks = num_classes + num_inheritance + num_associations

    return {
        "model": model_name,
        "num_classes": num_classes,
        "num_inheritance": num_inheritance,
        "num_associations": num_associations,
        "association_types": dict(assoc_type_counts),  # breakdown by type
        "num_blocks": num_blocks,
        "tree_depth": tree_depth,
        "most_frequent_label": most_frequent_label
    }


def compute_dataset_summary(stats_df):
    """
    Compute and return aggregate statistics and insights for the UML dataset.
    """

    total_models = len(stats_df)
    total_classes = stats_df["num_classes"].sum()
    total_inheritance = stats_df["num_inheritance"].sum()
    total_associations = stats_df["num_associations"].sum()
    total_blocks = stats_df["num_blocks"].sum()

    avg_classes = stats_df["num_classes"].mean()
    avg_blocks = stats_df["num_blocks"].mean()
    avg_depth = stats_df["tree_depth"].mean()
    max_depth = stats_df["tree_depth"].max()
    min_depth = stats_df["tree_depth"].min()

    std_classes = stats_df["num_classes"].std()
    std_blocks = stats_df["num_blocks"].std()
    std_depth = stats_df["tree_depth"].std()

    # Build combined association type counts across all models
    label_counts = Counter()
    for assoc_map in stats_df["association_types"]:
        label_counts.update(assoc_map)

    # Add inheritance as its own top-level label
    label_counts["inheritance"] = total_inheritance

    # Most frequent label type overall
    most_frequent_label = label_counts.most_common(1)[0][0] if label_counts else None

    # Models with deepest trees
    max_depth_models = stats_df[stats_df["tree_depth"] == max_depth]["model"].tolist()
    min_depth_models = stats_df[stats_df["tree_depth"] == min_depth]["model"].tolist()

    # Block density = blocks per class
    stats_df["block_density"] = stats_df["num_blocks"] / stats_df["num_classes"].replace(0, pd.NA)
    most_dense_models = stats_df.sort_values(by="block_density", ascending=False).head(5)[["model", "block_density"]]

    return {
        "total_models": total_models,
        "total_classes": total_classes,
        "total_inheritance": total_inheritance,
        "total_associations": total_associations,
        "total_blocks": total_blocks,

        "avg_classes_per_model": round(avg_classes, 2),
        "avg_blocks_per_model": round(avg_blocks, 2),
        "avg_tree_depth": round(avg_depth, 2),
        "std_tree_depth": round(std_depth, 2),
        "max_tree_depth": max_depth,
        "min_tree_depth": min_depth,
        "max_depth_models": max_depth_models,
        "min_depth_models": min_depth_models,

        "std_blocks_per_model": round(std_blocks, 2),
        "std_classes_per_model": round(std_classes, 2),

        "most_frequent_label_overall": most_frequent_label,
        "label_frequency_distribution": dict(label_counts),

        "top_dense_models (blocks per class)": most_dense_models.to_dict(orient="records")
    }

def pretty_print_summary(summary):
    print("\nUML Dataset Summary")
    print("=" * 40)

    print(f"Total models: {summary['total_models']}")
    print(f"Total blocks: {summary['total_blocks']}")
    print(f"  - Classes: {summary['total_classes']}")
    print(f"  - Inheritance edges: {summary['total_inheritance']}")
    print(f"  - Associations: {summary['total_associations']}")

    print("\nDepth Statistics")
    print("-" * 40)
    print(f"Average tree depth: {summary['avg_tree_depth']}")
    print(f"Standard deviation: {summary['std_tree_depth']}")
    print(f"Maximum tree depth: {summary['max_tree_depth']}")
    print(f"  - Models with max depth: {', '.join(summary['max_depth_models'])}")
    print(f"Minimum tree depth: {summary['min_tree_depth']}")
    print(f"  - Models with min depth: {', '.join(summary['min_depth_models'])}")

    print("\nBlocks per Model")
    print("-" * 40)
    print(f"Average: {summary['avg_blocks_per_model']}")
    print(f"Standard deviation: {summary['std_blocks_per_model']}")

    print("\nClasses per Model")
    print("-" * 40)
    print(f"Average: {summary['avg_classes_per_model']}")
    print(f"Standard deviation: {summary['std_classes_per_model']}")

    print("\nRelationship Label Distribution")
    print("-" * 40)
    for label, count in summary['label_frequency_distribution'].items():
        print(f"{label}: {count}")

    print(f"\nMost frequent relationship label overall: {summary['most_frequent_label_overall']}")

    print("\nTop Structurally Dense Models (blocks per class)")
    print("-" * 40)
    for entry in summary['top_dense_models (blocks per class)']:
        model = entry['model']
        density = entry['block_density']
        print(f"{model}: {density:.2f}")