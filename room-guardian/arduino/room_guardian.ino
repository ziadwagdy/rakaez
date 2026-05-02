// ============================================================
//  رصد (Rasd) — Arduino Sketch
//  Reads DHT22 + vibration sensor, sends JSON over Serial
//  Wiring:
//    DHT22  DATA → pin 2
//    Vibration sensor → pin A0
// ============================================================
#include <DHT.h>

#define DHT_PIN   2
#define DHT_TYPE  DHT22
#define VIB_PIN   A0
#define LED_PIN   13        // built-in LED blinks on alert

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(LED_PIN, OUTPUT);
  delay(2000);  // let DHT stabilise
}

void loop() {
  float temp     = dht.readTemperature();
  float humidity = dht.readHumidity();
  int   vib      = analogRead(VIB_PIN);

  if (isnan(temp) || isnan(humidity)) {
    Serial.println("{\"error\":\"sensor_read_failed\"}");
  } else {
    // Alert LED
    digitalWrite(LED_PIN, (temp > 35 || vib > 500) ? HIGH : LOW);

    // Send JSON line — Python reads this over Serial
    Serial.print("{\"temperature\":");
    Serial.print(temp, 1);
    Serial.print(",\"humidity\":");
    Serial.print(humidity, 1);
    Serial.print(",\"vibration\":");
    Serial.print(vib);
    Serial.println("}");
  }

  delay(2000);  // send every 2 seconds
}
