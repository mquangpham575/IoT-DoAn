#include <Wire.h>
#include <BH1750.h>
#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ESPmDNS.h>
#include <WiFiManager.h>
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
WiFiManager wm;

// =========================
// Cấu hình & Biến hệ thống
// =========================
String serverUrl = "";
const char* apiKey = "IOT_SECRET_2026";
const char* azureServerIp = "20.212.105.13"; // Azure VM Public IP
unsigned long lastUpdate = 0;
const long updateInterval = 5000; // Gửi dữ liệu mỗi 5 giây

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

// INTENT: Resolve the backend server IP using mDNS discovery or Cloud fallback.
void resolveServerIP() {
  Serial.println("[NET] Discovering iot-server.local...");
  int n = MDNS.queryService("http", "tcp");
  if (n > 0) {
    String ip = MDNS.address(0).toString();
    int port = MDNS.port(0);
    serverUrl = "http://" + ip + ":" + String(port) + "/data";
    Serial.print("[NET] Local server found: ");
    Serial.println(serverUrl);
  } else {
    Serial.println("[NET] Local discovery failed. Falling back to Azure Cloud...");
    serverUrl = "http://" + String(azureServerIp) + ":8000/data";
    Serial.print("[NET] Cloud server set: ");
    Serial.println(serverUrl);
  }
}

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

  if (!isnan(temperature) && temperature > tempThreshold) alert = true;
  if (!isnan(humidity) && humidity > humidityThreshold) alert = true;
  if (gasValue > gasThreshold) alert = true;
  if (soundValue > soundThreshold) alert = true;
  if (lux < lightThreshold) alert = true;

  return alert;
}

// INTENT: Construct a JSON payload and transmit sensor data to the backend server via HTTP POST.
void sendDataToServer() {
  if (WiFi.status() == WL_CONNECTED && serverUrl != "") {
    if (isnan(temperature) || isnan(humidity)) return;

    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("X-API-KEY", apiKey);

    String jsonPayload = "{";
    jsonPayload += "\"temperature\":" + String(temperature) + ",";
    jsonPayload += "\"humidity\":" + String(humidity) + ",";
    jsonPayload += "\"gas\":" + String(gasValue) + ",";
    jsonPayload += "\"light\":" + String(lux) + ",";
    jsonPayload += "\"noise\":" + String(soundValue);
    jsonPayload += "}";

    int httpResponseCode = http.POST(jsonPayload);
    Serial.print("[HTTP] Response: ");
    Serial.println(httpResponseCode);
    http.end();
  } else if (serverUrl == "") {
    resolveServerIP();
  }
}

// INTENT: Handle physical alert indicators (LED/Buzzer) based on system alert state.
void controlDevices(bool alert) {
  if (alert) {
    digitalWrite(LED_PIN, HIGH);
    tone(BUZZER_PIN, 2000, 100);
  } else {
    digitalWrite(LED_PIN, LOW);
    noTone(BUZZER_PIN);
  }
}

// INTENT: Configure hardware pins, initialize libraries, and handle dynamic WiFi/mDNS setup.
void setup() {
  Serial.begin(115200);

  // WDT Config
  dht.begin();
  Wire.begin(21, 22);
  lightMeter.begin();

  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  // WiFiManager: AutoConnect with a captive portal
  Serial.println("[SYS] Starting WiFiManager...");
  wm.setConfigPortalTimeout(60); // Start portal if no connection after 60s
  if (!wm.autoConnect("ESP32-Health-Monitor")) {
    Serial.println("[SYS] Failed to connect and hit timeout");
    ESP.restart();
  }

  // mDNS Setup
  if (!MDNS.begin("esp32-sensor")) {
    Serial.println("[SYS] Error setting up MDNS responder!");
  }
  
  resolveServerIP();
  
  // Initialize Watchdog ONLY after successful connection
  esp_task_wdt_config_t wdt_config = {
      .timeout_ms = 15000,
      .idle_core_mask = 0,
      .trigger_panic = true,
  };
  esp_task_wdt_init(&wdt_config);
  esp_task_wdt_add(NULL);

  Serial.println("[SYS] Initialization Complete.");
}

// INTENT: Execute the main program cycle using non-blocking timing.
void loop() {
  esp_task_wdt_reset();
  
  unsigned long currentMillis = millis();

  // Read sensors continuously for real-time alerts
  readSensors();
  controlDevices(checkAlert());

  // Send data at defined intervals
  if (currentMillis - lastUpdate >= updateInterval) {
    lastUpdate = currentMillis;
    printSensorData();
    sendDataToServer();
  }
}
