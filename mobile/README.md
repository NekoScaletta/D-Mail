# Mobile Expo

Mobile app dùng Expo React Native để nhập nội dung email, gọi backend `/predict`, rồi hiển thị kết quả.

## Cài đặt

Nên dùng Node.js 20 LTS hoặc 22 LTS. Node 21 có thể báo cảnh báo engine với Expo/Metro.

```bash
npm install
```

## Chạy với Expo Go

```bash
npm run start
```

Quét QR bằng Expo Go trên điện thoại.

## Cấu hình API URL

Mặc định app dùng:

```text
http://localhost:8000
```

Khi chạy trên điện thoại thật, `localhost` là điện thoại, không phải máy tính. Hãy tạo file `.env` trong `mobile/`:

```env
EXPO_PUBLIC_API_URL=http://192.168.1.10:8000
```

Thay `192.168.1.10` bằng IP LAN của máy đang chạy backend.

## Ghi chú audit

Project dùng Expo SDK 56. `npm audit` hiện còn cảnh báo moderate từ dependency nội bộ `xcode -> uuid`. Không nên chạy `npm audit fix --force` vì npm sẽ hạ Expo xuống SDK cũ và làm vỡ tương thích.
