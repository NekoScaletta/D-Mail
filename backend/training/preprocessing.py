from pathlib import Path

import pandas as pd


def normalize_label(value) -> int:
    text = str(value).strip().lower()
    if text in {"spam", "1", "true"}:
        return 1
    if text in {"ham", "not spam", "0", "false"}:
        return 0
    raise ValueError(f"Nhãn không hợp lệ: {value}")


def load_spam_dataset(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"Không tìm thấy dataset: {csv_path}")

    df = pd.read_csv(csv_path)
    label_col = _find_column(df, ["label", "v1", "category", "class"])
    text_col = _find_column(df, ["text", "message", "v2", "email"])

    cleaned = pd.DataFrame()
    cleaned["label"] = df[label_col].apply(normalize_label)
    cleaned["text"] = df[text_col].fillna("").astype(str)
    cleaned = cleaned[cleaned["text"].str.strip() != ""]
    return cleaned.drop_duplicates().reset_index(drop=True)


def _find_column(df: pd.DataFrame, candidates: list[str]) -> str:
    lowered = {column.lower(): column for column in df.columns}
    for candidate in candidates:
        if candidate in lowered:
            return lowered[candidate]
    raise ValueError(f"Dataset cần một trong các cột: {', '.join(candidates)}")
