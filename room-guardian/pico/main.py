# ============================================================
#  رصد (Rasd) — Raspberry Pi Pico W
#  MicroPython — runs on the Pico W board
#  Reads DHT11 + Rain sensor + Soil moisture sensor
#  Sends data to Flask server over WiFi every 2 seconds
#
#  Wiring:
#    DHT11  DATA  → GP15
#    Rain sensor  → GP26 (ADC0)
#    Soil sensor  → GP27 (ADC1)
#
#  Install via Thonny: save this file as main.py on the Pico W
# ============================================================
import network
import urequests
import dht
import machine
import time
import json

# ── WiFi credentials — change these ──────────────────────────
WIFI_SSID     = "your_wifi_name"
WIFI_PASSWORD = "your_wifi_password"

# ── Flask server IP — change to your computer's local IP ─────
# Find it with: ipconfig (Windows) or ifconfig (Mac/Linux)
SERVER_URL = "http://192.168.1.100:8080/api/data"

# ── Sensor setup ─────────────────────────────────────────────
dht_sensor   = dht.DHT11(machine.Pin(15))
rain_sensor  = machine.ADC(machine.Pin(26))   # ADC0
soil_sensor  = machine.ADC(machine.Pin(27))   # ADC1
led          = machine.Pin("LED", machine.Pin.OUT)   # onboard LED

# ── Connect to WiFi ───────────────────────────────────────────
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    print("Connecting to WiFi", end="")
    for _ in range(20):
        if wlan.isconnected():
            break
        time.sleep(0.5)
        print(".", end="")
    print()
    if wlan.isconnected():
        print("✅ Connected! IP:", wlan.ifconfig()[0])
        led.on()
    else:
        print("❌ WiFi connection failed")

# ── Read sensors and send to server ──────────────────────────
def read_and_send():
    try:
        dht_sensor.measure()
        temp     = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
    except Exception as e:
        print("DHT11 read error:", e)
        return

    water_level   = rain_sensor.read_u16()   # 0–65535
    soil_moisture = soil_sensor.read_u16()   # 0–65535

    data = {
        "temperature":  temp,
        "humidity":     humidity,
        "water_level":  water_level,
        "soil_moisture": soil_moisture
    }

    print("Sending:", data)

    try:
        r = urequests.post(
            SERVER_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )
        resp = r.json()
        if resp.get("alerts"):
            print("⚠️  Alerts:", resp["alerts"])
        r.close()
    except Exception as e:
        print("Send error:", e)
        led.toggle()   # blink LED on error


# ── Main loop ────────────────────────────────────────────────
connect_wifi()
print("🛡 رصد (Rasd) — Pico W running")

while True:
    read_and_send()
    time.sleep(2)
