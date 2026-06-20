# استقبال بيانات من Pico W عبر POST
from flask import Flask, jsonify, request

app = Flask(__name__)

readings = []   # قائمة لتخزين القراءات مؤقتاً

@app.route('/api/data', methods=['POST'])
def receive():
    data = request.get_json()          # استقبل JSON
    readings.append(data)              # احفظها في القائمة
    print('استُقبل:', data)
    return jsonify({'ok': True})

@app.route('/api/readings')
def get_readings():
    return jsonify(readings)           # أعد كل القراءات

app.run(port=8080)
