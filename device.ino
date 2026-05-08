#include <WiFi.h>
#include <HTTPClient.h>
#include <ESPmDNS.h>
#include <ArduinoJson.h> 
#include <Wire.h>
#include <BH1750.h>
#include <DHT.h>

// ==========================================
// CONFIGURATION
// ==========================================
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl = "http://YOUR_SERVER_IP:8000/data";
const char* deviceName = "iot-health-monitor";

#define DHTPIN 4
#define DHTTYPE DHT22
#define MQ135_PIN 34
#define SOUND_PIN 35
#define BUZZER_PIN 18
#define LED_PIN 19

const unsigned long SENSOR_INTERVAL = 5000;
const unsigned long SOUND_WINDOW = 50;

// ==========================================
// GLOBALS
// ==========================================
DHT dht(DHTPIN, DHTTYPE);
BH1750 lightMeter;
unsigned long lastSensorRead = 0;

struct SensorData {
  float temp;
  float humid;
  float lux;
  int gas;
  int noise;
} data;

// ==========================================
// SENSOR PROCESSING
// ==========================================
int readNoiseLevel() {
  unsigned int peakToPeak = 0;
  unsigned int signalMax = 0;
  unsigned int signalMin = 4095;
  unsigned long startMillis = millis();

  while (millis() - startMillis < SOUND_WINDOW) {
    int sample = analogRead(SOUND_PIN);
    if (sample > signalMax) signalMax = sample;
    else if (sample < signalMin) signalMin = sample;
  }
  return signalMax - signalMin;
}

void collectData() {
  data.temp = dht.readTemperature();
  data.humid = dht.readHumidity();
  data.lux = lightMeter.readLightLevel();
  data.gas = analogRead(MQ135_PIN); 
  data.noise = readNoiseLevel();
}

// ==========================================
// EDGE LOGIC & AI
// ==========================================
bool applyRuleBase() {
  bool isAlert = false;
  if (data.gas > 2000) isAlert = true;
  if (data.noise > 1500) isAlert = true;
  if (data.temp > 35.0 || data.humid > 85.0) isAlert = true;
  return isAlert;
}

void executeAction(bool alert) {
  if (alert) {
    digitalWrite(LED_PIN, HIGH);
    tone(BUZZER_PIN, 1000, 200);
  } else {
    digitalWrite(LED_PIN, LOW);
    noTone(BUZZER_PIN);
  }
}

// ==========================================
// COMMUNICATION
// ==========================================
void sendToServer() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<200> doc;
    doc["temperature"] = data.temp;
    doc["humidity"] = data.humid;
    doc["light"] = data.lux;
    doc["gas"] = data.gas;
    doc["noise"] = data.noise;

    String jsonPayload;
    serializeJson(doc, jsonPayload);
    
    int httpResponseCode = http.POST(jsonPayload);
    Serial.printf("HTTP Response code: %d\n", httpResponseCode);
    http.end();
  }
}

// ==========================================
// MAIN SETUP & LOOP
// ==========================================
void setup() {
  Serial.begin(115200);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  dht.begin();
  Wire.begin(21, 22);
  lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected!");

  if (MDNS.begin(deviceName)) {
    Serial.println("mDNS responder started");
  }
}

void loop() {
  if (millis() - lastSensorRead >= SENSOR_INTERVAL) {
    lastSensorRead = millis();
    collectData();
    bool alert = applyRuleBase();
    executeAction(alert);
    sendToServer();
  }
}
