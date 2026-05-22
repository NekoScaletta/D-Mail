from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.model_loader import load_model_bundle
from app.predict import classify_email
from app.schemas import HealthResponse, PredictRequest, PredictResponse


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
    )


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Nội dung email không được rỗng.")

    result = classify_email(text)
    return PredictResponse(**result)
