import json
import os
import random
import time

import paho.mqtt.client as mqtt


MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_PUBLISH_TOPIC", "iot/esp32_01/sensor")
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


def main() -> None:
    client = mqtt.Client()
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_start()

    print("Starting MQTT ESP32 Simulator...")
    print(f"Broker: {MQTT_HOST}:{MQTT_PORT}")
    print(f"Topic: {MQTT_TOPIC}")

    try:
        while True:
            payload = generate_payload()
            client.publish(MQTT_TOPIC, json.dumps(payload), qos=0)
            print(f"Published: {payload}")
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nMQTT simulator stopped.")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
