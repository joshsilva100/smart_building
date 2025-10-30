#include <WiFi.h>

const char* ssid = "HVACR"; //Our wifi/hotspot name :]
const char* password = "INNO4990~"; // password to connect to the hotspot
const uint16_t port = 4269;
const char* host = "10.42.0.1";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  Serial.print("Connecting...");

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected!");
    Serial.print("ESP32 IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n Failed to connect. Check SSID or password.");
  }
}

void loop() {
  WiFiClient client; 

  if (!client.connect(host,port)){
    Serial.println("\nCould not connect!");
    delay(3000);
    return;
  }

  Serial.println("\nConnected!");

  client.println("Hey Dr. Guo, Let's go gambling!");
  Serial.println("\nDisconnecting...");
  client.stop();

  delay(10000);

}