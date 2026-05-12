# Real Device Test Checklist

## 1. Hardware

- [ ] ESP32 powers on
- [ ] DHT22 connected correctly
- [ ] MQ135 connected correctly
- [ ] BH1750 connected through I2C
- [ ] MAX4466 connected correctly
- [ ] LED connected correctly
- [ ] Buzzer connected correctly
- [ ] All components share common GND

## 2. Backend

- [ ] `docker compose up --build` runs successfully
- [ ] Backend is available at `http://localhost:8000`
- [ ] Dashboard opens successfully
- [ ] `GET /api/v1/system/health` returns `status: ok`
- [ ] MQTT broker is running if MQTT demo is needed
- [ ] Discord webhook is configured if alert demo is needed

## 3. Firmware Configuration

- [ ] WiFi SSID is correct
- [ ] WiFi password is correct
- [ ] `serverUrl` points to PC/Laptop LAN IP
- [ ] `serverUrl` uses `/data` or `/api/v1/sensor/readings`
- [ ] API key matches backend configuration
- [ ] Serial Monitor baud rate is 115200

## 4. Integration Test

- [ ] ESP32 connects to WiFi
- [ ] Serial Monitor shows ESP32 local IP
- [ ] ESP32 prints sensor values
- [ ] ESP32 sends HTTP POST request
- [ ] HTTP response code is 200
- [ ] Dashboard shows new reading
- [ ] Risk score updates correctly
- [ ] Recommendation appears
- [ ] Discord alert is sent when status is WARNING or CRITICAL

## 5. Evidence for report

- [ ] Screenshot of Serial Monitor showing HTTP 200
- [ ] Screenshot of dashboard receiving real ESP32 data
- [ ] Screenshot of Discord alert
- [ ] Exported CSV from dashboard
- [ ] Short demo video showing device and dashboard update
