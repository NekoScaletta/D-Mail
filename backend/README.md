# Backend FastAPI

Backend nhận nội dung email từ web/mobile, tiền xử lý văn bản, load model đã train và trả về kết quả phân loại.

## Cài đặt

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Chạy API local

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoint chính:

- `GET /`: kiểm tra server.
- `GET /health`: kiểm tra trạng thái model.
- `POST /predict`: phân loại email.
- `POST /predict-image`: phân loại ảnh chụp email bằng ChatGPT API khi có `OPENAI_API_KEY`.

Body mẫu:

```json
{
  "text": "Congratulations, you won a free prize"
}
```

Response mẫu:

```json
{
  "prediction": "spam",
  "label": 1,
  "confidence": 0.94,
  "model_status": "trained",
  "message": "Dự đoán bằng model đã train."
}
```

## ChatGPT API

Nếu cấu hình `OPENAI_API_KEY`, endpoint `/predict` sẽ ưu tiên OpenAI Responses API để phân loại văn bản. Nếu không có key hoặc OpenAI lỗi, backend tự fallback về model TF-IDF đã train.

Endpoint `/predict-image` nhận JSON:

```json
{
  "image_base64": "<base64>",
  "mime_type": "image/png"
}
```

Biến môi trường:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
```

## Train model

Dataset nằm tại `data/spam.csv`. File hiện tại dùng bộ SpamAssassin từ OpenScience/Kaggle và đã được chuẩn hoá về các cột:

- `label`: `ham`, `spam`, `0`, hoặc `1`.
- `text` hoặc `message`: nội dung email.

Chạy:

```bash
python training/train_model.py
```

Kết quả:

- Model: `models/spam_model.pkl`
- Vectorizer: `models/tfidf_vectorizer.pkl`
- Báo cáo: `training/evaluation_report.txt`
- Confusion matrix: `training/confusion_matrix.csv`

## Deploy Render

- Root directory: `backend`
- Build command: `pip install -r requirements.txt && python training/train_model.py`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Render sẽ tự train model từ `data/spam.csv` trong lúc build, nên không cần commit 2 file `.pkl` trong `models/`.
