import os
import random
import time

import requests


SERVER_URL = os.getenv("SIMULATOR_SERVER_URL", "http://localhost:8000/api/v1/sensor/readings")
API_KEY = os.getenv("IOT_API_KEY", "IOT_SECRET_2026")
DEVICE_ID = os.getenv("SIMULATOR_DEVICE_ID", "esp32_01")


def generate_payload() -> dict:
    return {
        "device_id": DEVICE_ID,
        "temperature": round(random.uniform(22.0, 39.5), 1),
        "humidity": round(random.uniform(40.0, 92.0), 1),
        "light": round(random.uniform(5.0, 1000.0), 1),
        "gas": random.randint(400, 3400),
        "noise": random.randint(100, 3200),
    }


def simulate_device() -> None:
    print("Starting HTTP ESP32 Simulator...")
    print(f"Target: {SERVER_URL}")

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": API_KEY,
    }

    try:
        while True:
            payload = generate_payload()

            try:
                response = requests.post(SERVER_URL, json=payload, headers=headers, timeout=5)
                response.raise_for_status()
                body = response.json()
                data = body.get("data", {})
                print(
                    f"Sent {payload['device_id']} | "
                    f"T={payload['temperature']}C | "
                    f"Gas={payload['gas']} | "
                    f"Status={data.get('status_label')} | "
                    f"Risk={data.get('risk_score')}"
                )
            except Exception as exc:
                print(f"HTTP simulator error: {exc}")

            time.sleep(3)

    except KeyboardInterrupt:
        print("\nSimulator stopped.")


if __name__ == "__main__":
    simulate_device()
