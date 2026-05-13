# Real Device Troubleshooting Guide

## 1. ESP32 cannot connect to WiFi

Check:

- SSID/password are correct.
- ESP32 is close enough to router.
- WiFi is 2.4 GHz. Many ESP32 boards do not support 5 GHz.
- Try using a phone hotspot for quick validation.

## 2. ESP32 connects to WiFi but cannot send data

Check:

- Firmware must not use `localhost`.
- Use PC/Laptop LAN IP.
- ESP32 and backend must be on the same network.
- Backend must be running.
- Port 8000 must be reachable.
- Windows Firewall may block inbound connections.

Test backend from another device in the same WiFi:

```text
http://<PC_LAN_IP>:8000/api/v1/system/health
```

## 3. HTTP response is 403

Cause:

- API key is missing or incorrect.

Check firmware header:

```text
X-API-KEY: IOT_SECRET_2026
```

## 4. HTTP response is 422

Cause:

- Payload field names or values do not match backend schema.

Required fields:

```text
temperature
humidity
gas
light
noise
```

Optional but recommended:

```text
device_id
```

## 5. Dashboard does not update

Check:

```bash
curl http://localhost:8000/api/v1/sensor/history?limit=5
```

If API has data but dashboard does not update:

- Refresh browser.
- Check browser console.
- Confirm dashboard is opening the same backend.

## 6. Discord does not send alert

Check `.env`:

```env
ENABLE_DISCORD_ALERT=true
DISCORD_WEBHOOK_URL=your_webhook_url
ALERT_COOLDOWN_SECONDS=60
```

Also note:

- Discord alert is only sent for WARNING or CRITICAL.
- Cooldown prevents repeated spam from the same device/status.
