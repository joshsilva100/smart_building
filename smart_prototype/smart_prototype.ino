/* smart_prototype.ino
 * HVAC/Smart Building
 * Joshua Silva
 *
 * Purpose: Initialize and collect data from the Adafruit HDC3022, SCD-41, VEML-7700, & SPH0645 sensors 
 *          using the ESP32 Feather V2
 * 
 * Output format is temp,humid,co2_ppm,lux,noise 
 *  
 * References: 
 *            https://github.com/adafruit/Adafruit_HDC302x/tree/main 
 *            https://github.com/Sensirion/arduino-i2c-scd4x/tree/master/src
 *            https://github.com/adafruit/Adafruit_VEML7700 
 *            https://docs.espressif.com/projects/arduino-esp32/en/latest/api/i2s.html#sample-code 
 *            https://cdn-learn.adafruit.com/assets/assets/000/123/406/original/adafruit_products_Adafruit_ESP32_Feather_V2_Pinout.png?1691707257     
              https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/sleep_modes.html
 */ 

/* Libraries */
#include <WiFi.h>
#include <Adafruit_HDC302x.h> 
#include <SensirionI2cScd4x.h>
#include <Wire.h> 
#include "Adafruit_VEML7700.h" 
#include <ESP_I2S.h> 
#include <esp_sleep.h> 

/* Wifi Init */
const char* ssid = "HVACR"; //Our wifi/hotspot name :]
const char* password = "INNO4990~"; // password to connect to the hotspot
const uint16_t port = 5400;
const char* host = "10.42.0.1"; 

/* HDC3022 Init */
Adafruit_HDC302x hdc = Adafruit_HDC302x(); 

/* SCD-41 Init */ 
SensirionI2cScd4x scd41;  

/* VEML-7700 Init */ 
Adafruit_VEML7700 veml = Adafruit_VEML7700(); 

/* SPH0645 Init */ 

// I2S pins on ESP32 Feather V2
#define I2S_LRC 25 // A1/DAC1
#define I2S_DIN 26 // DOUT from mic A0/DAC2
#define I2S_BCLK 5 // SCK

// I2S Parameters
const int sampleRate = 15000;  // sample rate in Hz 
i2s_mode_t mode = I2S_MODE_STD; 
i2s_data_bit_width_t bps = I2S_DATA_BIT_WIDTH_32BIT;
i2s_slot_mode_t slot = I2S_SLOT_MODE_MONO; 

I2SClass i2s;

void setup() {
  Serial.begin(115200); 

  /* HDC3022 Setup */
  hdc.begin(0x44, &Wire); //Default I2C address for HDC3022  

  /* SCD-41 Setup */ 
  Wire.begin();
  scd41.begin(Wire, SCD41_I2C_ADDR_62);
  scd41.wakeUp(); 
  scd41.startPeriodicMeasurement();

  /* VEML-7700 Setup */ 
  veml.begin();

  /* SPH0645 Setup */ 
  i2s.setPins(I2S_BCLK, I2S_LRC, -1, I2S_DIN); // Use suggested pins. We do not need to write data to the sensor, give bogus value
  i2s.begin(mode, sampleRate, bps, slot); // start I2S at the sample rate with 32-bits per sample

  /* Wifi Setup */ 
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

  // WiFi.begin(ssid, password);

  // Serial.print("Connecting...");

  // if (WiFi.status() == WL_CONNECTED) {
  //   Serial.println("\nConnected!");
  //   Serial.print("ESP32 IP Address: ");
  //   Serial.println(WiFi.localIP());
  // } else {
  //   Serial.println("\n Failed to connect. Check SSID or password.");
  // }

  if (!client.connect(host,port)){
    Serial.println("\nCould not connect!");
    delay(3000);
    return;
  }
  Serial.println("\nConnected!");
  /* HDC3022 Readings */
  double temp = 0.0;
  double humid = 0.0;
  hdc.readTemperatureHumidityOnDemand(temp, humid, TRIGGERMODE_LP3); //LP0 Lowest Noise. Goes up to LP3, go for low power use 

  /* SCD-41 Readings */ 
  uint16_t co2_ppm = 0;
  float temp_41 = 0.0;
  float humid_41 = 0.0;
  scd41.readMeasurement(co2_ppm, temp_41, humid_41); // Raw works fine as well if we don't care about extra checks & float conversion
  
  /* VEML-7700 Readings */ 
  float lux = 0.0;
  lux = veml.readLux(); 

  /* SPH0645 Readings */ 
  int noise = 0;
  noise = i2s.read(); 

  /* Output Data */
  Serial.print(temp); // In Celsius by default 
  Serial.print(F(","));
  Serial.print(humid); 
  Serial.print(F(",")); 

  Serial.print(co2_ppm); 
  Serial.print(F(",")); 

  Serial.print(lux); 
  Serial.print(F(",")); 

  Serial.print(noise);
  Serial.print(F("\n")); 
  /* Sent Data */
  client.printf("%f,%f,%u,%f,%i",temp,humid,co2_ppm,lux,noise); // In Celsius by default 
  // client.print(F(","));
  // client.print(humid); 
  // client.print(F(",")); 

  // client.print(co2_ppm); 
  // client.print(F(",")); 

  // client.print(lux); 
  // client.print(F(",")); 

  // client.print(noise);
  // client.print(F("\n")); 

  Serial.println("\nDisconnecting...");
  client.stop();
  delay(5000); // Read at slowest sensor (SCD-41 every 5 seconds, 30 at low power)

  //setup for ESP32 deepsleep/wakeup
  Serial.println("ESP32 going to deep sleep for 30 minutes...");
  const uint32_t sleepTimeSec = 30 * 60; // 30mins = 1800secs
  const uint64_t sleepTimeUs = (uint64_t)sleepTimeSec * 1000000ULL; 

  // This is the timer for the Esp32 to wake up
  esp_sleep_enable_timer_wakeup(sleepTimeUs); 
  Serial.println("Entering deep sleep now."); 
  Serial.flush();

   // goes to deep sleep
  esp_deep_sleep_start();
} 
