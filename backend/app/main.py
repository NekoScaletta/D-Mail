from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.model_loader import load_model_bundle
from app.openai_classifier import classify_image_with_openai, classify_text_with_openai, is_openai_enabled
from app.predict import classify_email
from app.schemas import HealthResponse, ImagePredictRequest, PredictRequest, PredictResponse


app = FastAPI(
    title="D-mail Spam Detection API",
    description="API phân loại email spam dùng chung cho web và mobile.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict:
    return {
        "message": "D-mail backend đang hoạt động.",
        "docs": "/docs",
        "predict_endpoint": "/predict",
    }


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    bundle = load_model_bundle()
    return HealthResponse(
        status="ok",
        model_loaded=bundle.model is not None,
        vectorizer_loaded=bundle.vectorizer is not None,
        model_status=bundle.status,
        openai_enabled=is_openai_enabled(),
    )


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Nội dung email không được rỗng.")

    if request.use_ai and is_openai_enabled():
        try:
            ai_result = classify_text_with_openai(text)
            return PredictResponse(
                prediction=ai_result.prediction,
                label=ai_result.label,
                confidence=ai_result.confidence,
                model_status="openai",
                message="Dự đoán bằng ChatGPT API.",
                source="openai",
                reason=ai_result.reason,
                extracted_text=ai_result.extracted_text or text,
            )
        except Exception:
            # Nếu OpenAI lỗi, app vẫn hoạt động bằng model đã train.
            pass

    result = classify_email(text)
    return PredictResponse(**result)


@app.post("/predict-image", response_model=PredictResponse)
def predict_image(request: ImagePredictRequest) -> PredictResponse:
    if not request.use_ai or not is_openai_enabled():
        raise HTTPException(
            status_code=503,
            detail="Chưa cấu hình OPENAI_API_KEY nên backend chưa phân loại ảnh trực tiếp bằng ChatGPT API.",
        )

    try:
        ai_result = classify_image_with_openai(request.image_base64, request.mime_type)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return PredictResponse(
        prediction=ai_result.prediction,
        label=ai_result.label,
        confidence=ai_result.confidence,
        model_status="openai",
        message="Dự đoán ảnh bằng ChatGPT API.",
        source="openai_vision",
        reason=ai_result.reason,
        extracted_text=ai_result.extracted_text,
    )
