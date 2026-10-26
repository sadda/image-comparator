import argparse
import json
import os
import tkinter as tk
from importlib.resources import files

from .app import App
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
    dataset_cls = DATASETS[name]
    return dataset_cls(**kwargs), name


def main() -> None:
    parser = argparse.ArgumentParser(prog="wildlife-app")
    parser.add_argument("project", help="Project name, such as turtles_of_smsrc.")
    parser.add_argument("--config", help="Custom config file merged into the built-in one.")
    args = parser.parse_args()

    if os.path.samefile(os.getcwd(), os.path.expanduser("~")):
        raise RuntimeError("Do not run the app in the home folder. Create a folder for the project and run it there.")

    cfg = load_config(args.project, args.config)
    dataset, name = get_dataset(cfg)
    root = tk.Tk()
    App(root, dataset, name)
    root.mainloop()


if __name__ == "__main__":
    main()
