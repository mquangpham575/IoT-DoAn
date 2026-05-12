# Branch Change Summary - feature/backend-edge-logic

## 1. Branch Purpose

Branch:

```text
feature/backend-edge-logic
```

Purpose:

- Build a structured backend module for the IoT Health Monitoring project.
- Add backend-side edge logic.
- Support dashboard visualization.
- Add Docker, MQTT, and Discord alert integration.
- Keep compatibility with existing firmware that uses the old `/data` endpoint.

## 2. High-Level Changes

This branch changes the backend from a simple single-file prototype into a structured FastAPI backend.

Main improvements:

- New backend project structure.
- API versioning.
- SQLite persistence.
- Rule-based backend edge logic.
- Risk score calculation.
- Human-centered recommendations.
- Dashboard UI improvement.
- Dark / Light mode.
- Docker Compose deployment.
- MQTT broker integration.
- Discord alert integration.
- Real-device integration documentation.
- Backward compatibility for existing firmware.

## 3. Backend Structure Added

Added:

```text
backend/app/
├── main.py
├── config.py
├── database.py
├── models.py
├── schemas.py
├── routers/
│   ├── sensor_router.py
│   ├── system_router.py
│   ├── dashboard_router.py
│   └── device_router.py
├── services/
│   ├── edge_service.py
│   ├── comfort_service.py
│   ├── alert_service.py
│   ├── discord_service.py
│   ├── mqtt_service.py
│   ├── notification_service.py
│   └── device_service.py
└── utils/
    ├── response_utils.py
    └── time_utils.py
```

Why:

- Separate routing, database, edge logic, alerting, and configuration.
- Make the backend easier to maintain and explain during demo.
- Avoid putting all logic inside one `server.py`.

## 4. API Changes

### 4.1. Standard API

Added:

```text
POST /api/v1/sensor/readings
GET  /api/v1/sensor/latest
GET  /api/v1/sensor/history?limit=50
GET  /api/v1/system/health
GET  /api/v1/devices/default
```

### 4.2. Legacy API Kept

Kept:

```text
POST /data
GET  /history
GET  /
```

Why:

- Existing firmware already uses `/data`.
- The backend must not break teammate firmware.
- `/data` and `/api/v1/sensor/readings` both route into the same backend processing pipeline.

## 5. Sensor Payload

Standard payload:

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

Legacy payload without `device_id` is still supported through backend default value.

## 6. Edge Logic Added

Added file:

```text
backend/app/services/edge_service.py
```

Responsibilities:

- Evaluate environmental condition.
- Detect abnormal temperature, humidity, gas, light, and noise values.
- Calculate `risk_score`.
- Generate `comfort_level`.
- Generate `status_label`.
- Generate `reasons`.

Status levels:

```text
0 -> NORMAL
1 -> WARNING
2 -> CRITICAL
```

## 7. Recommendation Logic Improved

Added/updated:

```text
backend/app/services/alert_service.py
```

Changes:

- Recommendation is now human-centered.
- Recommendation guides people to improve the environment.
- Recommendation does not tell users to move the device.
- This is more realistic because the ESP32 is a fixed monitoring node.

Example improved recommendation:

```text
Không khí có dấu hiệu kém an toàn. Nên tăng thông gió, mở cửa hoặc kiểm tra xem trong phòng có khói, mùi lạ hay nguồn khí bất thường không.
```

## 8. Database Added

Added SQLite database initialization:

```text
backend/app/database.py
backend/data/iot_data.db
```

The database stores:

```text
id
device_id
temperature
humidity
gas
light
noise
comfort_level
status_label
risk_score
reasons
recommendation
created_at
```

Note:

- `backend/data/*.db` is ignored by Git.
- Database is runtime data and should not be committed.

## 9. Dashboard Improved

Updated:

```text
backend/templates/dashboard.html
```

Dashboard now shows:

- Server online/offline status.
- Risk score.
- NORMAL / WARNING / CRITICAL label.
- Sensor values.
- Detected reasons.
- Human-centered recommendation.
- Trend charts.
- Recent readings table.
- CSV export.
- Dark / Light mode.

## 10. Simulator Updated

Updated:

```text
backend/simulator.py
```

Purpose:

- Simulate ESP32 HTTP data.
- Send payload to the standard API endpoint:

```text
/api/v1/sensor/readings
```

Added:

```text
backend/mqtt_simulator.py
```

Purpose:

- Simulate ESP32 MQTT publisher.
- Publish JSON payload to:

```text
iot/esp32_01/sensor
```

## 11. Docker Added

Added:

```text
Dockerfile
docker-compose.yml
backend/.dockerignore
```

Docker Compose services:

```text
backend
mqtt
```

Backend port:

```text
8000
```

MQTT broker port:

```text
1883
```

## 12. MQTT Added

Added:

```text
backend/app/services/mqtt_service.py
backend/mosquitto/mosquitto.conf
```

Backend subscribes to:

```text
iot/+/sensor
```

Expected MQTT payload uses the same schema as HTTP.

Why:

- Adds support for IoT messaging protocol.
- Aligns better with IoT Engineering course topics.
- Allows future ESP32 or gateway to publish data through MQTT.

## 13. Discord Alert Added

Added:

```text
backend/app/services/discord_service.py
backend/app/services/notification_service.py
```

Behavior:

- Sends alert when status is WARNING or CRITICAL.
- Uses Discord webhook from `.env`.
- Applies cooldown to avoid spam.

Important:

- Real webhook URL must not be committed.
- `.env` must remain ignored.

## 14. Documentation Added

Added docs:

```text
docs/api_contract.md
docs/system_architecture.md
docs/edge_logic_rules.md
docs/setup_guide.md
docs/phase4_mqtt_docker_discord.md
docs/phase2_device_integration.md
docs/backend_compatibility_contract.md
docs/real_device_test_checklist.md
docs/real_device_troubleshooting.md
docs/real_device_data_template.csv
docs/esp32_backend_integration_note.md
```

Purpose:

- Explain API contract.
- Explain system architecture.
- Explain edge logic.
- Explain Docker/MQTT/Discord setup.
- Explain real ESP32 integration.
- Provide checklist for teammate testing.

## 15. What Was Not Changed

To avoid conflict with teammates:

- Firmware file should not be overwritten unless firmware owner agrees.
- Mobile app should not be overwritten unless mobile owner agrees.
- Existing `/data` endpoint is preserved.
- Legacy `/history` endpoint is preserved.

## 16. Current Data Limitation

The branch does not contain real experimental data from ESP32 hardware.

Current data sources are:

- curl test data.
- HTTP simulator data.
- MQTT simulator data.
- local SQLite runtime data.

Real device evidence still needs to be collected from the teammate who has the hardware.

## 17. Recommended Demo Flow

1. Start Docker:

```bash
docker compose up --build
```

2. Open dashboard:

```text
http://localhost:8000
```

3. Send HTTP test data.

4. Run MQTT simulator.

5. Trigger CRITICAL payload.

6. Show Discord alert.

7. Explain that real ESP32 can continue using `/data`.

8. Explain that standardized API is available at `/api/v1/sensor/readings`.

## 18. Git Safety Notes

Do not commit:

```text
.env
backend/data/*.db
backend/.venv/
backend/ml/*.pkl
*:Zone.Identifier
```

Commit source and docs only.
