import argparse
import json
import os
import tkinter as tk
from importlib.resources import files

from .app import App
from .app.app import DATA_CSV
from .app.utils import download_file
from .datasets import TurtlesOfSMSRC, TurtlewatchEgypt, WildlifeDataset

DATASETS = {
    "TurtlesOfSMSRC": TurtlesOfSMSRC,
    "TurtlewatchEgypt": TurtlewatchEgypt,
}


def load_config(project: str, config_path: str | None) -> dict:
    cfg = {}
    config_file = files("wildlife_re_id_app") / "configs" / f"{project}.json"
    if config_file.is_file():
        cfg = json.loads(config_file.read_text())
    elif config_path is None:
        raise FileNotFoundError(f"Config not found: {project}")

    if config_path is not None:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config not found: {config_path}")
        with open(config_path) as f:
            cfg.update(json.load(f))
    return cfg


def get_dataset(cfg: dict) -> tuple[WildlifeDataset, str]:
    kwargs = dict(cfg)
    name = kwargs.pop("dataset")
    kwargs.pop("downloads", None)
    dataset_cls = DATASETS[name]
    return dataset_cls(**kwargs), name


def download(dataset: WildlifeDataset, downloads: dict[str, str]) -> None:
    print("Downloading the dataset. This may take tens of minutes.")
    dataset.download_dataset()
    for path, url in downloads.items():
        print(f"Downloading {path}")
        download_file(url, path)
    print("Download finished.")


def check_files(dataset: WildlifeDataset, downloads: dict[str, str], project: str) -> None:
    missing = []
    if not dataset.is_downloaded():
        missing.append("the dataset")
    paths = set(downloads) | {DATA_CSV}
    for path in sorted(paths):
        if not os.path.exists(path):
            missing.append(path)
    if missing:
        missing_str = "\n".join(missing)
        raise SystemExit(f"Missing:\n{missing_str}\nRun 'wildlife-app {project} --download' or copy the files into {os.getcwd()}.")


def main() -> None:
    parser = argparse.ArgumentParser(prog="wildlife-app")
    parser.add_argument("project", help="Project name, such as turtles_of_smsrc.")
    parser.add_argument("--config", help="Custom config file merged into the built-in one.")
    parser.add_argument("--download", action="store_true", help="Download the dataset and the files listed in the config before starting the app.")
    args = parser.parse_args()

    if os.path.samefile(os.getcwd(), os.path.expanduser("~")):
        raise RuntimeError("Do not run the app in the home folder. Create a folder for the project and run it there.")

    cfg = load_config(args.project, args.config)
    dataset, name = get_dataset(cfg)
    if args.download:
        download(dataset, cfg.get("downloads", {}))
    check_files(dataset, cfg.get("downloads", {}), args.project)

    root = tk.Tk()
    App(root, dataset, name)
    root.mainloop()


if __name__ == "__main__":
    main()
