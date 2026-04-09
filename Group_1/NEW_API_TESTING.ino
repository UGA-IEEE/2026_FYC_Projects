#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

// ================================================================
// CONFIGURATION
// ================================================================
const char* EAP_IDENTITY = "username#####@uga.edu"; 
const char* EAP_PASSWORD = "password";
const char* MQTT_SERVER  = "172.21.70.115"; 
const char* API_KEY      = "c0f07161-d376-4f10-b63a-8131dcb2b763"; 

const int   MQTT_PORT    = 1883;
const char* SENSOR_ID    = "wrist_01";
String mqttTopic         = "sensors/" + String(API_KEY);

WiFiClient espClient;
PubSubClient mqtt(espClient);
MAX30105 sensor;

const byte RATE_SIZE = 4;
byte rates[RATE_SIZE];
byte rateSpot = 0;
long lastBeat = 0;
float beatsPerMinute = 0;
int beatAvg = 0;
float lastSpO2 = 0;
long redSum = 0, irSum = 0;
int spo2SampleCount = 0;

// ================================================================
// WIFI & MQTT HELPERS
// ================================================================
void connectWiFi() {
  WiFi.mode(WIFI_STA);
  Serial.print("Connecting to eduroam");
  WiFi.begin("eduroam", WPA2_AUTH_PEAP, "", EAP_IDENTITY, EAP_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
    attempts++;
    if (attempts > 30) { ESP.restart(); }
  }
  Serial.println("\nWiFi Connected!");
}

void reconnectMQTT() {
  while (!mqtt.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (mqtt.connect("esp32_wearable")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqtt.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

// ================================================================
// SPO2 CALCULATION
// ================================================================
float calculateSpO2(long red, long ir) {
  if (ir == 0) return 0;
  float ratio = (float)red / (float)ir;
  float spo2 = 110.0 - 25.0 * ratio; 
  if (spo2 > 100.0) spo2 = 100.0;
  if (spo2 < 80.0) spo2 = 80.0;
  return spo2;
}

// ================================================================
// SETUP
// ================================================================
void setup() {
  Serial.begin(115200);
  delay(1000);
  
  connectWiFi();
  mqtt.setServer(MQTT_SERVER, MQTT_PORT);

  // Using XIAO pins 6 (SDA) and 7 (SCL)
  Wire.begin(6, 7); 

  if (!sensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30102 not found! Check wiring.");
    delay(3000);
    ESP.restart(); 
  }

  sensor.setup(); 
  // CALIBRATED BRIGHTNESS (0x1F) to prevent saturation (262143 error)
  sensor.setPulseAmplitudeRed(0x1F); 
  sensor.setPulseAmplitudeIR(0x1F);
  
  Serial.println("System Ready. Place finger LIGHTLY on sensor.");
}

// ================================================================
// MAIN LOOP
// ================================================================
void loop() {
  if (!mqtt.connected()) reconnectMQTT();
  mqtt.loop();

  long irValue = sensor.getIR();
  long redValue = sensor.getRed();

  // DEBUG: Monitor IR values
  //Serial.print("IR Value: "); Serial.println(irValue);

  // Detect finger presence
  if (irValue < 20000) {
    return; 
  }

  redSum += redValue;
  irSum += irValue;
  spo2SampleCount++;

  // Beat Detection Logic
  if (checkForBeat(irValue)) {
    long delta = millis() - lastBeat;
    lastBeat = millis();
    beatsPerMinute = 60.0 / (delta / 1000.0);

    if (beatsPerMinute > 40 && beatsPerMinute < 220) {
      rates[rateSpot % RATE_SIZE] = (byte)beatsPerMinute;
      rateSpot++;
      beatAvg = 0;
      for (byte i = 0; i < RATE_SIZE; i++) beatAvg += rates[i];
      beatAvg /= RATE_SIZE;
    }
  }

  // Publish every 2 seconds if a beat is detected
  static unsigned long lastPublish = 0;
  if (millis() - lastPublish > 2000 && beatAvg > 0) {
    lastPublish = millis();
    
    float currentSpO2 = calculateSpO2(redSum / spo2SampleCount, irSum / spo2SampleCount);
    redSum = 0; irSum = 0; spo2SampleCount = 0;

    String json = "{";
    json += "\"sensor_id\":\"" + String(SENSOR_ID) + "\",";
    json += "\"heart_rate\":" + String(beatAvg) + ",";
    json += "\"spo2\":" + String(currentSpO2, 1);
    json += "}";

    bool sent = mqtt.publish(mqttTopic.c_str(), json.c_str());
    Serial.printf("\n*** Sent to Pi: HR=%d SpO2=%.1f | MQTT: %s ***\n", 
                  beatAvg, currentSpO2, sent ? "OK" : "FAIL");
  }
}
