# Setup Guide - IoT Health Monitoring System

## 1. Mục tiêu

Tài liệu này hướng dẫn cách chạy Backend, Simulator và Dashboard trong giai đoạn chưa có thiết bị ESP32 thật.

Trong giai đoạn này, simulator sẽ đóng vai trò như ESP32 và gửi dữ liệu cảm biến giả lập lên Backend.

## 2. Yêu cầu môi trường

Máy cần có:

- Python 3.10 trở lên
- Git
- Trình duyệt web
- Kết nối mạng nội bộ nếu muốn test Mobile App bằng điện thoại

Kiểm tra Python:

```bash
python --version
```

Hoặc:

```bash
python3 --version
```

## 3. Clone repository

```bash
git clone git@github.com:mquangpham575/IoT-DoAn.git
cd IoT-DoAn
```

Checkout sang branch backend:

```bash
git switch feature/backend-edge-logic
```

## 4. Cấu trúc Backend

```text
backend/
├── app/
├── templates/
├── static/
├── data/
├── ml/
├── simulator.py
├── requirements.txt
└── run.py
```

## 5. Tạo virtual environment

Từ thư mục root project:

```bash
cd backend
python -m venv .venv
```

Kích hoạt virtual environment trên Linux/WSL/macOS:

```bash
source .venv/bin/activate
```

Kích hoạt virtual environment trên Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 6. Cài dependencies

```bash
pip install -r requirements.txt
```

## 7. Chạy Backend

Trong thư mục `backend`:

```bash
python run.py
```

Hoặc nếu dùng Uvicorn trực tiếp:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Nếu chạy thành công, Backend sẽ mở tại:

```text
http://localhost:8000
```

## 8. Kiểm tra Backend Health

Mở terminal khác và chạy:

```bash
curl http://localhost:8000/api/v1/system/health
```

Kết quả mong đợi:

```json
{
  "status": "ok",
  "service": "iot-health-backend",
  "version": "1.0.0",
  "database": "connected"
}
```

## 9. Chạy Simulator

Simulator dùng để giả lập ESP32 gửi dữ liệu lên Backend.

Trong thư mục `backend`:

```bash
python simulator.py
```

Simulator sẽ gửi dữ liệu định kỳ lên API:

```text
POST http://localhost:8000/api/v1/sensor/readings
```

## 10. Mở Dashboard

Sau khi Backend chạy, mở trình duyệt:

```text
http://localhost:8000
```

Dashboard sẽ hiển thị:

- Nhiệt độ
- Độ ẩm
- Gas
- Ánh sáng
- Tiếng ồn
- Risk score
- Trạng thái môi trường
- Cảnh báo
- Lịch sử dữ liệu

## 11. Test API thủ công

### 11.1. Gửi sensor reading

```bash
curl -X POST http://localhost:8000/api/v1/sensor/readings \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: IOT_SECRET_2026" \
  -d '{
    "device_id": "esp32_01",
    "temperature": 30.5,
    "humidity": 72.0,
    "gas": 1250,
    "light": 650,
    "noise": 320
  }'
```

### 11.2. Lấy dữ liệu mới nhất

```bash
curl http://localhost:8000/api/v1/sensor/latest
```

### 11.3. Lấy lịch sử dữ liệu

```bash
curl "http://localhost:8000/api/v1/sensor/history?limit=20"
```

## 12. Kết nối Mobile App trong cùng mạng LAN

Tìm IP của máy đang chạy Backend:

```bash
ip addr
```

Hoặc:

```bash
hostname -I
```

Ví dụ IP là:

```text
192.168.1.10
```

Trên Mobile App, nhập Backend URL:

```text
http://192.168.1.10:8000
```

Lưu ý:

- Điện thoại và laptop phải cùng mạng WiFi.
- Firewall của máy tính không được chặn port 8000.
- Backend phải chạy với host `0.0.0.0`, không phải chỉ `127.0.0.1`.

## 13. Git workflow

Sau khi tạo hoặc sửa file:

```bash
git status
```

Add file cần commit:

```bash
git add backend/app backend/requirements.txt backend/run.py docs .gitignore
```

Commit:

```bash
git commit -m "chore: initialize backend edge logic structure"
```

Push:

```bash
git push
```

## 14. Lưu ý không commit file runtime

Không nên commit:

- SQLite database
- File model `.pkl` sinh ra
- Virtual environment
- Cache Python

Các file này nên được ignore trong `.gitignore`:

```gitignore
backend/data/*.db
backend/*.db
backend/ml/*.pkl
backend/.venv/
__pycache__/
*.pyc
.env
```

## 15. Troubleshooting

### Backend không chạy

Kiểm tra đã cài dependencies chưa:

```bash
pip install -r requirements.txt
```

### Simulator báo connection refused

Kiểm tra Backend đã chạy chưa:

```bash
curl http://localhost:8000/api/v1/system/health
```

### Mobile không kết nối được Backend

Kiểm tra:

- Điện thoại và laptop có cùng WiFi không
- Backend có chạy host `0.0.0.0` không
- IP nhập trên app có đúng không
- Firewall có chặn port 8000 không

### Database không có dữ liệu

Kiểm tra simulator đã gửi dữ liệu chưa:

```bash
python simulator.py
```

Sau đó gọi:

```bash
curl "http://localhost:8000/api/v1/sensor/history?limit=5"
```
