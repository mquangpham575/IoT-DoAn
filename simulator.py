import requests
import time
import random

SERVER_URL = "http://localhost:8000/data"

def simulate_device():
    print("Starting ESP32 Simulator...")
    print(f"Target Server: {SERVER_URL}")
    
    try:
        while True:
            # Giả lập dữ liệu từ các cảm biến
            payload = {
                "temperature": round(random.uniform(25.0, 40.0), 1),
                "humidity": round(random.uniform(40.0, 90.0), 1),
                "light": round(random.uniform(10.0, 500.0), 1),
                "gas": random.randint(300, 3000),
                "noise": random.randint(100, 2000)
            }
            
            try:
                response = requests.post(SERVER_URL, json=payload, timeout=2)
                print(f"Sent: {payload} | Server Response: {response.json().get('edge_status')}")
            except requests.exceptions.RequestException as e:
                print(f"Connection Error: {e}")
            
            time.sleep(5) # Gửi 5 giây 1 lần như code INO
            
    except KeyboardInterrupt:
        print("\nSimulator stopped.")

if __name__ == "__main__":
    simulate_device()
