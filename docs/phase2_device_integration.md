# Phase 2 - Real Device Integration Readiness

## 1. Mục tiêu

Phase 2 không thay đổi code của người phụ trách firmware hoặc mobile app. Mục tiêu là chuẩn hóa quy trình tích hợp thiết bị thật với backend hiện tại.

Backend hiện hỗ trợ hai cách gửi dữ liệu:

```text
POST /data
POST /api/v1/sensor/readings
```

Trong đó:

- `/data` là endpoint legacy để firmware cũ vẫn chạy được.
- `/api/v1/sensor/readings` là endpoint chuẩn mới, có version API rõ ràng hơn.

## 2. Trạng thái dữ liệu hiện tại

Project hiện chưa có dữ liệu thực nghiệm từ thiết bị ESP32 thật trong GitHub.

Nguồn dữ liệu hiện tại gồm:

- Dữ liệu test bằng `curl`
- Dữ liệu từ HTTP simulator
- Dữ liệu từ MQTT simulator
- Dữ liệu runtime trong SQLite local: `backend/data/iot_data.db`

File database `.db` là runtime artifact và không commit lên GitHub.

## 3. Luồng tích hợp khuyến nghị

```text
ESP32 thật
   |
   | HTTP POST /data hoặc /api/v1/sensor/readings
   v
FastAPI Backend
   |
   | validate payload
   | edge logic
   | risk score
   | recommendation
   | Discord alert
   v
SQLite Database
   |
   v
Dashboard / Mobile App
```

## 4. Endpoint tương thích

### 4.1. Legacy endpoint

Firmware hiện tại của team có thể tiếp tục dùng:

```text
POST /data
```

Endpoint này được giữ lại để tránh làm hỏng phần firmware đã có.

### 4.2. Standard endpoint

Nếu sau này muốn chuẩn hóa API, firmware có thể đổi sang:

```text
POST /api/v1/sensor/readings
```

Endpoint này phù hợp hơn cho tài liệu, mobile app, dashboard và các lần mở rộng sau này.

## 5. Payload chuẩn

Backend kỳ vọng payload dạng:

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

Nếu firmware cũ chưa gửi `device_id`, backend có thể dùng mặc định:

```text
esp32_01
```

## 6. Cấu hình quan trọng cho ESP32

Trong firmware, `SERVER_URL` không được dùng `localhost`.

Sai:

```cpp
const char* serverUrl = "http://localhost:8000/data";
```

Đúng:

```cpp
const char* serverUrl = "http://<PC_LAN_IP>:8000/data";
```

hoặc:

```cpp
const char* serverUrl = "http://<PC_LAN_IP>:8000/api/v1/sensor/readings";
```

Ví dụ:

```cpp
const char* serverUrl = "http://192.168.1.10:8000/data";
```

## 7. Cách lấy IP của máy chạy backend

Trên WSL/Ubuntu:

```bash
hostname -I
```

Nếu chạy Docker Desktop/WSL, ưu tiên dùng IP LAN của Windows bằng:

```powershell
ipconfig
```

Sau đó tìm IPv4 của WiFi hoặc Ethernet adapter.

## 8. Điều kiện test thành công

ESP32 được xem là tích hợp thành công khi:

- Serial Monitor hiển thị ESP32 đã kết nối WiFi.
- Serial Monitor hiển thị HTTP response code `200`.
- Dashboard tăng thêm record mới.
- API `/api/v1/sensor/history?limit=5` có dữ liệu mới.
- Nếu dữ liệu vượt ngưỡng, Discord nhận được alert.
