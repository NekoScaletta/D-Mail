from pathlib import Path
import sys

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from evaluate import save_evaluation
from preprocessing import load_spam_dataset


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "spam.csv"
MODEL_DIR = BASE_DIR / "models"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def train() -> None:
    df = load_spam_dataset(DATA_PATH)

    test_size = 0.25 if len(df) >= 20 else 0.3
    stratify = df["label"] if df["label"].nunique() == 2 and len(df) >= 10 else None
    x_train, x_test, y_train, y_test = train_test_split(
        df["text"],
        df["label"],
        test_size=test_size,
        random_state=42,
        stratify=stratify,
    )

    candidates = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "Naive Bayes": MultinomialNB(),
    }

    best_name = ""
    best_pipeline = None
    best_score = -1.0
    best_predictions = None

    for name, model in candidates.items():
        pipeline = Pipeline(
            steps=[
                ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=1)),
                ("model", model),
            ]
        )
        pipeline.fit(x_train, y_train)
        predictions = pipeline.predict(x_test)
        score = f1_score(y_test, predictions, zero_division=0)
        print(f"{name} F1-score: {score:.4f}")

        if score > best_score:
            best_name = name
            best_pipeline = pipeline
            best_score = score
            best_predictions = predictions

    if best_pipeline is None:
        raise RuntimeError("Không train được model.")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_pipeline.named_steps["model"], MODEL_DIR / "spam_model.pkl")
    joblib.dump(best_pipeline.named_steps["tfidf"], MODEL_DIR / "tfidf_vectorizer.pkl")

    print("\nModel tốt nhất:", best_name)
    print(f"Accuracy : {accuracy_score(y_test, best_predictions):.4f}")
    print(f"Precision: {precision_score(y_test, best_predictions, zero_division=0):.4f}")
    print(f"Recall   : {recall_score(y_test, best_predictions, zero_division=0):.4f}")
    print(f"F1-score : {f1_score(y_test, best_predictions, zero_division=0):.4f}")
    print("\nBáo cáo chi tiết:")
    print(save_evaluation(y_test, best_predictions, Path(__file__).resolve().parent))
    print("Đã lưu model vào thư mục models/.")


if __name__ == "__main__":
    train()
