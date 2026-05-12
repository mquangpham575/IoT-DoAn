# ESP32 Backend Integration Note

## 1. Do not overwrite teammate firmware

The current firmware file should not be overwritten unless the firmware owner agrees.

This backend is designed to be compatible with the existing firmware endpoint:

```text
POST /data
```

## 2. Minimum change required in firmware

If the old firmware already sends data to:

```text
http://<PC_LAN_IP>:8000/data
```

then no API migration is required.

Only make sure:

- backend IP is correct
- API key is correct
- JSON payload contains required sensor values

## 3. Optional future upgrade

When the team wants to standardize API naming, firmware can switch to:

```text
http://<PC_LAN_IP>:8000/api/v1/sensor/readings
```

This is optional and not required for the current integration test.

## 4. Recommended communication to firmware teammate

Backend đã giữ endpoint `/data` để tương thích với firmware hiện tại. Bạn không cần đổi API ngay. Chỉ cần đảm bảo ESP32 gửi được dữ liệu về đúng IP backend và nhận HTTP 200 là dashboard/alert sẽ hoạt động.
