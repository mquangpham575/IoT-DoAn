import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Tạo dữ liệu giả lập (Synthetic Dataset)
def generate_data(n=1000):
    np.random.seed(42)
    temp = np.random.uniform(20, 45, n)
    humid = np.random.uniform(30, 95, n)
    gas = np.random.uniform(300, 4000, n)
    
    # Labeling logic: 0: Good, 1: Warning, 2: Danger
    labels = []
    for t, h, g in zip(temp, humid, gas):
        if g > 3000 or (t > 38 and h > 85):
            labels.append(2) # Danger
        elif g > 2000 or t > 35 or h > 80:
            labels.append(1) # Warning
        else:
            labels.append(0) # Good
            
    return pd.DataFrame({'temp': temp, 'humid': humid, 'gas': gas, 'label': labels})

# 2. Huấn luyện mô hình
print("Generating data and training model...")
df = generate_data()
X = df[['temp', 'humid', 'gas']]
y = df['label']

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# 3. Xuất mô hình
joblib.dump(model, 'comfort_model.pkl')
print("Model saved as comfort_model.pkl")

# Kiểm tra thử
test_data = [[28.0, 50.0, 500]] # Lý tưởng
prediction = model.predict(test_data)
print(f"Test Prediction (Ideal): {prediction[0]}") # Expected: 0
