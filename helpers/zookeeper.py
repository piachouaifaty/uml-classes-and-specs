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


