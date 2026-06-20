# إرسال بيانات الحساس إلى Flask عبر WiFi
# يجب تشغيل app.py أولاً على الحاسوب

import network, urequests, ujson, dht
from machine import Pin
from time import sleep

# ── WiFi ────────────────────────────────
SSID     = 'اسم_الشبكة'
PASSWORD = 'كلمة_المرور'
SERVER   = 'http://192.168.1.X:8080/api/data'  # غيّر X بـ IP حاسوبك

# ── الاتصال ─────────────────────────────
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    sleep(0.5)
print('IP:', wlan.ifconfig()[0])

# ── الحساسات ────────────────────────────
sensor = dht.DHT11(Pin(15))

# ── الحلقة الرئيسية ─────────────────────
while True:
    sensor.measure()

    data = {
        'temperature':  sensor.temperature(),
        'humidity':     sensor.humidity(),
        'water_level':  62000,   # قيمة ثابتة مؤقتاً
        'soil_moisture': 18000   # قيمة ثابتة مؤقتاً
    }

    response = urequests.post(SERVER, json=data)
    print('أُرسل:', data)
    print('الرد:', response.text)
    response.close()

    sleep(5)
