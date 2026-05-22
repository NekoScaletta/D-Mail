# D-mail - Hệ thống phân loại email spam

D-mail là project demo gồm 3 phần:

- `backend/`: API Python FastAPI dùng chung cho web và mobile.
- `web/`: giao diện React + Vite để kiểm tra email trên trình duyệt.
- `mobile/`: app Expo React Native để kiểm tra email trên điện thoại.

Hệ thống dùng mô hình nhẹ TF-IDF + Logistic Regression để phân loại email `spam` hoặc `ham`. Khi chưa train model, backend vẫn có chế độ demo fallback để web/mobile kiểm tra được luồng gọi API.

## Kiến trúc

```text
Web React/Vite  ─┐
                 ├── POST /predict ── FastAPI ── Model TF-IDF + ML
Mobile Expo    ─┘
```

## Cách chạy nhanh

Khuyến nghị dùng:

- Python 3.11+
- Node.js 20 LTS hoặc 22 LTS. Node 21 có thể chạy web, nhưng Expo/Metro SDK mới sẽ cảnh báo engine.

### 1. Chạy backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Mở `http://localhost:8000/docs` để xem Swagger UI.

### 2. Train model thật

Backend có sẵn dataset SpamAssassin tại `backend/data/spam.csv`, được chuẩn hoá từ bộ dữ liệu OpenScience/Kaggle. Có thể thay bằng dataset lớn hơn miễn là có cột `label` và `text` hoặc `message`.

```bash
cd backend
python training/train_model.py
```

Sau khi train, model được lưu vào:

- `backend/models/spam_model.pkl`
- `backend/models/tfidf_vectorizer.pkl`

### 3. Chạy web

```bash
cd web
npm install
npm run dev
```

Web mặc định gọi API tại `http://localhost:8000`. Nếu backend deploy rồi, tạo file `.env` trong `web/`:

```env
VITE_API_URL=https://your-backend.onrender.com
```

### 4. Chạy mobile bằng Expo

```bash
cd mobile
npm install
npm run start
```

Nếu chạy trên điện thoại thật, đổi URL API trong `mobile/.env` hoặc `mobile/api.js` sang IP LAN của máy tính, ví dụ:

```env
EXPO_PUBLIC_API_URL=http://192.168.1.10:8000
```

Nếu gặp cảnh báo Node engine từ Expo, đổi sang Node 20 LTS hoặc Node 22 LTS rồi chạy lại `npm install`.

## Deploy

### Backend lên Render

1. Đưa repo lên GitHub.
2. Tạo Web Service trên Render.
3. Root directory: `backend`.
4. Build command: `pip install -r requirements.txt && python training/train_model.py`.
5. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
6. Render sẽ tự train model từ `backend/data/spam.csv` trong lúc build, nên không cần commit file `.pkl`.

### Web lên Vercel

1. Import repo vào Vercel.
2. Root directory: `web`.
3. Build command: `npm run build`.
4. Output directory: `dist`.
5. Thêm biến môi trường `VITE_API_URL` trỏ về URL backend Render.

## Gợi ý ảnh chụp cho báo cáo

- Cấu trúc thư mục project.
- Swagger UI của FastAPI tại `/docs`.
- Kết quả train model có Accuracy, Precision, Recall, F1-score.
- Web đang phân loại một email spam.
- Web đang phân loại một email không spam.
- App mobile chạy trên Expo Go.
- Sơ đồ kiến trúc web/mobile gọi chung backend.

## Gợi ý khi thuyết trình demo

- Trình bày lý do chọn TF-IDF + Logistic Regression vì nhẹ, dễ deploy free.
- Demo backend `/predict` trước bằng Swagger.
- Demo web và mobile cùng gọi một backend.
- Giải thích fallback demo chỉ để test luồng khi chưa có model, còn kết quả chính thức dùng model đã train.
- Nêu cách thay dataset mẫu bằng dataset lớn hơn để cải thiện độ chính xác.
