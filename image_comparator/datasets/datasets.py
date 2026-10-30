import ast
import os
import tempfile
import zipfile

import pandas as pd
import wildlife_datasets
from animal_re_id.datasets import TurtlesFromMetadata, TurtlewatchEgypt_Citizen, TurtlewatchEgypt_Master
from wildlife_datasets.datasets import WildlifeDataset as WD

from . import utils


class WildlifeDataset:
    def __init__(self) -> None:
        self.query: WD | None = None
        self.database: WD | None = None

    def get_index_database(self, i) -> int | None:
        assert self.database is not None
        return utils.get_index(self.database, i)

    def get_index_query(self, i) -> int | None:
        assert self.query is not None
        return utils.get_index(self.query, i)

    def download_dataset(self) -> None:
        raise NotImplementedError("Must be implemented by subclasses.")

    def is_downloaded(self) -> bool:
        raise NotImplementedError("Must be implemented by subclasses.")

    def load(self) -> None:
        raise NotImplementedError("Must be implemented by subclasses.")


class TurtlesOfSMSRC(WildlifeDataset):
    dataset_wd = wildlife_datasets.datasets.TurtlesOfSMSRC

    def __init__(self, root: str, matching_encounters_path: str | None = None) -> None:
        self.root = root
        self.matching_encounters_path = matching_encounters_path

    def download_dataset(self) -> None:
        self.dataset_wd.get_data(self.root)

    def is_downloaded(self) -> bool:
        file_name = os.path.join(self.root, "metadata.csv")
        return os.path.exists(file_name)

    def load(self) -> None:
        replace_identity = []
        if self.matching_encounters_path is not None:
            if not os.path.exists(self.matching_encounters_path):
                raise FileNotFoundError(f"Matching encounters file not found: {self.matching_encounters_path}")
            with open(self.matching_encounters_path) as f:
                replace_identity = ast.literal_eval(f.read())
        self.query = self.dataset_wd(self.root, load_segmentation=True, img_load="bbox", replace_identity=replace_identity)
        self.database = self.query


class TurtlewatchEgypt(WildlifeDataset):
    dataset_wd_query = wildlife_datasets.datasets.TurtlewatchEgypt_Citizen

    def __init__(
        self,
        file_name_individuals: str,
        file_name_downloads: str,
        root_citizen: str,
        root_heads: str,
        root_flippers_f: str,
        root_flippers_r: str,
    ) -> None:

        self.file_name_individuals = file_name_individuals
        self.file_name_downloads = file_name_downloads
        self.root_citizen = root_citizen
        self.root_heads = root_heads
        self.root_flippers_f = root_flippers_f
        self.root_flippers_r = root_flippers_r

        manual_paths = [file_name_individuals, file_name_downloads, root_heads, root_flippers_f, root_flippers_r]
        missing = [path for path in manual_paths if not os.path.exists(path)]
        if missing:
            missing_str = "\n".join(os.path.abspath(path) for path in missing)
            raise FileNotFoundError(f"These files must be copied manually and are missing:\n{missing_str}")

    def download_dataset(self) -> None:
        data = pd.read_csv(self.file_name_downloads)
        self.dataset_wd_query.get_data(self.root_citizen, data=data, force=True)

    def is_downloaded(self) -> bool:
        file_name = os.path.join(self.root_citizen, "metadata.csv")
        return os.path.exists(file_name)

    def load(self) -> None:
        dataset_kwargs_citizen = {"load_label": False}
        dataset_kwargs_master = {"load_label": False, "check_files": False, "img_load": "bbox"}

        self.query = TurtlewatchEgypt_Citizen(self.root_citizen, dataset_kwargs=dataset_kwargs_citizen).wildlife_dataset
        self.database = TurtlewatchEgypt_Master(
            self.root_heads,
            self.root_flippers_f,
            self.root_flippers_r,
            self.file_name_individuals,
            dataset_kwargs=dataset_kwargs_master,
        ).wildlife_dataset


def _download_zip(url: str | None, root: str) -> None:
    if url is None:
        raise ValueError("The config does not contain url, so the dataset cannot be downloaded.")
    with tempfile.TemporaryDirectory() as tmpdir:
        file_name = os.path.join(tmpdir, "data.zip")
        utils.download_file(url, file_name)
        with zipfile.ZipFile(file_name) as f:
            f.extractall(root)


class Identification(WildlifeDataset):
    def __init__(self, root: str, url: str | None = None) -> None:
        self.root = root
        self.url = url
        self.root_query = os.path.join(root, "query")
        self.root_database = os.path.join(root, "database")

    def download_dataset(self) -> None:
        _download_zip(self.url, self.root)

    def is_downloaded(self) -> bool:
        file_name_query = os.path.join(self.root_query, "metadata.csv")
        file_name_database = os.path.join(self.root_database, "metadata.csv")
        return os.path.exists(file_name_query) and os.path.exists(file_name_database)

    def load(self) -> None:
        dataset_kwargs = {"load_label": False}

        self.query = TurtlesFromMetadata(self.root_query, dataset_kwargs=dataset_kwargs).wildlife_dataset
        self.database = TurtlesFromMetadata(self.root_database, dataset_kwargs=dataset_kwargs).wildlife_dataset


class Discovery(WildlifeDataset):
    def __init__(self, root: str, url: str | None = None) -> None:
        self.root = root
        self.url = url

    def download_dataset(self) -> None:
        _download_zip(self.url, self.root)

    def is_downloaded(self) -> bool:
        file_name = os.path.join(self.root, "metadata.csv")
        return os.path.exists(file_name)

    def load(self) -> None:
        dataset_kwargs = {"load_label": False}

        self.query = TurtlesFromMetadata(self.root, dataset_kwargs=dataset_kwargs).wildlife_dataset
        self.database = self.query
