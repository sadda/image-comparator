import json
import sys
import tkinter as tk
from importlib.resources import files

from .app import App
from .datasets import TurtlesOfSMSRC, TurtlewatchEgypt, WildlifeDataset

DATASETS = {
    "TurtlesOfSMSRC": TurtlesOfSMSRC,
    "TurtlewatchEgypt": TurtlewatchEgypt,
}


def get_dataset(project: str) -> tuple[WildlifeDataset, str]:
    config_file = files("wildlife_re_id_app") / "configs" / f"{project}.json"
    if not config_file.is_file():
        raise FileNotFoundError(f"Config not found: {project}")
    cfg = json.loads(config_file.read_text())

    dataset_cls = DATASETS[cfg["dataset"]]
    kwargs = cfg.get("kwargs", {})
    return dataset_cls(**kwargs), cfg["dataset"]


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("Usage: wildlife-app <project>")
    dataset, name = get_dataset(sys.argv[1])
    root = tk.Tk()
    App(root, dataset, name)
    root.mainloop()


if __name__ == "__main__":
    main()
