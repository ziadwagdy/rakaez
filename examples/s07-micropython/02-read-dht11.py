# قراءة الحرارة والرطوبة من DHT11
# الحساس موصول على GP15

from machine import Pin
from time import sleep
import dht

sensor = dht.DHT11(Pin(15))

while True:
    sensor.measure()                      # اقرأ الحساس
    temp  = sensor.temperature()          # درجة الحرارة
    humid = sensor.humidity()             # الرطوبة

    print(f"الحرارة: {temp}°C")
    print(f"الرطوبة: {humid}%")
    print("---")

    sleep(2)                              # DHT11 يحتاج ثانيتين بين القراءات
