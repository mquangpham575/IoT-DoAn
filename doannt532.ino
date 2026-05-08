#include <Wire.h>
#include <BH1750.h>
#include <DHT.h>

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

void readSensors() {
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  gasValue = analogRead(MQ135_PIN);
  lux = lightMeter.readLightLevel();
  soundValue = analogRead(SOUND_PIN);
}

void printSensorData() {
  Serial.println("==============================");
  Serial.println("DU LIEU CAM BIEN HIEN TAI");
  Serial.println("==============================");

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("DHT22: Loi doc du lieu");
  } else {
    Serial.print("Nhiet do: ");
    Serial.print(temperature);
    Serial.println(" °C");

    Serial.print("Do am: ");
    Serial.print(humidity);
    Serial.println(" %");
  }

  Serial.print("Gia tri MQ135: ");
  Serial.println(gasValue);

  Serial.print("Do sang BH1750: ");
  Serial.print(lux);
  Serial.println(" lux");

  Serial.print("Do on MAX4466: ");
  Serial.println(soundValue);
}

bool checkAlert() {
  bool alert = false;

  if (!isnan(temperature) && temperature > tempThreshold) {
    Serial.println("[CANH BAO] Nhiet do cao");
    alert = true;
  }

  if (!isnan(humidity) && humidity > humidityThreshold) {
    Serial.println("[CANH BAO] Do am cao");
    alert = true;
  }

  if (gasValue > gasThreshold) {
    Serial.println("[CANH BAO] Nong do gas cao");
    alert = true;
  }

  if (soundValue > soundThreshold) {
    Serial.println("[CANH BAO] Tieng on lon");
    alert = true;
  }

  if (lux < lightThreshold) {
    Serial.println("[CANH BAO] Moi truong qua toi");
    alert = true;
  }

  return alert;
}

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

void setup() {
  Serial.begin(115200);

  dht.begin();

  Wire.begin(21, 22);
  lightMeter.begin();

  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  digitalWrite(BUZZER_PIN, LOW);
  digitalWrite(LED_PIN, LOW);

  Serial.println("He thong giam sat moi truong bat dau...");
}

void loop() {
  readSensors();

  printSensorData();

  bool alert = checkAlert();

  controlDevices(alert);

  delay(2000);
}
