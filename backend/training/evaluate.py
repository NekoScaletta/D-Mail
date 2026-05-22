from pathlib import Path

import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix


def save_evaluation(y_true, y_pred, output_dir: Path) -> str:
    output_dir.mkdir(parents=True, exist_ok=True)

    report = classification_report(
        y_true,
        y_pred,
        target_names=["ham", "spam"],
        zero_division=0,
    )
    matrix = confusion_matrix(y_true, y_pred)

    report_path = output_dir / "evaluation_report.txt"
    matrix_path = output_dir / "confusion_matrix.csv"

    report_path.write_text(report, encoding="utf-8")
    pd.DataFrame(
        matrix,
        index=["actual_ham", "actual_spam"],
        columns=["pred_ham", "pred_spam"],
    ).to_csv(matrix_path, encoding="utf-8")

    return report
