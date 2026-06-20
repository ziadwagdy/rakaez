# إرجاع JSON من Flask — هذا ما تقرأه الـ Dashboard
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/latest')
def latest():
    data = {
        'temperature':   28.5,
        'humidity':      65,
        'water_level':   62000,
        'soil_moisture': 18000
    }
    return jsonify(data)   # يحوّل القاموس إلى JSON

# جرّب في المتصفح: http://localhost:8080/api/latest
app.run(port=8080)
