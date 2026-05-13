# Backend & Edge Logic Runbook

## 1. Scope

This runbook is for the Backend & Edge Logic module of the IoT Health Monitoring project.

The backend is responsible for:

- Receiving sensor data from ESP32, HTTP simulator, or MQTT simulator.
- Validating sensor payloads.
- Calculating environmental risk using backend edge logic.
- Saving sensor readings into SQLite.
- Serving dashboard and API endpoints.
- Sending Discord alerts when the environment reaches WARNING or CRITICAL state.
- Supporting both legacy firmware endpoint and standardized API endpoint.

## 2. Current Architecture

```text
ESP32 / HTTP Simulator / MQTT Simulator
        |
        | HTTP POST / MQTT Publish
        v
FastAPI Backend
        |
        | Validate payload
        | Edge logic
        | Risk score
        | Recommendation
        | Discord alert
        v
SQLite Database
        |
        v
Dashboard / Android App
```

## 3. Important Paths

```text
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── sensor_router.py
│   │   ├── system_router.py
│   │   ├── dashboard_router.py
│   │   └── device_router.py
│   └── services/
│       ├── edge_service.py
│       ├── alert_service.py
│       ├── comfort_service.py
│       ├── discord_service.py
│       ├── mqtt_service.py
│       └── notification_service.py
├── templates/
│   └── dashboard.html
├── data/
│   └── iot_data.db
├── mosquitto/
│   └── mosquitto.conf
├── simulator.py
├── mqtt_simulator.py
├── Dockerfile
└── requirements.txt

docker-compose.yml
.env.example
```

## 4. Environment Variables

Create a local `.env` file from `.env.example`.

```bash
cp .env.example .env
```

Example `.env`:

```env
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

IOT_API_KEY=IOT_SECRET_2026
REQUIRE_API_KEY=true

ENABLE_DISCORD_ALERT=True
DISCORD_WEBHOOK_URL=
ALERT_COOLDOWN_SECONDS=60

ENABLE_MQTT=true
MQTT_HOST=mqtt
MQTT_PORT=1883
MQTT_TOPIC=iot/+/sensor
MQTT_CLIENT_ID=iot-health-backend
MQTT_USERNAME=
MQTT_PASSWORD=
```

Important:

- Do not commit `.env`.
- Do not commit a real Discord webhook URL.
- `backend/data/*.db` is runtime data and should not be committed.

## 5. Run with Docker Compose

Recommended for demo:

```bash
docker compose up --build
```

Backend:

```text
http://localhost:8000
```

MQTT broker:

```text
localhost:1883
```

Stop services:

```bash
docker compose down
```

Rebuild cleanly:

```bash
docker compose down
docker compose up --build
```

## 6. Run Locally without Docker

From project root:

```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

If `.venv` does not exist:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

If Ubuntu reports `ensurepip is not available`:

```bash
sudo apt update
sudo apt install python3.10-venv -y
rm -rf backend/.venv
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 7. Health Check

```bash
curl http://localhost:8000/api/v1/system/health
```

Expected:

```json
{
  "status": "ok",
  "app_name": "IoT Health Monitoring Backend",
  "version": "1.1.0",
  "database": "ok"
}
```

## 8. HTTP Sensor Test

Standard API:

```bash
curl -X POST http://localhost:8000/api/v1/sensor/readings \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: IOT_SECRET_2026" \
  -d '{
    "device_id": "esp32_01",
    "temperature": 36.5,
    "humidity": 82,
    "gas": 2300,
    "light": 120,
    "noise": 1500
  }'
```

Legacy API:

```bash
curl -X POST http://localhost:8000/data \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: IOT_SECRET_2026" \
  -d '{
    "temperature": 36.5,
    "humidity": 82,
    "gas": 2300,
    "light": 120,
    "noise": 1500
  }'
```

Expected result:

- Status should be `success`.
- `status_label` should be generated.
- `risk_score` should be generated.
- `recommendation` should be generated.
- Dashboard should update.

## 9. Read History

Standard API:

```bash
curl http://localhost:8000/api/v1/sensor/history?limit=5
```

Legacy dashboard-compatible API:

```bash
curl http://localhost:8000/history?limit=5
```

Latest reading:

```bash
curl http://localhost:8000/api/v1/sensor/latest
```

## 10. Dashboard

Open:

```text
http://localhost:8000/
```

Dashboard shows:

- Server status
- Risk score
- NORMAL / WARNING / CRITICAL status
- Sensor values
- Detected reasons
- Human-centered recommendation
- Trend charts
- History table
- Export CSV
- Dark / Light mode

## 11. HTTP Simulator

```bash
cd backend
source .venv/bin/activate
python simulator.py
```

Default target:

```text
http://localhost:8000/api/v1/sensor/readings
```

Override target:

```bash
SIMULATOR_SERVER_URL=http://localhost:8000/api/v1/sensor/readings python simulator.py
```

## 12. MQTT Flow

MQTT broker is included in Docker Compose.

Backend subscribes to:

```text
iot/+/sensor
```

MQTT simulator publishes to:

```text
iot/esp32_01/sensor
```

Run MQTT simulator locally:

```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
MQTT_HOST=localhost python mqtt_simulator.py
```

Expected:

- MQTT simulator publishes data every few seconds.
- Backend receives data through MQTT.
- Dashboard updates.
- Discord alert is triggered if WARNING or CRITICAL and Discord is enabled.

## 13. Discord Alert

Enable in `.env`:

```env
ENABLE_DISCORD_ALERT=true
DISCORD_WEBHOOK_URL=your_webhook_url_here
ALERT_COOLDOWN_SECONDS=60
```

Restart Docker:

```bash
docker compose down
docker compose up --build
```

Test CRITICAL alert:

```bash
curl -X POST http://localhost:8000/api/v1/sensor/readings \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: IOT_SECRET_2026" \
  -d '{
    "device_id": "esp32_01",
    "temperature": 41.5,
    "humidity": 88,
    "gas": 3300,
    "light": 20,
    "noise": 3100
  }'
```

Expected:

- Backend returns `CRITICAL`.
- Discord receives alert.
- Alert message gives human-centered recommendation.
- Cooldown prevents repeated spam.

## 14. Docker Logs

Check service status:

```bash
docker compose ps
```

Backend logs:

```bash
docker compose logs backend --tail=80
```

MQTT logs:

```bash
docker compose logs mqtt --tail=80
```

Useful indicators:

```text
GET /api/v1/system/health 200 OK
POST /api/v1/sensor/readings 200 OK
New client connected as iot-health-backend
```

## 15. Git Safety

Before commit:

```bash
git status
```

Do not commit:

```text
.env
backend/data/*.db
backend/.venv/
backend/ml/*.pkl
*:Zone.Identifier
```

Safe commit pattern:

```bash
git add specific_file_or_folder
git status
git commit -m "message"
git push
```

Avoid:

```bash
git add .
```

unless you are 100% sure no runtime or secret file is included.

## 16. Common Issues

### 16.1. Dashboard does not update

Check:

```bash
curl http://localhost:8000/api/v1/sensor/history?limit=5
```

If API has data but dashboard does not update:

- Refresh browser.
- Check browser console.
- Confirm correct backend URL.

### 16.2. ESP32 cannot call backend

Common cause:

- Firmware uses `localhost`.

Fix:

- Use PC/Laptop LAN IP instead.

Example:

```cpp
const char* serverUrl = "http://192.168.1.10:8000/data";
```

### 16.3. HTTP 403

Cause:

- Missing or wrong API key.

Check:

```text
X-API-KEY: IOT_SECRET_2026
```

### 16.4. HTTP 422

Cause:

- Missing required fields or invalid payload schema.

Required fields:

```text
temperature
humidity
gas
light
noise
```

Recommended field:

```text
device_id
```

### 16.5. Discord does not send

Check:

- `ENABLE_DISCORD_ALERT=true`
- `DISCORD_WEBHOOK_URL` is correct
- Reading status is WARNING or CRITICAL
- Cooldown is not blocking repeated alerts
