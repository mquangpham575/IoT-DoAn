import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Tạo dữ liệu giả lập (Synthetic Dataset) với 5 cảm biến và logic phi tuyến tính
def generate_data(n=2000):
    np.random.seed(42)
    temp = np.random.uniform(15, 45, n)
    humid = np.random.uniform(20, 95, n)
    gas = np.random.uniform(300, 4000, n)
    light = np.random.uniform(0, 1000, n)
    noise = np.random.uniform(100, 3500, n)
    
    labels = []
    for t, h, g, l, ns in zip(temp, humid, gas, light, noise):
        # Trọng số tính điểm phạt cơ bản
        score = 0
        
        # 1. Tương tác Nhiệt - Ẩm (Compound Heat-Humidity index)
        if t > 33 and h > 70:
            score += 35  # Nóng ẩm oi bức cực kỳ khó chịu
        elif t > 35:
            score += 20
        elif t < 18:
            score += 10
            
        if h > 85:
            score += 15
        elif h < 30:
            score += 8
            
        # 2. Khí độc / Chất lượng không khí (MQ135)
        if g > 3000:
            score += 45
        elif g > 1500:
            score += 20
            
        # 3. Tiếng ồn
        if ns > 2500:
            score += 20
        elif ns > 1500:
            score += 10
            
        # 4. Thiếu ánh sáng
        if l < 30:
            score += 15
        elif l < 80:
            score += 8
            
        # 5. Thêm biến động ngẫu nhiên (simulating subjective human feedback variance)
        score += np.random.normal(0, 10)
        
        # Phân loại nhãn cuối cùng
        if score >= 65:
            labels.append(2)  # Danger/Critical
        elif score >= 30:
            labels.append(1)  # Warning
        else:
            labels.append(0)  # Normal
            
    return pd.DataFrame({
        'temp': temp,
        'humid': humid,
        'gas': gas,
        'light': light,
        'noise': noise,
        'label': labels
    })

# 2. Huấn luyện mô hình
print("Generating 5-feature dataset and training RandomForest model...")
df = generate_data()
X = df[['temp', 'humid', 'gas', 'light', 'noise']]
y = df['label']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 3. Xuất mô hình
joblib.dump(model, 'comfort_model.pkl')
print("Model saved as comfort_model.pkl")

# Kiểm tra thử
test_data = [[28.0, 50.0, 500, 400.0, 300]]  # Điều kiện lý tưởng
prediction = model.predict(test_data)
print(f"Test Prediction (Ideal Environment): {prediction[0]}")  # Expected: 0
