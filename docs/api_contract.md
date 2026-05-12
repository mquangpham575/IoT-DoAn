# API Contract - IoT Health Monitoring System

## 1. Mục tiêu

Tài liệu này định nghĩa chuẩn giao tiếp giữa ESP32, Backend, Dashboard và Mobile App.

Backend đóng vai trò trung tâm nhận dữ liệu cảm biến, kiểm tra dữ liệu, xử lý Edge Logic, lưu database và cung cấp API cho Dashboard/Mobile App.

## 2. Base URL

Khi chạy local:

```text
http://localhost:8000
```

Khi chạy trong cùng mạng LAN với ESP32 hoặc điện thoại:

```text
http://<LOCAL_SERVER_IP>:8000
```

Ví dụ:

```text
http://192.168.1.10:8000
```

## 3. Authentication

ESP32 hoặc simulator gửi dữ liệu lên Backend bằng API key trong header.

```http
X-API-KEY: IOT_SECRET_2026
```

Trong giai đoạn demo, API key có thể được cấu hình trong `backend/app/config.py`.

## 4. Sensor Reading API

### 4.1. Create Sensor Reading

```http
POST /api/v1/sensor/readings
```

API này dùng để ESP32 hoặc simulator gửi dữ liệu cảm biến lên Backend.

#### Request headers

```http
Content-Type: application/json
X-API-KEY: IOT_SECRET_2026
```

#### Request body

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

#### Field description

| Field | Type | Required | Description |
|---|---:|---:|---|
| `device_id` | string | Yes | Mã định danh thiết bị gửi dữ liệu |
| `temperature` | float | Yes | Nhiệt độ môi trường, đơn vị °C |
| `humidity` | float | Yes | Độ ẩm môi trường, đơn vị % |
| `gas` | integer | Yes | Chỉ số khí từ cảm biến MQ135 hoặc giá trị quy đổi tương đương |
| `light` | float | Yes | Cường độ ánh sáng, đơn vị lux |
| `noise` | integer | Yes | Chỉ số tiếng ồn hoặc raw value từ microphone module |

#### Success response

```json
{
  "status": "success",
  "message": "Sensor reading received successfully",
  "data": {
    "id": 1,
    "device_id": "esp32_01",
    "temperature": 30.5,
    "humidity": 72.0,
    "gas": 1250,
    "light": 650,
    "noise": 320,
    "comfort_level": 1,
    "status_label": "WARNING",
    "risk_score": 62,
    "reasons": [
      "High temperature",
      "Moderate air quality risk"
    ],
    "recommendation": "Nên tăng thông gió hoặc kiểm tra môi trường phòng.",
    "created_at": "2026-05-13 10:30:00"
  }
}
```

#### Error response - Invalid API key

```json
{
  "detail": "Invalid API key"
}
```

#### Error response - Invalid payload

```json
{
  "detail": [
    {
      "loc": ["body", "temperature"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

## 5. Latest Sensor Reading API

### 5.1. Get Latest Reading

```http
GET /api/v1/sensor/latest
```

API này dùng cho Dashboard hoặc Mobile App lấy dữ liệu cảm biến mới nhất.

#### Success response

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "device_id": "esp32_01",
    "temperature": 30.5,
    "humidity": 72.0,
    "gas": 1250,
    "light": 650,
    "noise": 320,
    "comfort_level": 1,
    "status_label": "WARNING",
    "risk_score": 62,
    "reasons": [
      "High temperature",
      "Moderate air quality risk"
    ],
    "recommendation": "Nên tăng thông gió hoặc kiểm tra môi trường phòng.",
    "created_at": "2026-05-13 10:30:00"
  }
}
```

#### Empty response

```json
{
  "status": "success",
  "data": null,
  "message": "No sensor readings available"
}
```

## 6. Sensor History API

### 6.1. Get Sensor History

```http
GET /api/v1/sensor/history?limit=50
```

API này dùng để lấy lịch sử dữ liệu cảm biến cho Dashboard hoặc Mobile App.

#### Query parameters

| Parameter | Type | Required | Default | Description |
|---|---:|---:|---:|---|
| `limit` | integer | No | 50 | Số lượng bản ghi muốn lấy |
| `device_id` | string | No | null | Lọc dữ liệu theo thiết bị |

#### Example request

```http
GET /api/v1/sensor/history?limit=20
```

#### Success response

```json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "id": 2,
      "device_id": "esp32_01",
      "temperature": 31.2,
      "humidity": 75.0,
      "gas": 1800,
      "light": 520,
      "noise": 450,
      "comfort_level": 1,
      "status_label": "WARNING",
      "risk_score": 58,
      "reasons": [
        "High temperature"
      ],
      "recommendation": "Nên tăng thông gió hoặc giảm nhiệt độ phòng.",
      "created_at": "2026-05-13 10:35:00"
    },
    {
      "id": 1,
      "device_id": "esp32_01",
      "temperature": 30.5,
      "humidity": 72.0,
      "gas": 1250,
      "light": 650,
      "noise": 320,
      "comfort_level": 0,
      "status_label": "NORMAL",
      "risk_score": 25,
      "reasons": [],
      "recommendation": "Môi trường hiện tại ổn định.",
      "created_at": "2026-05-13 10:30:00"
    }
  ]
}
```

## 7. System Health API

### 7.1. Health Check

```http
GET /api/v1/system/health
```

API này dùng để kiểm tra Backend còn hoạt động hay không.

#### Success response

```json
{
  "status": "ok",
  "service": "iot-health-backend",
  "version": "1.0.0",
  "database": "connected",
  "timestamp": "2026-05-13 10:30:00"
}
```

## 8. Dashboard API

### 8.1. Dashboard Page

```http
GET /
```

Trả về giao diện Dashboard HTML.

## 9. Backward-Compatible APIs

Để không làm hỏng code cũ và giúp ESP32/mobile cũ vẫn chạy được trong giai đoạn chuyển đổi, Backend có thể giữ thêm các API tương thích:

```http
POST /data
GET /history
GET /
```

Các API cũ nên gọi lại logic mới bên trong thay vì viết riêng logic khác.

## 10. Status Label Convention

| comfort_level | status_label | Meaning |
|---:|---|---|
| 0 | `NORMAL` | Môi trường ổn định |
| 1 | `WARNING` | Có chỉ số cần chú ý |
| 2 | `CRITICAL` | Có rủi ro cao, cần xử lý ngay |

## 11. Notes for Firmware Team

ESP32 chỉ cần gửi đúng JSON theo API contract. ESP32 không cần tự tính `risk_score`, `status_label` hoặc `recommendation`.

## 12. Notes for Mobile Team

Mobile App chỉ cần gọi:

```http
GET /api/v1/sensor/latest
GET /api/v1/sensor/history?limit=20
```

Mobile App không nên tự tính Edge Logic để tránh sai lệch giữa Dashboard và App.
