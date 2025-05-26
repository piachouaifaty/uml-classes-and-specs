import re
import os
import pandas as pd

def parse_zoo_filename(file_name):
    """
    Parse a zoo filename into kind, number, and file type.
    Handles:
    - Fragment files: Model_class0.plantuml
    - Full model files: Model.plantuml / Model.yuml
    """
    file_name = file_name.strip()

    # First check for fragment-style files: Model_kindNumber.ext
    #<ModelName>_<Kind><Number>.<Extension>
    match = re.match(r"^(.+?)_(class|rel)(\d+)\.(\w+)$", file_name, re.IGNORECASE)
    if match:
        model, kind, number, ext = match.groups()
        return kind.lower(), int(number), ext.lower()

    # Then check for full-model files: Model.ext
    match_full = re.match(r"^(.+?)\.(\w+)$", file_name, re.IGNORECASE)
    if match_full:
        model, ext = match_full.groups()
        return "full", None, ext.lower()

    return None, None, None


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


def match_models_to_zoo_files(models_df, zoo_files_df):
    """
    Match zoo files to known model names (prefix match).
    Returns:
        matched_df: files matched to a model
        unmatched_files_df: zoo files not matched to any model
        unmatched_models_df: models not matched to any file
    """
    matched_rows = []
    matched_file_names = set()
    matched_models = set()

    model_names = models_df['name'].unique()

    for model_name in model_names:
        matches = zoo_files_df[zoo_files_df['file_name'].str.startswith(model_name)]
        if not matches.empty:
            matched_models.add(model_name)
        for _, row in matches.iterrows():
            matched_rows.append({
                "model": model_name,
                "file_name": row["file_name"],
                "file_path": row["file_path"]
            })
            matched_file_names.add(row["file_name"])

    matched_df = pd.DataFrame(matched_rows)

    # Files not matched to any model
    unmatched_files_df = zoo_files_df[~zoo_files_df['file_name'].isin(matched_file_names)].copy()

    # Models that didn't match any file
    unmatched_models_df = models_df[~models_df['name'].isin(matched_models)].copy()

    return matched_df, unmatched_files_df, unmatched_models_df


