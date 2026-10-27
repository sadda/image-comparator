import os

import pandas as pd
import requests
from wildlife_datasets.datasets import WildlifeDataset


def get_index(dataset: WildlifeDataset, image_id: int | str) -> int | None:
    # The returned index label is used as a position in dataset[i], so the index must be 0, 1, ..., n-1
    assert dataset.metadata.index.equals(pd.RangeIndex(len(dataset.metadata))), "Metadata index must be 0, 1, ..., n-1."
    idx = dataset.metadata["image_id"] == image_id
    if idx.sum() > 1:
        raise ValueError("image_id found multiple times.")
    elif idx.sum() == 1:
        return dataset.metadata[idx].index[0]
    elif idx.sum() == 0:
        print(f"image_id {image_id} not found")
        return None


def download_file(url: str, output_path: str) -> None:
    r = requests.get(url, allow_redirects=True)
    r.raise_for_status()
    output_dir = os.path.dirname(output_path)
    if output_dir != "":
        os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(r.content)
