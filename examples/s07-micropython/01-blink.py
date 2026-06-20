# الجلسة ٧ — أول برنامج على Pico W
# افتح Thonny، وصّل Pico W، انسخ هذا الكود واضغط Run

from machine import Pin
from time import sleep

# Pin 25 هو LED المدمج في Pico W
led = Pin(25, Pin.OUT)

while True:           # كرّر للأبد
    led.on()          # أضئ
    sleep(0.5)        # انتظر نصف ثانية
    led.off()         # أطفئ
    sleep(0.5)        # انتظر نصف ثانية

# جرّب: غيّر 0.5 إلى 0.1 أو 2 — ماذا يحدث؟
