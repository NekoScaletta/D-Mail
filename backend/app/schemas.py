from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Nội dung email cần phân loại")


class PredictResponse(BaseModel):
    prediction: str
    label: int
    confidence: float
    model_status: str
    message: str


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    vectorizer_loaded: bool
    model_status: str
