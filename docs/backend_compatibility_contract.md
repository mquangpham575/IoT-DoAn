# Backend Compatibility Contract

## 1. Vì sao cần compatibility?

Trong team IoT, firmware, backend và mobile thường được phát triển song song. Nếu backend thay đổi API đột ngột, firmware có thể bị lỗi.

Vì vậy backend hiện hỗ trợ cả endpoint cũ và endpoint mới:

```text
POST /data
POST /api/v1/sensor/readings
```

## 2. Ý nghĩa từng endpoint

### `/data`

Đây là endpoint legacy. Mục tiêu là đảm bảo firmware cũ của team vẫn hoạt động mà không cần sửa ngay.

### `/api/v1/sensor/readings`

Đây là endpoint chuẩn mới. Mục tiêu là làm API rõ nghĩa hơn, có version, dễ mở rộng và dễ viết tài liệu.

## 3. Chiến lược tích hợp

Không ép firmware đổi API ngay.

Chiến lược đúng là:

```text
Firmware cũ dùng /data -> vẫn chạy
Firmware mới dùng /api/v1/sensor/readings -> càng tốt
Backend gom cả hai về cùng một logic xử lý
```

## 4. Logic xử lý chung

Cả hai endpoint đều đi qua cùng backend pipeline:

```text
Receive payload
   |
Validate sensor fields
   |
Evaluate backend edge logic
   |
Calculate risk score
   |
Generate reasons
   |
Generate human-centered recommendation
   |
Save to SQLite
   |
Trigger Discord alert if needed
```

## 5. Khi teammate không dùng API mới

Nếu teammate tiếp tục dùng `/data`, hệ thống vẫn hoạt động.

Điều kiện duy nhất là firmware phải gửi dữ liệu về một endpoint mà backend hỗ trợ. Nếu firmware không gửi dữ liệu về backend, dashboard và alert sẽ không có dữ liệu thiết bị thật.

## 6. Payload tối thiểu

```json
{
  "temperature": 30.5,
  "humidity": 72.0,
  "gas": 1250,
  "light": 650,
  "noise": 320
}
```

## 7. Payload khuyến nghị

```json
{
  "device_id": "esp32_01",
  "temperature": 30.5,
  "humidity": 72.0,
  "gas": 1250,
  "light": 650,
  "noise": 320
}
```
