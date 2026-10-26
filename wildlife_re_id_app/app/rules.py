from typing import Protocol

import networkx as nx
import numpy as np
import pandas as pd

from .utils import convert_identity

ANS_POS = "same"
ANS_NEG = "different"
ANS_UNK = ""


class MatchingRules(Protocol):
    # Columns used for toggling: (column in answers, column in metadata)
    toggle_columns: dict[str, tuple[str, str]]
    # Column used for jumping to the next group and the label of its button
    next_column: str
    next_label: str
    # Message shown when update rejects an answer (None for no message)
    reject_message: str | None

    def __init__(self, answers: pd.DataFrame) -> None: ...

    def answer_exists(self, idx: int) -> bool: ...

    def update(self, idx: int, answer_old: str, answer_new: str) -> str: ...

    def progress(self, query: pd.DataFrame, database: pd.DataFrame) -> list[str]: ...


class QueryQueryRules:
    """Query encounters are matched with each other. "Same" answers merge encounters into clusters."""

    toggle_columns = {
        "l": ("encounter1", "encounter_id"),
        "r": ("encounter2", "encounter_id"),
    }
    next_column = "matching_part"
    next_label = "Next body part"
    reject_message = None

    def __init__(self, answers: pd.DataFrame) -> None:
        self.answers = answers
        self.identity1 = convert_identity(answers, "identity1", "encounter1")
        self.identity2 = convert_identity(answers, "identity2", "encounter2")

        mask_same = answers["answer"] == ANS_POS
        nodes = np.unique(self.identity1.to_list() + self.identity2.to_list())
        edges_same = zip(self.identity1[mask_same], self.identity2[mask_same])
        self.G_same = nx.Graph()
        self.G_same.add_nodes_from(nodes.tolist())
        self.G_same.add_edges_from(edges_same)
        self._check()

    def _check(self) -> None:
        if not nx.is_forest(self.G_same):
            raise ValueError("G_same must not have any cycles")
        mask_diff = self.answers["answer"] == ANS_NEG
        for a, b in zip(self.identity1[mask_diff], self.identity2[mask_diff]):
            if nx.has_path(self.G_same, a, b):
                raise ValueError("Cluster contains both same and different.")
    
    def answer_exists(self, idx: int) -> bool:
        a = self.identity1.iloc[idx]
        b = self.identity2.iloc[idx]

        # Rule 1: the identities are already in the same cluster
        if nx.has_path(self.G_same, a, b):
            return True

        # Rule 2: the clusters of the identities are connected by a "different" answer
        comp_a = nx.node_connected_component(self.G_same, a)
        comp_b = nx.node_connected_component(self.G_same, b)
        mask_diff = self.answers["answer"] == ANS_NEG
        for u, v in zip(self.identity1[mask_diff], self.identity2[mask_diff]):
            if (u in comp_a and v in comp_b) or (v in comp_a and u in comp_b):
                return True
        return False

    def update(self, idx: int, answer_old: str, answer_new: str) -> str:
        # TODO: the whole logic will break if A-B same, B-C different, A-C different and the user changes B-C to same
        a = self.identity1.iloc[idx]
        b = self.identity2.iloc[idx]
        if answer_new == answer_old:
            return answer_new
        if answer_new == ANS_POS:
            # Rule: keep the forest structure (no cycles), so "same" is rejected for already connected identities
            if nx.has_path(self.G_same, a, b):
                return ANS_UNK
            self.G_same.add_edge(a, b)
        elif answer_old == ANS_POS:
            self.G_same.remove_edge(a, b)
        return answer_new

    def _decided(self) -> pd.Series:
        # Same as answer_exists for all rows, but computes the components and "different" pairs only once
        component = {}
        for i, nodes in enumerate(nx.connected_components(self.G_same)):
            for node in nodes:
                component[node] = i
        component1 = self.identity1.map(component)
        component2 = self.identity2.map(component)

        mask_diff = self.answers["answer"] == ANS_NEG
        pairs_diff = set(zip(component1[mask_diff], component2[mask_diff]))
        pairs_diff |= {(b, a) for a, b in pairs_diff}

        same_component = component1 == component2
        diff_component = pd.Series([pair in pairs_diff for pair in zip(component1, component2)], index=self.answers.index)
        return same_component | diff_component

    def progress(self, query: pd.DataFrame, database: pd.DataFrame) -> list[str]:
        n_encounters = query["encounter_id"].nunique()
        n_identities = query.loc[query["identity"] != "unknown", "identity"].nunique()
        decided = self._decided()
        lines = [f"DATASET: {n_encounters} ENCOUNTERS, {n_identities} KNOWN IDENTITIES.", ""]
        for matching_part, answers_part in self.answers.groupby("matching_part"):
            n = len(answers_part)
            n_answered = answers_part["answer"].notnull().sum()
            n_decided = decided[answers_part.index].sum()
            lines.append(f"{str(matching_part).upper()} ({n}): answered {n_answered}, decided {n_decided}.")
        return lines


class QueryDatabaseRules:
    """Query encounters are matched with database identities. Each encounter has at most one identity."""

    toggle_columns = {
        "l": ("encounter1", "encounter_id"),
        "r": ("identity2", "identity"),
    }
    next_column = "encounter1"
    next_label = "Next encounter"
    # TODO: it would be more helpful to provide the specific reason
    # TODO: update should return a potential error message instead of the new answer
    reject_message = "The encounter is already identified as another identity. The answer was not accepted."

    def __init__(self, answers: pd.DataFrame) -> None:
        self.answers = answers
        self._check()

    def _identified_as(self, encounter: str, exclude_idx: int | None = None) -> set[str]:
        mask = (self.answers["encounter1"] == encounter) & (self.answers["answer"] == ANS_POS)
        if exclude_idx is not None:
            mask &= self.answers.index != exclude_idx
        return set(self.answers.loc[mask, "identity2"])

    def _check(self) -> None:
        answers_same = self.answers[self.answers["answer"] == ANS_POS]
        for encounter, answers_encounter in answers_same.groupby("encounter1"):
            identities = set(answers_encounter["identity2"])
            if len(identities) > 1:
                raise ValueError(f"Encounter {encounter} is identified as multiple identities: {identities}.")

    def answer_exists(self, idx: int) -> bool:
        row = self.answers.iloc[idx]

        # Rule 1: the encounter is already identified
        if self._identified_as(row["encounter1"]):
            return True

        # Rule 2: the encounter was already marked as different from this identity (possibly for another body part)
        mask = (self.answers["encounter1"] == row["encounter1"]) & (self.answers["identity2"] == row["identity2"])
        if (self.answers.loc[mask, "answer"] == ANS_NEG).any():
            return True
        return False

    def update(self, idx: int, answer_old: str, answer_new: str) -> str:
        row = self.answers.iloc[idx]
        if answer_new == ANS_POS:
            # Rule: an encounter cannot be the same as two different identities
            identities = self._identified_as(row["encounter1"], exclude_idx=idx)
            if identities - {row["identity2"]}:
                return ANS_UNK
        return answer_new

    def progress(self, query: pd.DataFrame, database: pd.DataFrame) -> list[str]:
        n_encounters = query["encounter_id"].nunique()
        n_identities = database["identity"].nunique()
        # Number of candidate identities and of identities answered as different for each encounter
        pairs = self.answers[["encounter1", "identity2"]].drop_duplicates()
        pairs_diff = self.answers.loc[self.answers["answer"] == ANS_NEG, ["encounter1", "identity2"]].drop_duplicates()
        n_candidates = pairs.groupby("encounter1").size()
        n_diff = pairs_diff.groupby("encounter1").size().reindex(n_candidates.index, fill_value=0)

        encounters_same = self.answers.loc[self.answers["answer"] == ANS_POS, "encounter1"]
        identified = n_candidates.index.isin(encounters_same)
        new = ~identified & (n_diff == n_candidates).to_numpy()
        n = len(n_candidates)
        n_identified = identified.sum()
        n_new = new.sum()
        n_open = n - n_identified - n_new
        return [
            f"QUERY: {n_encounters} ENCOUNTERS. DATABASE: {n_identities} IDENTITIES.",
            "",
            f"ENCOUNTERS ({n}): identified {n_identified}, new {n_new}, open {n_open}.",
        ]
