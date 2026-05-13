# IoT Health & Comfort Monitoring System (Group 9)

An intelligent, real-time ecosystem designed to monitor indoor environmental quality and assess human comfort levels using a Hybrid AI-Rule-Base Engine.

---

## 🚀 Overview

This project implements a complete End-to-End (E2E) IoT solution. It captures environmental data (Temperature, Humidity, Air Quality, Light, and Noise) at the **Edge**, processes it via a **Centralized Hybrid Engine**, and provides actionable insights through a **Web Dashboard** and **Mobile Application**.

### The Core Goal

To provide a proactive health monitoring system that not only displays data but intelligently predicts "Comfort Levels" (Good, Warning, Critical) to mitigate environmental health risks.

---

## 🛠 System Architecture

The system follows a decentralized sensing, centralized processing architecture:

1.  **Edge Layer (ESP32)**:
    - Autonomous sensor data acquisition.
    - Local alert triggers (LED/Buzzer).
    - Dynamic network configuration via WiFiManager.
    - mDNS-based backend discovery.
2.  **Logic Layer (Modular FastAPI & Hybrid AI)**:
    - **Modular Architecture**: Separated concerns (Routers, Services, Schemas) for enterprise-grade maintainability.
    - **Hybrid Engine**: Combines deterministic logic (Edge safety) with machine learning (RandomForest) for comfort assessment.
    - **Alerting**: Integrated Discord Webhooks for real-time critical notifications.
    - **Broker**: Built-in MQTT support via Mosquitto for low-latency IoT communication.
3.  **Presentation Layer**:
    - **Web Dashboard (Modern UI)**: High-premium, responsive design with dark mode and non-blocking health monitoring.
    - **Mobile App**: Capacitor-based hybrid application for cross-platform access.

---

## 📡 Technology Stack

| Component     | Technology                                | Role                                  |
| :------------ | :---------------------------------------- | :------------------------------------ |
| **Firmware**  | C++ (Arduino/ESP32), WiFiManager, ESPmDNS | Edge Sensing & Watchdog               |
| **Backend**   | Python (FastAPI), Requests, Paho-MQTT     | Modular API & Notification Engine     |
| **AI/ML**     | Scikit-learn (RandomForest), Pandas       | Comfort Level Prediction (3 features) |
| **Messaging** | Mosquitto (MQTT), Discord Webhooks        | Alerting & Pub/Sub Connectivity       |
| **Database**  | SQLite 3                                  | Lightweight Relational Storage        |

---

## 📚 Project Documentation & Thesis

- **[BaoCao.md](./BaoCao.md)**: The comprehensive scientific thesis detailing sensor physics, system architecture, and AI performance metrics.
- **[docs/](./docs/)**: Contains API contracts, edge logic rules, and deployment runbooks.

---

## 📐 Hardware Specifications (BOM)

- **Microcontroller**: ESP32 DevKit V1
- **Sensors**:
  - **DHT22**: Temperature & Humidity
  - **MQ135**: Air Quality (Gas/CO₂)
  - **BH1750**: Ambient Light (Lux)
  - **MAX4466**: Sound/Noise Level
- **Actuators**: 5V Buzzer, LED (Status Indicators)

---

## ⚙️ Getting Started

### 1. Local Development (Docker)

The easiest way to run the full stack (FastAPI + MQTT) is using Docker:

1.  Navigate to the root directory.
2.  Configure `.env` (API Keys, Dashboard Token, Discord Webhooks).
3.  Start the stack: `docker compose up -d --build`.

### 2. Manual Backend Setup (No Docker)

1.  Navigate to `/backend`.
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Run the application: `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

### 3. Cloud Deployment (Azure)

To deploy the 24/7 production stack to your Azure VM:

1.  Navigate to the root directory.
2.  Run the management script: `./deploy_iot.ps1 deploy`.
3.  Monitor logs: `./deploy_iot.ps1 logs`.

### 4. Mobile App (Android)

The Android app is a lightweight wrapper that opens the **same web dashboard** URL inside the app.

**Default dashboard URL (currently hardcoded for demo):**

- `http://20.212.105.13:8000/?token=IoT_Health`

**Build APK (debug):**

1. Navigate to `/mobile`.
2. Install dependencies: `npm install`.
3. Sync Capacitor Android project: `npx cap sync android`.
4. Build debug APK:
   - `cd android && ./gradlew assembleDebug`
5. Output APK:
   - `mobile/android/app/build/outputs/apk/debug/app-debug.apk`

**Install to a real device:**

1. Enable Developer Options + USB debugging on your phone.
2. Connect via USB and verify: `adb devices -l`.
3. Install/update APK: `adb install -r mobile/android/app/build/outputs/apk/debug/app-debug.apk`.

**If you deploy to a different backend host/token:**

- Update the default URL/token in `mobile/www/index.html`.
- Update allowed navigation host in `mobile/capacitor.config.json` (Capacitor WebView navigation allowlist).

**Android HTTP note (testing only):**

- The project currently allows cleartext HTTP traffic (for demo/testing). For production, use HTTPS/TLS.

---

## 🤝 Teammate Handover & Access

Share the following details with your team to enable remote monitoring:

- **Public Dashboard**: `http://20.212.105.13:8000/?token=IoT_Health`
- **MQTT Broker**: `20.212.105.13:1883`
- **Discord Notifications**: Ensure the `DISCORD_WEBHOOK_URL` is set to receive push alerts.

**Security note:**

- The dashboard uses a token in the URL query string. Anyone who has the link+token can access it.

---

## 📈 Project Status:

- [x] **Modular Architecture**: Transitioned from monolithic to scalable microservice style.
- [x] **Hybrid AI Engine**: RandomForest ML integrated with edge rule safety.
- [x] **Cloud Reliability**: Azure VM (24/7), Docker recovery, and Hardware Watchdog.
- [x] **UX Hardening**: Non-blocking dashboard UI with dual Server/Device health badges.
- [x] **Mobile Strategy & Testing**: Capacitor-based hybrid app with structured testing workflows.
- [x] **Scientific Documentation**: Finalized the comprehensive academic-grade thesis (`BaoCao.md`).

---

## 👥 Team & Contributions

- **Member 1**: Hardware Design & Assembly.
- **Member 2**: Embedded Systems & Edge Logic.
- **Member 3**: AI/ML Modeling & Hybrid Engine.
- **Member 4**: Backend API & Web Infrastructure.
- **Member 5**: Mobile App Development.
