import pandas as pd


def convert_identity(answers: pd.DataFrame, col_identity: str, col_encounter: str | None = None) -> pd.Series:
    mask = answers[col_identity] == "unknown"
    if not mask.any():
        return answers[col_identity]
    if col_encounter not in answers.columns:
        raise ValueError(f"Column {col_encounter} must be in answers if there are unknown identities")
    if answers.loc[mask, col_encounter].isnull().sum() > 0:
        raise ValueError(f"Column {col_encounter} must not have nans if there are unknown identities")
    identity = answers[col_identity].copy().astype(str)
    identity[mask] = "unknown" + "_" + answers.loc[mask, col_encounter].astype(str)
    return identity


def read_answers(file_name: str) -> pd.DataFrame:
    # Identities are read as strings so that the same identity is equal in both columns, missing identities are unknown
    columns = ["identity1", "identity2"]
    answers = pd.read_csv(file_name, dtype={column: str for column in columns})
    answers[columns] = answers[columns].fillna("unknown")
    return answers
