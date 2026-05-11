#include <Wire.h>
#include <BH1750.h>
#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <esp_task_wdt.h>

// =========================
// Khai báo chân kết nối
// =========================
#define DHTPIN 4
#define DHTTYPE DHT22

#define MQ135_PIN 34
#define SOUND_PIN 35

#define BUZZER_PIN 18
#define LED_PIN 19

// =========================
// Khởi tạo đối tượng
// =========================
DHT dht(DHTPIN, DHTTYPE);
BH1750 lightMeter;

// =========================
// Cấu hình WiFi & Server
// =========================
const char* ssid = "iot-nhom9";
const char* password = "12345678";
const char* serverUrl = "http://10.0.88.218:8000/data";
const char* apiKey = "IOT_SECRET_2026";

// =========================
// Biến lưu dữ liệu cảm biến
// =========================
float temperature = 0;
float humidity = 0;
float lux = 0;
int gasValue = 0;
int soundValue = 0;

// =========================
// Ngưỡng cảnh báo
// =========================
float tempThreshold = 35.0;
float humidityThreshold = 85.0;
int gasThreshold = 2500;
int soundThreshold = 2500;
float lightThreshold = 20.0;

// INTENT: Read physical values from all connected sensors into global variables.
void readSensors() {
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  gasValue = analogRead(MQ135_PIN);
  lux = lightMeter.readLightLevel();
  soundValue = analogRead(SOUND_PIN);
}

// INTENT: Print all current sensor readings to the Serial terminal for debugging.
void printSensorData() {
  Serial.print("[DATA] ");
  Serial.print("T:"); Serial.print(temperature, 1); Serial.print("C | ");
  Serial.print("H:"); Serial.print(humidity, 1); Serial.print("% | ");
  Serial.print("G:"); Serial.print(gasValue); Serial.print("ppm | ");
  Serial.print("L:"); Serial.print(lux, 1); Serial.print("lux | ");
  Serial.print("N:"); Serial.println(soundValue);
}

// INTENT: Evaluate sensor values against thresholds and return an alert status.
bool checkAlert() {
  bool alert = false;

  if (!isnan(temperature) && temperature > tempThreshold) {
    Serial.println("[WARN] Nhiet do cao");
    alert = true;
  }

  if (!isnan(humidity) && humidity > humidityThreshold) {
    Serial.println("[WARN] Do am cao");
    alert = true;
  }

  if (gasValue > gasThreshold) {
    Serial.println("[ALERT] Nong do gas cao");
    alert = true;
  }

  if (soundValue > soundThreshold) {
    Serial.println("[WARN] Tieng on lon");
    alert = true;
  }

  if (lux < lightThreshold) {
    Serial.println("[WARN] Moi truong qua toi");
    alert = true;
  }

  return alert;
}

// INTENT: Initialize and maintain the WiFi connection with a retry mechanism.
void connectToWiFi() {
  Serial.print("[NET] Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("\n[NET] Connected. IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[NET] Connection Failed.");
  }
}

// INTENT: Construct a JSON payload and transmit sensor data to the backend server via HTTP POST.
void sendDataToServer() {
  if (WiFi.status() == WL_CONNECTED) {
    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("[ERR] Invalid sensor data.");
      return;
    }

    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("X-API-KEY", apiKey);

    // Tạo chuỗi JSON
    String jsonPayload = "{";
    jsonPayload += "\"temperature\":" + String(isnan(temperature) ? 0 : temperature) + ",";
    jsonPayload += "\"humidity\":" + String(isnan(humidity) ? 0 : humidity) + ",";
    jsonPayload += "\"gas\":" + String(gasValue) + ",";
    jsonPayload += "\"light\":" + String(lux) + ",";
    jsonPayload += "\"noise\":" + String(soundValue);
    jsonPayload += "}";

    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      Serial.print("[HTTP] POST Success: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("[HTTP] POST Failed: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("[NET] WiFi lost. Reconnecting...");
    connectToWiFi();
  }
}

// INTENT: Handle physical alert indicators (LED/Buzzer) based on system alert state.
void controlDevices(bool alert) {
  if (alert) {
    digitalWrite(LED_PIN, HIGH);

    tone(BUZZER_PIN, 2000);
    delay(300);
    noTone(BUZZER_PIN);
  } else {
    digitalWrite(LED_PIN, LOW);
    noTone(BUZZER_PIN);
  }
}

// INTENT: Configure hardware pins, initialize sensor libraries, and establish initial network connection.
void setup() {
  Serial.begin(115200);

  // Initialize Watchdog Timer (10 seconds) for ESP32 Core 3.x
  esp_task_wdt_config_t wdt_config = {
      .timeout_ms = 10000,
      .idle_core_mask = 0,
      .trigger_panic = true,
  };
  esp_task_wdt_init(&wdt_config);
  esp_task_wdt_add(NULL);

  dht.begin();

  Wire.begin(21, 22);
  lightMeter.begin();

  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  digitalWrite(BUZZER_PIN, LOW);
  digitalWrite(LED_PIN, LOW);

  connectToWiFi();

  Serial.println("[SYS] System Initialized.");
}

// INTENT: Execute the main program cycle: read, print, check alerts, and transmit data.
void loop() {
  esp_task_wdt_reset(); // Reset Watchdog timer
  readSensors();

  printSensorData();

  bool alert = checkAlert();

  controlDevices(alert);

  sendDataToServer();

  delay(2000);
}
