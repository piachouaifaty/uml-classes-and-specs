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

def index_zoo_files(zoo_path="dataset/zoo"):
    """
    Return a DataFrame with all files in zoo/ and basic filename metadata.
    """
    rows = []
    for fname in os.listdir(zoo_path):
        fpath = os.path.join(zoo_path, fname)
        rows.append({
            "file_name": fname,
            "file_path": fpath
        })
    return pd.DataFrame(rows)