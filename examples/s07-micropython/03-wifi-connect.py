# الاتصال بـ WiFi
# غيّر SSID و PASSWORD قبل التشغيل

import network
from time import sleep

SSID     = 'اسم_الشبكة'
PASSWORD = 'كلمة_المرور'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print('جارٍ الاتصال...')
while not wlan.isconnected():
    sleep(0.5)
    print('.', end='')

print()
print('✅ متصل!')
print('IP:', wlan.ifconfig()[0])
