import requests
import time
import random

SERVER_URL = "http://localhost:8000/data"
API_KEY = "IOT_SECRET_2026"

def simulate_device():
    print("Starting Production ESP32 Simulator...")
    headers = {"X-API-KEY": API_KEY}
    
    try:
        while True:
            payload = {
                "temperature": round(random.uniform(22.0, 38.0), 1),
                "humidity": round(random.uniform(40.0, 90.0), 1),
                "light": round(random.uniform(50.0, 1000.0), 1),
                "gas": random.randint(400, 3500),
                "noise": random.randint(100, 2000)
            }
            
            try:
                response = requests.post(SERVER_URL, json=payload, headers=headers, timeout=5)
                status = response.json().get('status')
                comfort = response.json().get('comfort')
                print(f"Sent: {payload['temperature']}C | Server Status: {status} | Comfort: {comfort}")
            except Exception as e:
                print(f"Error: {e}")
            
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\nSimulator stopped.")

if __name__ == "__main__":
    simulate_device()
