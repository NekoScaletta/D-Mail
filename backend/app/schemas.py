from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Nội dung email cần phân loại")
    use_ai: bool = Field(True, description="Ưu tiên dùng OpenAI nếu backend đã cấu hình API key")


class ImagePredictRequest(BaseModel):
    image_base64: str = Field(..., min_length=1, description="Ảnh email ở dạng base64, có hoặc không có data URL prefix")
    mime_type: str = Field("image/png", description="MIME type của ảnh")
    use_ai: bool = Field(True, description="Ưu tiên dùng OpenAI Vision nếu backend đã cấu hình API key")


class PredictResponse(BaseModel):
    prediction: str
    label: int
    confidence: float
    model_status: str
    message: str
    source: str = "ml"
    reason: str | None = None
    extracted_text: str | None = None


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    vectorizer_loaded: bool
    model_status: str
    openai_enabled: bool = False
