# Flask + SQLite معاً
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DB = 'rasd.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row   # النتائج كقاموس
    return conn

# إنشاء الجدول عند بدء التشغيل
with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY,
            temperature REAL, humidity REAL,
            water_level INTEGER, soil_moisture INTEGER,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

@app.route('/api/data', methods=['POST'])
def receive():
    d = request.get_json()
    with get_db() as db:
        db.execute(
            "INSERT INTO readings (temperature,humidity,water_level,soil_moisture) VALUES (?,?,?,?)",
            (d['temperature'], d['humidity'], d['water_level'], d['soil_moisture'])
        )
    return jsonify({'ok': True})

@app.route('/api/readings')
def readings():
    with get_db() as db:
        rows = db.execute("SELECT * FROM readings ORDER BY id DESC LIMIT 50").fetchall()
    return jsonify([dict(r) for r in rows])

app.run(port=8080)
