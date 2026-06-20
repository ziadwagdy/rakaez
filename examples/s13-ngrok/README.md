# مشاركة رصد مع العالم — ngrok

## الخطوات

### ١. تثبيت ngrok
- اذهب إلى https://ngrok.com
- سجّل حساباً مجانياً
- حمّل ngrok وثبّته

### ٢. إضافة التوكن
```bash
ngrok config add-authtoken YOUR_TOKEN_HERE
```

### ٣. تشغيل النفق
```bash
# شغّل Flask أولاً
python app.py

# ثم في نافذة أخرى
ngrok http 8080
```

### ٤. الرابط العام
```
Forwarding: https://xxxx-xx-xx-xxx.ngrok.io
```

## تحديث dashboard.html للرابط العام
```javascript
// بدل localhost استخدم رابط ngrok
fetch('https://xxxx.ngrok.io/api/latest')
```

## ملاحظة
- الرابط يتغير في كل مرة تشغّل ngrok (الحساب المجاني)
- يظل يعمل طالما النافذة مفتوحة
