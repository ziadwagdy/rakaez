# ============================================================
#  رصد (Rasd) — Sensor State
#  Pico W POSTs data to /api/data over WiFi — no serial needed
#  Demo mode runs a background thread with fake data
# ============================================================
import threading
import time
import config

_latest = {"temperature": 0, "humidity": 0, "water_level": 65535, "soil_moisture": 65535}
_lock   = threading.Lock()


def update(data: dict):
    """Called by Flask when Pico W POSTs new sensor data."""
    with _lock:
        _latest.update(data)


def start_demo():
    """Start a background thread that generates fake sensor data."""
    def _loop():
        while True:
            with _lock:
                _latest.update(config.demo_reading())
            time.sleep(2)
    t = threading.Thread(target=_loop, daemon=True)
    t.start()
    print("🎭 Demo mode active — generating fake sensor data")


def get_latest():
    with _lock:
        return dict(_latest)
