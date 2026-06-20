# أبسط تطبيق Flask ممكن
# شغّل: python 01-hello-flask.py
# افتح: http://localhost:8080

from flask import Flask

app = Flask(__name__)

@app.route('/')          # عنوان URL
def home():
    return 'مرحباً من رصد! 🛡️'

@app.route('/hello')     # عنوان آخر
def hello():
    return 'هذا route مختلف'

app.run(port=8080)
