# Web React + Vite

Web cho phép người dùng nhập nội dung email, gọi backend `/predict`, rồi hiển thị kết quả spam/không spam và độ tin cậy.

## Cài đặt

```bash
npm install
```

## Chạy local

```bash
npm run dev
```

Mặc định web gọi API tại `http://localhost:8000`.

## Cấu hình backend URL

Tạo file `.env` trong thư mục `web/`:

```env
VITE_API_URL=http://localhost:8000
```

Khi deploy Vercel, đổi thành URL backend Render:

```env
VITE_API_URL=https://your-backend.onrender.com
```

## Deploy Vercel

- Root directory: `web`
- Build command: `npm run build`
- Output directory: `dist`
