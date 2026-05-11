# Hệ thống Giám sát Sức khỏe và Tiện nghi Môi trường (Nhóm 9)

## 1. Tổng quan Đề tài
Xây dựng hệ thống IoT giám sát môi trường trong nhà (nhiệt độ, độ ẩm, CO₂, ánh sáng, tiếng ồn) theo thời gian thực. Hệ thống sử dụng **AI Hybrid Engine** để đánh giá mức độ tiện nghi và phát hiện rủi ro sức khỏe.

---

## 2. Cấu trúc Dự án (Project Structure)

Dự án được tổ chức theo các module chuyên nghiệp:

```text
/ (Root)
├── firmware/           # Mã nguồn thiết bị nhúng
│   └── esp32_main/     # Code ESP32 (Arduino/C++)
├── backend/            # Central Server & AI
│   ├── templates/      # Dashboard UI
│   ├── server.py       # FastAPI Server
│   ├── comfort_model.pkl
│   └── iot_data.db
├── mobile/             # Ứng dụng Android (Kotlin)
└── README.md           # Tài liệu hướng dẫn
```

---

## 3. Thiết kế Phần cứng (Hardware)

### 3.1. Danh sách linh kiện (BOM)
- **Controller:** ESP32 DevKit V1.
- **Cảm biến:** DHT22, MQ135, BH1750, MAX4466.
- **Cảnh báo:** Còi Buzzer 5V, LED 5mm.

### 3.2. Sơ đồ chân (Pin Mapping)
| Linh kiện | Chân ESP32 |
| :--- | :--- |
| **DHT22** | GPIO 4 |
| **MQ135** | GPIO 34 (ADC1) |
| **Max4466** | GPIO 35 (ADC1) |
| **BH1750** | 21 (SDA) / 22 (SCL) |
| **Buzzer** | GPIO 18 |
| **LED** | GPIO 19 |

---

## 4. Hướng dẫn Vận hành

### 4.1. Khởi động Backend
```bash
cd backend
python server.py
```
- **Dashboard:** `http://localhost:8000/`

### 4.2. Nạp Firmware ESP32
Mở file `firmware/esp32_main/esp32_main.ino` bằng Arduino IDE.
- **WiFi:** `iot-nhom9` / `12345678`
- **Server URL:** `http://10.0.88.218:8000/data`

---

## 5. Phân công Nhiệm vụ
- **Member 1**: Thiết kế phần cứng và lắp ráp.
- **Member 2**: Lập trình nhúng và Edge Logic.
- **Member 3**: Phát triển AI và hệ thống Rule-base.
- **Member 4**: Phát triển Backend API và Dashboard.
- **Member 5**: Phát triển App Android và mDNS Discovery.
