import re


def clean_text(text: str) -> str:
    """Tiền xử lý đơn giản, phù hợp với TF-IDF."""
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", " url ", text)
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    text = text.replace("_", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clamp_confidence(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 4)
