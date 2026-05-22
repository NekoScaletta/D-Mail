# D-mail Project Memory

## Tổng quan

D-mail là hệ thống demo phân loại email spam cho web và mobile.

- Backend: FastAPI trong `backend/`.
- Web: React + Vite trong `web/`.
- Mobile: Expo React Native trong `mobile/`.
- Model: TF-IDF vectorizer + Logistic Regression, train bằng `backend/training/train_model.py`.

## Luồng chính

1. Web hoặc mobile gửi `POST /predict` tới backend.
2. Backend load `backend/models/spam_model.pkl` và `backend/models/tfidf_vectorizer.pkl`.
3. Nếu model chưa tồn tại, backend dùng fallback demo để app vẫn test được luồng.
4. Response gồm `prediction`, `label`, `confidence`, `model_status`, `message`.

## Lệnh thường dùng

Backend:

```bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
python training/train_model.py
```

Web:

```bash
cd web
npm run dev
npm run build
```

Mobile:

```bash
cd mobile
npm run start
```

## Ghi chú kỹ thuật

- README và comment ưu tiên tiếng Việt vì project phục vụ báo cáo sinh viên.
- Dùng Node.js 20 LTS hoặc 22 LTS cho Expo SDK 56. Node 21 có cảnh báo engine.
- Không chạy `npm audit fix --force` trong mobile vì npm có thể hạ Expo xuống SDK cũ.
