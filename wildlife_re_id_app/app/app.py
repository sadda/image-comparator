import os
import time
import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox, ttk
from typing import cast

import numpy as np
import pandas as pd
from PIL import Image, ImageTk

from ..datasets import WildlifeDataset
from .rules import ANS_NEG, ANS_POS, ANS_UNK, MatchingRules, QueryDatabaseRules, QueryQueryRules

DATA_CSV = "verification_data.csv"
ANS_CSV = "answers.csv"
CANVAS_SIZE = 400


class App:
    def __init__(self, root: tk.Tk, dataset: WildlifeDataset, name: str) -> None:
        self.root = root
        self.root.title("Image Comparator")
        self.dataset = dataset
        self.name = name
        self.skip_filled = True
        self.closed = False

        # Load the verification data
        df = pd.read_csv(DATA_CSV)
        assert isinstance(df.index, pd.RangeIndex)

        # Load the dataset
        self.dataset.load()
        assert self.dataset.query is not None

        # Select the rules for skipping and navigation
        assert self.dataset.database is not None
        self.rules_cls: type[MatchingRules]
        if self.dataset.query.metadata.equals(self.dataset.database.metadata):
            self.rules_cls = QueryQueryRules
        else:
            self.rules_cls = QueryDatabaseRules

        # Build UI
        self.idx = 0
        self.idx_shown = 0
        self.increase = True
        self._build_ui()
        self._bind_keys()
        self._initialize_answers(df)
        self._check_answers(df)
        if self.closed:
            return
        self._initial_load()
        if self.closed:
            return
        self._reset_i_lr()

        # A messagebox shown earlier runs its own event loop before mainloop() starts and can leave
        # the OS keyboard focus off this window, silently breaking the key bindings. Reclaim it now.
        self.root.lift()
        self.root.focus_force()

    def _initialize_answers(self, df):
        # Load the answer data
        if os.path.exists(ANS_CSV):
            self.answers = pd.read_csv(ANS_CSV)
            self.answers["answer"] = self.answers["answer"].astype(object)
            self.answers["time"] = self.answers["time"].astype(float)
        else:
            self.answers = df.copy()
            self.answers["answer"] = None
            self.answers["time"] = 0.0

        # Verify the segmentation data
        self.answers["index1"] = self.answers["image_id1"].apply(self.dataset.get_index_query)
        self.answers["index2"] = self.answers["image_id2"].apply(self.dataset.get_index_database)

    def _check_answers(self, df):
        # Verify the answer data
        columns1 = self.answers.columns.difference({"answer", "time", "index1", "index2"})
        columns2 = df.columns
        if set(columns1) != set(columns2) or not self.answers[columns1].equals(df[columns1]):
            messagebox.showinfo("Info", f"File {ANS_CSV} has wrong format. It may help to delete it. The application will now close.")
            self._close()

    def _initial_load(self):
        idx_null = self.answers[["index1", "index2"]].isnull()
        if idx_null.any().any():
            messagebox.showinfo("Info", "Some entries are mismatched. Try to run the app with --download.")
        else:
            # Load the first couple of images
            self._initialize_skipping()
            self.load_row()

    def _actions(self) -> list[tuple[str, str | None, Callable, int, int]]:
        return [
            ("Same (Q)", "q", self.on_same, 0, 0),
            ("Different (W)", "w", self.on_diff, 0, 1),
            ("Unknown (E)", "e", self.on_unknown, 0, 2),
            ("Previous (A)", "a", self.on_prev, 1, 0),
            ("Next (S)", "s", self.on_next, 1, 1),
            (self.rules_cls.next_label, None, self.next_group, 1, 2),
            ("Toggle heads left (R)", "r", self.on_toggle_left, 2, 0),
            ("Toggle heads right (F)", "f", self.on_toggle_right, 2, 1),
            ("Reset (V)", "v", self.on_reset, 2, 2),
        ]

    def _build_ui(self) -> None:
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Image frame
        self.img_frame = ttk.Frame(self.main_frame)
        self.img_frame.pack(pady=(0, 10))

        self.encounter_var_l = tk.StringVar()
        self.encounter_var_r = tk.StringVar()
        self.encounter_label_l = ttk.Entry(self.img_frame, textvariable=self.encounter_var_l, state="readonly", justify="center")
        self.encounter_label_r = ttk.Entry(self.img_frame, textvariable=self.encounter_var_r, state="readonly", justify="center")
        self.encounter_label_l.grid(row=0, column=0, padx=5, sticky="ew")
        self.encounter_label_r.grid(row=0, column=1, padx=5, sticky="ew")

        self.canvas_l = tk.Canvas(self.img_frame, width=CANVAS_SIZE, height=CANVAS_SIZE)
        self.canvas_r = tk.Canvas(self.img_frame, width=CANVAS_SIZE, height=CANVAS_SIZE)
        self.canvas_l.grid(row=1, column=0, padx=5)
        self.canvas_r.grid(row=1, column=1, padx=5)

        # Counter frame
        self.counter_var = tk.StringVar()
        self.counter_label = ttk.Label(self.main_frame, textvariable=self.counter_var, font=("TkDefaultFont", 12, "bold"))
        self.counter_label.pack(pady=(0, 10))

        # Bottom area
        self.bottom_frame = ttk.Frame(self.main_frame)
        self.bottom_frame.pack(fill="both", expand=True)

        # Buttons (left)
        self.btn_frame = ttk.Frame(self.bottom_frame)
        self.btn_frame.grid(row=0, column=0, sticky="nw")

        # Text (right)
        bg = self.root.cget("background")
        self.text_frame = tk.Frame(self.bottom_frame, bg=bg)
        self.text_frame.grid(row=0, column=1, sticky="n", padx=(20, 0))
        self.text_box = tk.Text(
            self.text_frame,
            width=60,
            height=10,
            wrap="word",
            bg=bg,
            relief="flat",
            highlightthickness=0,
            state="disabled",
            takefocus=0,
        )
        self.text_box.pack(fill="both", expand=True)

        for text, _, action, row, col in self._actions():
            ttk.Button(self.btn_frame, text=text, command=action).grid(row=row, column=col)

    def _close(self) -> None:
        self.closed = True
        self.root.destroy()

    def _bind_keys(self) -> None:
        for _, key, action, _, _ in self._actions():
            if key is not None:
                self.root.bind(key, lambda e, a=action: a())

    def _elapsed_since_plot(self) -> float:
        return time.perf_counter() - self.plot_time

    def _fit_to_canvas(self, img: Image.Image) -> Image.Image:
        w, h = img.size
        scale = min(CANVAS_SIZE / w, CANVAS_SIZE / h)
        new_size = (int(w * scale), int(h * scale))
        return img.resize(new_size, Image.Resampling.LANCZOS)

    def _log_time(self) -> None:
        current = cast(float, self.answers.loc[self.idx, "time"])
        elapsed = self._elapsed_since_plot()
        self.answers.loc[self.idx, "time"] = current + elapsed
        self._save_csv()

    def _reset_time(self) -> None:
        self.plot_time = time.perf_counter()

    def _save_csv(self) -> None:
        answers_save = self.answers.drop(["index1", "index2"], axis=1)
        answers_save.to_csv(ANS_CSV, index=False)

    def _set_text(self) -> None:
        # TODO: add more information?
        self.text_box.config(state="normal")
        self.text_box.delete("1.0", "end")
        assert self.dataset.query is not None and self.dataset.database is not None
        for line in self.rules.progress(self.dataset.query.metadata, self.dataset.database.metadata):
            self.text_box.insert("end", f"{line}\n")
        self.text_box.config(state="disabled")

    def on_same(self, event=None) -> None:
        self._log_time()
        self.answer(ANS_POS)

    def on_diff(self, event=None) -> None:
        self._log_time()
        self.answer(ANS_NEG)

    def on_unknown(self, event=None) -> None:
        self._log_time()
        self.answer(ANS_UNK)

    def on_toggle_left(self, event=None) -> None:
        self._toggle("l")

    def on_toggle_right(self, event=None) -> None:
        self._toggle("r")

    def on_prev(self, event=None) -> None:
        self._log_time()
        self.prev()

    def on_next(self, event=None) -> None:
        self._log_time()
        self.next()

    def on_reset(self, event=None) -> None:
        img1, img2 = self.load_images()
        self._show_image(img1, "l")
        self._show_image(img2, "r")
        self._reset_i_lr()

    def next_group(self) -> None:
        self.skip_filled = True
        column = self.rules.next_column
        unique_values = self.answers[column].unique()
        i = np.where(self.answers.iloc[self.idx][column] == unique_values)[0][0]
        i = np.mod(i + 1, len(unique_values))
        self.idx = np.where(unique_values[i] == self.answers[column])[0][0] - 1
        self.next()

    def _reset_i_lr(self) -> None:
        self.i_l = 0
        self.i_r = 0

    def _update_i_lr(self, n: int, position: str) -> None:
        if position == "l":
            self.i_l = (self.i_l + 1) % n
        elif position == "r":
            self.i_r = (self.i_r + 1) % n

    def _toggle(self, position):
        if position == "l":
            dataset = self.dataset.query
            i = self.i_l
        elif position == "r":
            dataset = self.dataset.database
            i = self.i_r
        else:
            raise ValueError("Position must be l or r.")
        assert dataset is not None

        # TODO: do not hard-code heads
        column, value = self.rules.toggle_filter(self.idx, position)
        mask1 = dataset.metadata["label"] == "head"
        mask2 = dataset.metadata[column] == value
        metadata_reduced = dataset.metadata[mask1 & mask2]
        metadata_reduced = metadata_reduced.sort_values("score", ascending=False)
        index = dataset.metadata.index.get_indexer(metadata_reduced.index)

        if len(index) > 0:
            img = dataset[index[i]]
            self._show_image(img, position)
            self._update_i_lr(len(index), position)

    def _initialize_skipping(self):
        self.rules = self.rules_cls(self.answers)

    def _update_answer(self, answer_new: str) -> None:
        answer_old = self.answers.loc[self.idx, "answer"]
        answer = self.rules.update(self.idx, answer_old, answer_new)
        if answer != answer_new and self.rules.reject_message is not None:
            messagebox.showinfo("Info", self.rules.reject_message)
        self.answers.loc[self.idx, "answer"] = answer

    def _answer_empty(self) -> bool:
        answer = self.answers.iloc[self.idx]["answer"]
        return pd.isnull(answer) or answer == ""

    def _skip_plotting(self) -> bool:
        if self.skip_filled:
            return self.rules.answer_exists(self.idx) or not self._answer_empty()
        else:
            return self.rules.answer_exists(self.idx) and self._answer_empty()

    def load_image_database(self, i: int | None = None) -> Image.Image:
        assert self.dataset.database is not None
        if i is None:
            i = self.idx
        row = self.answers.iloc[i]
        img = self.dataset.database[row["index2"]]
        assert isinstance(img, Image.Image)
        return img

    def load_image_query(self, i: int | None = None) -> Image.Image:
        assert self.dataset.query is not None
        if i is None:
            i = self.idx
        row = self.answers.iloc[i]
        img = self.dataset.query[row["index1"]]
        assert isinstance(img, Image.Image)
        return img

    def load_images(self, **kwargs) -> tuple[Image.Image, Image.Image]:
        img1 = self.load_image_query(**kwargs)
        img2 = self.load_image_database(**kwargs)
        return img1, img2

    def _show_image(self, img, position):
        if position == "l":
            self.canvas_l.delete("all")
            self.tk_img_l = ImageTk.PhotoImage(self._fit_to_canvas(img))
            self.canvas_l.create_image(200, 200, image=self.tk_img_l)
        elif position == "r":
            self.canvas_r.delete("all")
            self.tk_img_r = ImageTk.PhotoImage(self._fit_to_canvas(img))
            self.canvas_r.create_image(200, 200, image=self.tk_img_r)
        else:
            raise ValueError("Position must be l or r.")

    def _update_encounter_labels(self) -> None:
        row = self.answers.iloc[self.idx]
        self.encounter_var_l.set(f"Encounter: {row['encounter1']}")
        self.encounter_var_r.set(f"Encounter: {row['encounter2']}")

    def load_row(self) -> None:
        # Move to the first row which should be shown. A loop and not recursion, which fails for long skips.
        while True:
            if not (0 <= self.idx < len(self.answers)):
                if self.skip_filled:
                    messagebox.showinfo("Info", "All turtles were identified. Either delete some rows in answers.csv or the whole file.")
                self._close()
                return

            if not self._skip_plotting():
                img1, img2 = self.load_images()
                if img1 is not None and img2 is not None:
                    break

            if self.increase:
                self.idx += 1
            elif self.idx > 0:
                self.idx -= 1
            else:
                # Nothing to show before, stay at the displayed row
                self.idx = self.idx_shown
                return

        self.idx_shown = self.idx
        similarity = self.answers.iloc[self.idx]["similarity_orig"]
        text = f"{self.name} image {self.idx + 1}/{len(self.answers)} - similarity {similarity:.0f}"
        answer = self.answers.iloc[self.idx]["answer"]
        if not pd.isnull(answer):
            text = f"{text} - {answer.upper()}"
        self.counter_var.set(text)

        self._show_image(img1, "l")
        self._show_image(img2, "r")
        self._update_encounter_labels()

        # TODO: after the first displayed row, answered rows are shown again when moving forward.
        # In a resumed session, one unanswered row forces the user to go through all answered rows again.
        self.skip_filled = False
        self._set_text()
        self._reset_i_lr()

        self._reset_time()

    def answer(self, answer) -> None:
        self._update_answer(answer)
        self._save_csv()
        self.next()

    def next(self) -> None:
        self.increase = True
        self.idx += 1
        self.load_row()

    def prev(self) -> None:
        if self.idx > 0:
            self.increase = False
            self.idx -= 1
            self.load_row()
