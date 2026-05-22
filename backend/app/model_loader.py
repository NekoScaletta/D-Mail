from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "spam_model.pkl"
VECTORIZER_PATH = BASE_DIR / "models" / "tfidf_vectorizer.pkl"


@dataclass
class ModelBundle:
    model: Any | None
    vectorizer: Any | None
    status: str
    error: str | None = None

    @property
    def ready(self) -> bool:
        return self.model is not None and self.vectorizer is not None


@lru_cache(maxsize=1)
def load_model_bundle() -> ModelBundle:
    """Load model một lần để API chạy nhanh hơn."""
    if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
        return ModelBundle(
            model=None,
            vectorizer=None,
            status="demo",
            error="Chưa tìm thấy model .pkl. Backend đang dùng fallback demo.",
        )

    try:
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
        return ModelBundle(model=model, vectorizer=vectorizer, status="trained")
    except Exception as exc:
        return ModelBundle(
            model=None,
            vectorizer=None,
            status="demo",
            error=f"Không load được model: {exc}",
        )
