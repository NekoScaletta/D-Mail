import base64
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
DEFAULT_OPENAI_MODEL = "gpt-4.1-mini"


CLASSIFICATION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "prediction": {"type": "string", "enum": ["spam", "ham"]},
        "label": {"type": "integer", "enum": [0, 1]},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "reason": {"type": "string"},
        "extracted_text": {"type": "string"},
    },
    "required": ["prediction", "label", "confidence", "reason", "extracted_text"],
}


SYSTEM_PROMPT = (
    "Bạn là bộ phân loại email spam cho ứng dụng D-mail. "
    "Hãy phân loại email là spam hoặc ham. Spam gồm lừa đảo, quảng cáo không mong muốn, "
    "trúng thưởng giả, yêu cầu bấm link gấp, yêu cầu cung cấp OTP/mật khẩu/tài khoản, "
    "hoặc nội dung dụ chuyển tiền. Ham là email bình thường, công việc, học tập, thông báo hợp lệ. "
    "Trả về JSON đúng schema. label=1 nếu spam, label=0 nếu ham. "
    "confidence là mức tự tin từ 0 đến 1. reason viết ngắn bằng tiếng Việt."
)


@dataclass
class OpenAIResult:
    prediction: str
    label: int
    confidence: float
    reason: str
    extracted_text: str = ""


def is_openai_enabled() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))


def classify_text_with_openai(text: str) -> OpenAIResult:
    payload = _base_payload(
        [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Phân loại nội dung email sau:\n\n{text}",
                    }
                ],
            }
        ]
    )
    return _request_openai(payload)


def classify_image_with_openai(image_base64: str, mime_type: str) -> OpenAIResult:
    data_url = _to_data_url(image_base64, mime_type)
    payload = _base_payload(
        [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Đọc nội dung email trong ảnh, sau đó phân loại spam hoặc ham. "
                            "Nếu ảnh không phải email hoặc không đọc được chữ, hãy dùng thông tin nhìn thấy được "
                            "và ghi rõ trong reason."
                        ),
                    },
                    {
                        "type": "input_image",
                        "image_url": data_url,
                    },
                ],
            }
        ]
    )
    return _request_openai(payload)


def _base_payload(user_input: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "model": os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL),
        "instructions": SYSTEM_PROMPT,
        "input": user_input,
        "text": {
            "format": {
                "type": "json_schema",
                "name": "email_spam_classification",
                "strict": True,
                "schema": CLASSIFICATION_SCHEMA,
            }
        },
    }


def _request_openai(payload: dict[str, Any]) -> OpenAIResult:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY chưa được cấu hình.")

    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        OPENAI_RESPONSES_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            response_data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API lỗi {exc.code}: {detail[:300]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Không kết nối được OpenAI API: {exc.reason}") from exc

    output_text = _extract_output_text(response_data)
    try:
        parsed = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError("OpenAI API trả về dữ liệu không đúng JSON.") from exc

    prediction = str(parsed.get("prediction", "")).lower()
    label = int(parsed.get("label", 1 if prediction == "spam" else 0))
    if prediction not in {"spam", "ham"}:
        prediction = "spam" if label == 1 else "ham"
    label = 1 if prediction == "spam" else 0

    return OpenAIResult(
        prediction=prediction,
        label=label,
        confidence=_clamp_float(parsed.get("confidence", 0.75)),
        reason=str(parsed.get("reason") or "Phân loại bằng OpenAI."),
        extracted_text=str(parsed.get("extracted_text") or ""),
    )


def _extract_output_text(response_data: dict[str, Any]) -> str:
    if isinstance(response_data.get("output_text"), str):
        return response_data["output_text"]

    for item in response_data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and isinstance(content.get("text"), str):
                return content["text"]

    raise RuntimeError("OpenAI API không trả về output_text.")


def _to_data_url(image_base64: str, mime_type: str) -> str:
    value = image_base64.strip()
    if value.startswith("data:image/"):
        return value

    try:
        base64.b64decode(value, validate=True)
    except Exception as exc:
        raise ValueError("Ảnh base64 không hợp lệ.") from exc

    safe_mime = mime_type if mime_type.startswith("image/") else "image/png"
    return f"data:{safe_mime};base64,{value}"


def _clamp_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = 0.75
    return round(max(0.0, min(1.0, number)), 4)
