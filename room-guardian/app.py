# ============================================================
#  رصد (Rasd) — Flask API
#  Pico W sends data via POST /api/data over WiFi
#  Run: python app.py
# ============================================================
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import threading, time

import config
import database as db
import sensors
import alerts as alert_checker

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

# ── Background recorder (demo mode only) ────────────────────
def _demo_record_loop():
    while True:
        data = sensors.get_latest()
        if data["temperature"] != 0:
            db.insert_reading(
                data["temperature"], data["humidity"],
                data["water_level"], data["soil_moisture"]
            )
            alert_checker.check(
                data["temperature"], data["humidity"],
                data["water_level"], data["soil_moisture"]
            )
        time.sleep(5)


# ── Routes ────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")


@app.route("/api/status")
def status():
    return jsonify({"mode": "demo" if config.DEMO_MODE else "live", "ok": True})


# Pico W posts sensor data here
@app.route("/api/data", methods=["POST"])
def receive_data():
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "no data"}), 400

    sensors.update(data)
    db.insert_reading(
        data.get("temperature", 0),
        data.get("humidity", 0),
        data.get("water_level", 65535),
        data.get("soil_moisture", 65535)
    )
    triggered = alert_checker.check(
        data.get("temperature", 0),
        data.get("humidity", 0),
        data.get("water_level", 65535),
        data.get("soil_moisture", 65535)
    )
    return jsonify({"ok": True, "alerts": triggered})


@app.route("/api/latest")
def latest():
    data = sensors.get_latest()
    triggered = alert_checker.check(
        data["temperature"], data["humidity"],
        data["water_level"], data["soil_moisture"]
    )
    return jsonify({**data, "alerts": triggered})


@app.route("/api/readings")
def readings():
    return jsonify(db.get_recent_readings(50))


@app.route("/api/alerts")
def alerts():
    return jsonify(db.get_recent_alerts(20))


@app.route("/api/stats")
def stats():
    return jsonify(db.get_stats())


# ── Startup ───────────────────────────────────────────────────
if __name__ == "__main__":
    db.init_db()
    mode = "🎭 DEMO" if config.DEMO_MODE else "🔌 LIVE (waiting for Pico W)"
    if config.DEMO_MODE:
        sensors.start_demo()
        t = threading.Thread(target=_demo_record_loop, daemon=True)
        t.start()
    print(f"\n🛡  رصد (Rasd) running — {mode} mode")
    print(f"   Dashboard  → http://localhost:{config.PORT}")
    if not config.DEMO_MODE:
        print(f"   Pico W POST → http://<your-ip>:{config.PORT}/api/data\n")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
