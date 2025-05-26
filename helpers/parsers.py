import re
import matplotlib.pyplot as plt
import os
from .graphs import draw_inheritance_graph, print_inheritance_hierarchy
import matplotlib.image as mpimg

def parse_yuml_model(file_path, verbose=True):
    classes = set()
    inheritance = []
    associations = []  # Now stores (src, dst, rel_type)

    if verbose:
        print(f"\nParsing file: {file_path}")
        print("-" * 50)

    with open(file_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line or line.startswith('//'):
                continue

            if verbose:
                print(f"\nLine {i}: {line}")

            # Extract class names from brackets
            class_names = re.findall(r'\[([^\]]+)\]', line)
            normalized = [cls.split("|")[0].strip() for cls in class_names]
            if verbose:
                print(f" Raw class tokens: {class_names}")
                print(f" Normalized class names: {normalized}")
            classes.update(normalized)

            if len(normalized) != 2:
                if verbose:
                    print(" Skipping line: Not a binary relation.")
                continue

            src, dst = normalized

            # Check for inheritance
            if "^" in line:
                inheritance.append((dst, src))  # child → parent
                if verbose:
                    print(f" Detected INHERITANCE: {dst} → {src}")

            # Check for composition
            elif "++" in line:
                associations.append((src, dst, "composition"))
                if verbose:
                    print(f" Detected COMPOSITION: {src} ++ {dst}")

            # Check for aggregation/multiplicity
            elif "*" in line:
                associations.append((src, dst, "aggregation"))
                if verbose:
                    print(f" Detected AGGREGATION: {src} * {dst}")

            # Directed association
            elif "->" in line:
                associations.append((src, dst, "association"))
                if verbose:
                    print(f" Detected ASSOCIATION: {src} -> {dst}")

            else:
                associations.append((src, dst, "unknown"))
                if verbose:
                    print(f" Detected UNKNOWN relation: {src} ? {dst}")

    if verbose:
        print("\nFinal Parsed Results")
        print(f" Classes: {sorted(classes)}")
        print(f" Inheritance Edges: {inheritance}")
        print(f" Association Edges (typed): {associations}")
        print("-" * 50)

    return classes, inheritance, associations


def inspect_model_yuml_visually(model_name, yuml_df, image_base_path="dataset/zoo"):
    """
    Display the UML image and print class hierarchy from the .yuml file.
    """
    # Get file path from yuml_df
    row = yuml_df[yuml_df["model"] == model_name]
    if row.empty:
        print(f"No .yuml file found for model '{model_name}'")
        return

    file_path = row.iloc[0]["file_path"]
    print(f"Inspecting .yuml: {file_path}")

    # Parse .yuml structure
    classes, inheritance, associations = parse_yuml_model(file_path, verbose=False)

    print(f"\nClasses ({len(classes)}): {sorted(classes)}")
    print(f"Inheritance Edges ({len(inheritance)}): {inheritance}")
    print(f"Associations ({len(associations)}): {associations}")

    # Print hierarchy
    if inheritance:
        print("\nInheritance Hierarchy:")
        print_inheritance_hierarchy(inheritance)
    else:
        print("\nNo inheritance structure found.")

    # Show UML image
    img_path = os.path.join(image_base_path, f"{model_name}.png")
    print(f"\nUML Diagram Image: {img_path}")
    if os.path.exists(img_path):
        img = mpimg.imread(img_path)
        plt.figure(figsize=(10, 10))
        plt.imshow(img)
        plt.axis("off")
        plt.title(f"UML Model: {model_name}")
        plt.show()
    else:
        print(f"No image found for model '{model_name}' at {img_path}")

        # Draw inheritance graph
    if inheritance:
        print("\nInheritance Hierarchy:")
        draw_inheritance_graph(inheritance, model_name)
    else:
        print("\nNo inheritance structure found.")