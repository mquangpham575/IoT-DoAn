# Edge Logic Rules - IoT Health Monitoring System

## 1. Mục tiêu

Edge Logic dùng để đánh giá trạng thái môi trường dựa trên dữ liệu cảm biến.

Trong project này, Edge Logic được triển khai ở Backend để xử lý dữ liệu từ ESP32 hoặc simulator. ESP32 vẫn có thể xử lý cảnh báo cục bộ bằng LED/Buzzer, nhưng kết quả đánh giá chính được tính tại Backend.

Backend sẽ tạo ra các thông tin sau:

- `comfort_level`
- `status_label`
- `risk_score`
- `reasons`
- `recommendation`

## 2. Input sensors

| Sensor value | Description |
|---|---|
| `temperature` | Nhiệt độ môi trường, đơn vị °C |
| `humidity` | Độ ẩm môi trường, đơn vị % |
| `gas` | Chỉ số khí hoặc chất lượng không khí |
| `light` | Cường độ ánh sáng, đơn vị lux |
| `noise` | Chỉ số tiếng ồn hoặc raw value |

## 3. Output fields

| Field | Type | Description |
|---|---|---|
| `comfort_level` | integer | Mức đánh giá: 0, 1, 2 |
| `status_label` | string | `NORMAL`, `WARNING`, hoặc `CRITICAL` |
| `risk_score` | integer | Điểm rủi ro từ 0 đến 100 |
| `reasons` | list[string] | Danh sách nguyên nhân gây cảnh báo |
| `recommendation` | string | Khuyến nghị xử lý |

## 4. Status levels

| Level | Label | Meaning |
|---:|---|---|
| 0 | `NORMAL` | Môi trường ổn định |
| 1 | `WARNING` | Có chỉ số vượt ngưỡng, cần chú ý |
| 2 | `CRITICAL` | Có rủi ro cao, cần xử lý ngay |

## 5. Suggested thresholds

Các ngưỡng dưới đây dùng cho giai đoạn demo và có thể hiệu chỉnh sau khi có dữ liệu cảm biến thật.

### 5.1. Temperature

| Condition | Level | Reason |
|---|---:|---|
| `temperature <= 35` | 0 | Normal temperature |
| `35 < temperature <= 40` | 1 | High temperature |
| `temperature > 40` | 2 | Critical temperature |

### 5.2. Humidity

| Condition | Level | Reason |
|---|---:|---|
| `humidity <= 85` | 0 | Normal humidity |
| `85 < humidity <= 95` | 1 | High humidity |
| `humidity > 95` | 2 | Critical humidity |

### 5.3. Gas

| Condition | Level | Reason |
|---|---:|---|
| `gas <= 2000` | 0 | Normal air quality |
| `2000 < gas <= 3000` | 1 | Poor air quality |
| `gas > 3000` | 2 | Critical gas level |

### 5.4. Light

| Condition | Level | Reason |
|---|---:|---|
| `light >= 100` | 0 | Normal light level |
| `10 <= light < 100` | 1 | Low light level |
| `light < 10` | 1 | Very low light level |

Trong demo này, ánh sáng thấp thường chỉ nên là `WARNING`, không nên tự động đẩy lên `CRITICAL` trừ khi kết hợp với nhiều chỉ số khác.

### 5.5. Noise

| Condition | Level | Reason |
|---|---:|---|
| `noise <= 2000` | 0 | Normal noise level |
| `2000 < noise <= 3000` | 1 | High noise level |
| `noise > 3000` | 1 | Very high noise level |

Tương tự ánh sáng, tiếng ồn cao thường là yếu tố gây khó chịu hơn là nguy hiểm tức thời, nên trong demo nên ưu tiên mức `WARNING`.

## 6. Risk score calculation

Risk score nằm trong khoảng từ 0 đến 100.

Cách tính đề xuất:

```text
risk_score = base_score + temperature_score + humidity_score + gas_score + light_score + noise_score + combination_penalty
```

Trong đó:

| Component | Suggested score |
|---|---:|
| Base score | 10 |
| Temperature warning | +15 |
| Temperature critical | +30 |
| Humidity warning | +10 |
| Humidity critical | +20 |
| Gas warning | +25 |
| Gas critical | +45 |
| Low light | +5 |
| High noise | +10 |
| Multiple warning penalty | +10 |
| Any critical penalty | +15 |

Sau khi tính xong:

```text
risk_score = min(risk_score, 100)
```

## 7. Final status decision

Final status nên được xác định theo nguyên tắc thận trọng:

```text
Nếu có ít nhất một chỉ số critical:
    status_label = CRITICAL
Ngược lại nếu có ít nhất một chỉ số warning:
    status_label = WARNING
Ngược lại:
    status_label = NORMAL
```

Ngoài ra, nếu có từ 3 chỉ số warning trở lên, có thể nâng mức lên `CRITICAL` vì môi trường có nhiều yếu tố xấu cùng lúc.

## 8. Recommendation rules

### 8.1. Normal

```text
Môi trường hiện tại ổn định. Tiếp tục theo dõi định kỳ.
```

### 8.2. High temperature

```text
Nhiệt độ đang cao. Nên bật quạt, điều hòa hoặc tăng thông gió trong phòng.
```

### 8.3. High humidity

```text
Độ ẩm đang cao. Nên bật máy hút ẩm hoặc tăng lưu thông không khí.
```

### 8.4. Poor air quality

```text
Chất lượng không khí có dấu hiệu xấu. Nên mở cửa, bật quạt thông gió hoặc kiểm tra nguồn khí bất thường.
```

### 8.5. Low light

```text
Ánh sáng đang thấp. Nên bổ sung ánh sáng để cải thiện điều kiện sinh hoạt hoặc làm việc.
```

### 8.6. High noise

```text
Mức tiếng ồn đang cao. Nên kiểm tra nguồn gây ồn hoặc giảm thiết bị phát âm thanh trong khu vực.
```

### 8.7. Critical

```text
Môi trường có rủi ro cao. Cần kiểm tra khu vực ngay và xử lý các nguồn gây nguy hiểm.
```

## 9. Example

### Input

```json
{
  "device_id": "esp32_01",
  "temperature": 37.5,
  "humidity": 88.0,
  "gas": 2600,
  "light": 80,
  "noise": 1800
}
```

### Output

```json
{
  "comfort_level": 1,
  "status_label": "WARNING",
  "risk_score": 75,
  "reasons": [
    "High temperature",
    "High humidity",
    "Poor air quality",
    "Low light level"
  ],
  "recommendation": "Môi trường có nhiều chỉ số cần chú ý. Nên tăng thông gió, giảm nhiệt độ và kiểm tra chất lượng không khí."
}
```

## 10. Notes

Các rule trên chỉ là baseline cho giai đoạn demo. Sau khi có thiết bị thật, nhóm cần đo dữ liệu thực tế để hiệu chỉnh ngưỡng cho phù hợp với cảm biến và môi trường đo.
