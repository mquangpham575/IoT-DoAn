# System Architecture - IoT Health Monitoring System

## 1. Tổng quan hệ thống

Hệ thống Giám sát Sức khỏe và Tiện nghi Môi trường là một hệ thống IoT dùng để theo dõi các chỉ số môi trường trong nhà theo thời gian thực.

Các chỉ số chính gồm:

- Nhiệt độ
- Độ ẩm
- Chất lượng không khí hoặc khí độc hại
- Ánh sáng
- Tiếng ồn

Backend đóng vai trò trung tâm trong hệ thống. Backend nhận dữ liệu từ ESP32 hoặc simulator, kiểm tra dữ liệu, lưu vào database, xử lý Edge Logic và cung cấp dữ liệu cho Dashboard/Mobile App.

## 2. Luồng dữ liệu tổng quát

```text
ESP32 / Simulator
        |
        | HTTP POST JSON
        v
Backend API - FastAPI
        |
        | Validate payload
        v
Edge Logic / Comfort Engine
        |
        | Calculate comfort_level, risk_score, reasons, recommendation
        v
SQLite Database
        |
        | Query latest/history
        v
Dashboard / Android App
```

## 3. Thành phần hệ thống

### 3.1. Firmware - ESP32

ESP32 đọc dữ liệu từ các cảm biến và gửi dữ liệu lên Backend.

Cảm biến dự kiến:

| Sensor | Purpose |
|---|---|
| DHT22 | Đo nhiệt độ và độ ẩm |
| MQ135 | Đo chất lượng không khí hoặc khí |
| BH1750 | Đo cường độ ánh sáng |
| MAX4466 | Thu tín hiệu âm thanh/tiếng ồn |

ESP32 có thể xử lý một phần logic cảnh báo cục bộ như bật LED hoặc buzzer khi chỉ số vượt ngưỡng nghiêm trọng. Tuy nhiên, logic đánh giá chính vẫn được Backend xử lý để đảm bảo dữ liệu nhất quán giữa Dashboard và Mobile App.

### 3.2. Backend API

Backend được xây dựng bằng FastAPI.

Nhiệm vụ chính:

- Nhận dữ liệu cảm biến từ ESP32 hoặc simulator
- Validate dữ liệu đầu vào
- Kiểm tra API key
- Tính toán Edge Logic
- Tính risk score
- Sinh trạng thái môi trường
- Sinh nguyên nhân cảnh báo
- Sinh khuyến nghị xử lý
- Lưu dữ liệu vào SQLite database
- Cung cấp API cho Dashboard và Mobile App

### 3.3. SQLite Database

SQLite được dùng làm database local vì phù hợp với đồ án, dễ chạy, không cần cài đặt server database riêng.

Dữ liệu chính cần lưu:

- ID bản ghi
- Device ID
- Temperature
- Humidity
- Gas
- Light
- Noise
- Comfort level
- Status label
- Risk score
- Reasons
- Recommendation
- Created time

### 3.4. Edge Logic / Comfort Engine

Edge Logic là phần đánh giá môi trường dựa trên rule-based processing.

Backend xử lý:

- Phát hiện chỉ số vượt ngưỡng
- Xác định mức cảnh báo
- Tính điểm rủi ro từ 0 đến 100
- Kết hợp nhiều chỉ số để đưa ra trạng thái cuối cùng
- Sinh khuyến nghị phù hợp

Trong giai đoạn đầu, hệ thống ưu tiên rule-based logic để đảm bảo dễ kiểm thử, dễ giải thích và phù hợp với demo IoT.

### 3.5. Dashboard

Dashboard hiển thị dữ liệu môi trường theo thời gian thực.

Dashboard nên có:

- Card chỉ số hiện tại
- Risk score
- Status label
- Lý do cảnh báo
- Khuyến nghị xử lý
- Biểu đồ lịch sử
- Alarm log
- Export CSV nếu cần

### 3.6. Mobile App

Mobile App dùng để theo dõi nhanh trạng thái môi trường.

Mobile App gọi API từ Backend:

- Lấy dữ liệu mới nhất
- Lấy lịch sử gần đây
- Hiển thị trạng thái môi trường
- Hiển thị cảnh báo

Mobile App không nên tự tính logic cảnh báo. Tất cả logic chính nên đến từ Backend để đảm bảo đồng bộ.

## 4. Backend folder structure

```text
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── sensor_router.py
│   │   ├── device_router.py
│   │   ├── dashboard_router.py
│   │   └── system_router.py
│   ├── services/
│   │   ├── edge_service.py
│   │   ├── comfort_service.py
│   │   ├── alert_service.py
│   │   └── device_service.py
│   └── utils/
│       ├── time_utils.py
│       └── response_utils.py
├── templates/
│   └── dashboard.html
├── static/
│   ├── css/
│   └── js/
├── data/
│   └── iot_data.db
├── ml/
│   ├── train_ai.py
│   └── comfort_model.pkl
├── simulator.py
├── requirements.txt
└── run.py
```

## 5. Backend module responsibility

| Module | Responsibility |
|---|---|
| `main.py` | Tạo FastAPI app, gắn router, cấu hình middleware |
| `config.py` | Quản lý cấu hình chung |
| `database.py` | Kết nối SQLite và khởi tạo database |
| `schemas.py` | Định nghĩa request/response schema |
| `sensor_router.py` | API nhận và trả dữ liệu cảm biến |
| `system_router.py` | API kiểm tra tình trạng backend |
| `edge_service.py` | Rule-based edge processing |
| `comfort_service.py` | Tổng hợp logic đánh giá tiện nghi |
| `alert_service.py` | Sinh cảnh báo và khuyến nghị |
| `device_service.py` | Quản lý thông tin thiết bị |
| `simulator.py` | Giả lập ESP32 khi chưa có thiết bị thật |

## 6. Deployment mode trong giai đoạn đồ án

### Local development

```text
Laptop chạy Backend + Dashboard
Simulator giả lập ESP32
Mobile App gọi API bằng IP LAN
```

### Hardware integration

```text
ESP32 gửi dữ liệu thật qua WiFi
Backend nhận dữ liệu trong cùng mạng LAN
Dashboard và Mobile App hiển thị dữ liệu thời gian thực
```

## 7. Lý do chọn kiến trúc này

Kiến trúc này phù hợp với đồ án vì:

- Dễ phát triển khi chưa có thiết bị thật
- Có thể kiểm thử bằng simulator
- Backend tách rõ API, database và logic xử lý
- Dashboard và Mobile App không phụ thuộc trực tiếp vào ESP32
- Khi có ESP32 thật, chỉ cần thay simulator bằng thiết bị thật
- Dễ mở rộng sang MQTT, mDNS hoặc AI model ở giai đoạn sau
