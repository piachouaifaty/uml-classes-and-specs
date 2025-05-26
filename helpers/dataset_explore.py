import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
def display_model_image(model_name, image_base_path="dataset/zoo"):
    """
    Display a UML image corresponding to the model_name.
    """
    img_path = os.path.join(image_base_path, f"{model_name}.png")
    if os.path.exists(img_path):
        img = mpimg.imread(img_path)
        plt.figure(figsize=(10, 10))
        plt.imshow(img)
        plt.axis("off")
        plt.title(f"UML Model: {model_name}")
        plt.show()
    else:
        print(f"No image found for model '{model_name}' at {img_path}")


def display_fragment_image(fragment_id, fragments_df, image_base_path="dataset/zoo"):
    """
    Display the UML fragment image based on a fragment ID and print the filename.
    """
    row = fragments_df[fragments_df["unique_id"] == fragment_id]

    if row.empty:
        print(f"No fragment found with ID: {fragment_id}")
        return

    model_name = row.iloc[0]["model"]
    kind = row.iloc[0]["kind"]
    number = row.iloc[0]["number"]

    filename = f"{model_name}_{kind}{number}.png"
    img_path = os.path.join(image_base_path, filename)

    print(f"Fragment image path: {img_path}")

    if os.path.exists(img_path):
        img = mpimg.imread(img_path)
        plt.figure(figsize=(6, 6))
        plt.imshow(img)
        plt.axis("off")
        plt.title(f"Fragment: {filename}")
        plt.show()
    else:
        print(f"No fragment image found at {img_path}")


def display_fragment_and_model(fragment_id, fragments_df, image_base_path="dataset/zoo"):
    """
    Display both the fragment image and its corresponding full model image.
    """
    row = fragments_df[fragments_df["unique_id"] == fragment_id]

    if row.empty:
        print(f"No fragment found with ID: {fragment_id}")
        return

    model_name = row.iloc[0]["model"]

    print(f"Displaying fragment {fragment_id} and full model '{model_name}'")

    # Display fragment first (with file path)
    display_fragment_image(fragment_id, fragments_df, image_base_path)

    # Now display model image
    model_img_filename = os.path.join(image_base_path, f"{model_name}.png")
    print(f"📁 Model image path: {model_img_filename}")
    display_model_image(model_name, image_base_path)


def display_model_fragments(model_name, fragments_df, kind_filter="all"):
    """
    Display all fragment images for a given model.

    Parameters:
        model_name (str): Name of the UML model (e.g., "Make")
        fragments_df (pd.DataFrame): DataFrame with fragment metadata
        kind_filter (str): "all", "class", or "rel"
    """
    filtered = fragments_df[fragments_df["model"] == model_name]

    if kind_filter in ("class", "rel"):
        filtered = filtered[filtered["kind"] == kind_filter]

    if filtered.empty:
        print(f"No fragments found for model '{model_name}' with kind='{kind_filter}'")
        return

    for _, row in filtered.iterrows():
        frag_id = row['unique_id']
        number = row['number']
        kind = row['kind']

        print("-" * 50)
        print(f"Fragment number: {number}")
        print(f"Fragment kind: {kind}")
        print(f"Fragment ID: {frag_id}")
        display_fragment_image(frag_id, fragments_df)
