# Phase 4 - MQTT, Docker and Discord Alert

## 1. Goal

This phase improves the IoT backend with three practical engineering features:

- Dockerized backend deployment
- MQTT broker integration using Mosquitto
- Discord alert for WARNING and CRITICAL sensor readings

## 2. Architecture

```text
ESP32 / HTTP Simulator / MQTT Simulator
        |
        | HTTP POST or MQTT publish
        v
FastAPI Backend
        |
        | Edge logic + risk score + recommendation
        v
SQLite Database
        |
        v
Dashboard

If WARNING or CRITICAL:
        |
        v
Discord Webhook Alert
```

## 3. MQTT Topic

Default subscribe topic:

```text
iot/+/sensor
```

Example publish topic:

```text
iot/esp32_01/sensor
```

## 4. MQTT Payload

```json
{
  "device_id": "esp32_01",
  "temperature": 36.5,
  "humidity": 82,
  "gas": 2300,
  "light": 120,
  "noise": 1500
}
```

## 5. Docker Run

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

Start services:

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

## 6. Discord Alert

Enable in `.env`:

```env
ENABLE_DISCORD_ALERT=true
DISCORD_WEBHOOK_URL=your_webhook_url_here
ALERT_COOLDOWN_SECONDS=60
```

Never commit the real webhook URL.

## 7. Test HTTP

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

## 8. Test MQTT

When Docker Compose is running, test MQTT simulator locally:

```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
MQTT_HOST=localhost python mqtt_simulator.py
```

Then open the dashboard:

```text
http://localhost:8000
```
