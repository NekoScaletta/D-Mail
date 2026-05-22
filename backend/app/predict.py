import math

import numpy as np

from app.model_loader import load_model_bundle
from app.utils import clamp_confidence, clean_text


SPAM_KEYWORDS = {
    "free",
    "winner",
    "win",
    "prize",
    "urgent",
    "click",
    "claim",
    "bonus",
    "cash",
    "offer",
    "limited",
    "congratulations",
    "lottery",
    "reward",
    "guaranteed",
    "trúng",
    "thưởng",
    "miễn",
    "phí",
    "gấp",
    "otp",
    "mật",
    "khẩu",
    "chuyển",
    "khoản",
    "vay",
    "quà",
    "link",
    "bấm",
    "nhận",
}


def _predict_with_trained_model(text: str) -> dict:
    bundle = load_model_bundle()
    cleaned = clean_text(text)
    features = bundle.vectorizer.transform([cleaned])
    label = int(bundle.model.predict(features)[0])

    if hasattr(bundle.model, "predict_proba"):
        probabilities = bundle.model.predict_proba(features)[0]
        confidence = float(np.max(probabilities))
    elif hasattr(bundle.model, "decision_function"):
        score = float(bundle.model.decision_function(features)[0])
        confidence = 1 / (1 + math.exp(-abs(score)))
    else:
        confidence = 0.75

    return {
        "prediction": "spam" if label == 1 else "ham",
        "label": label,
        "confidence": clamp_confidence(confidence),
        "model_status": "trained",
        "message": "Dự đoán bằng model đã train.",
    }


def _predict_with_demo_fallback(text: str) -> dict:
    cleaned = clean_text(text)
    words = set(cleaned.split())
    score = len(words.intersection(SPAM_KEYWORDS))
    label = 1 if score >= 2 else 0
    confidence = 0.62 + min(score, 5) * 0.06 if label == 1 else 0.68

    return {
        "prediction": "spam" if label == 1 else "ham",
        "label": label,
        "confidence": clamp_confidence(confidence),
        "model_status": "demo",
        "message": "Chưa có model đã train, backend đang dùng luật demo tạm thời.",
    }


def classify_email(text: str) -> dict:
    bundle = load_model_bundle()
    if bundle.ready:
        return _predict_with_trained_model(text)
    return _predict_with_demo_fallback(text)
