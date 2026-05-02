# ============================================================
#  رصد (Rasd) — Configuration & Demo Mode
#  Hardware: Raspberry Pi Pico W + DHT11 + Rain + Soil sensors
# ============================================================
import os
import random
import math

# ── Run mode ────────────────────────────────────────────────
DEMO_MODE = os.environ.get("DEMO_MODE", "true").lower() == "true"

# ── Database ─────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

# ── Alert thresholds ─────────────────────────────────────────
TEMP_MAX          = float(os.environ.get("TEMP_MAX",      "35.0"))
TEMP_MIN          = float(os.environ.get("TEMP_MIN",      "10.0"))
HUMID_MAX         = float(os.environ.get("HUMID_MAX",     "80.0"))
HUMID_MIN         = float(os.environ.get("HUMID_MIN",     "20.0"))
# Sensors return 0-65535 (16-bit ADC on Pico W)
# Rain/water detected when value is LOW (wet = low resistance = low reading)
WATER_THRESHOLD   = int(os.environ.get("WATER_THRESH",   "20000"))   # below this = water detected
SOIL_WET_THRESHOLD = int(os.environ.get("SOIL_THRESH",   "20000"))   # below this = very wet

# ── Flask ─────────────────────────────────────────────────────
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8080"))
DEBUG = False

# ── Demo data generator ───────────────────────────────────────
_tick = 0

def demo_reading():
    """Return realistic fake sensor data that slowly drifts."""
    global _tick
    _tick += 1
    t = _tick * 0.05
    temp          = round(22 + 4 * math.sin(t) + random.uniform(-0.3, 0.3), 1)
    humidity      = round(55 + 8 * math.cos(t * 0.7) + random.uniform(-0.5, 0.5), 1)
    # Rain sensor: normally high (~60000), drops when wet
    water_level   = random.choices(
        [random.randint(55000, 65535), random.randint(5000, 18000)],
        weights=[90, 10]
    )[0]
    # Soil moisture: normally high (~55000), drops when wet
    soil_moisture = random.choices(
        [random.randint(50000, 65535), random.randint(8000, 19000)],
        weights=[88, 12]
    )[0]
    return {
        "temperature":  temp,
        "humidity":     humidity,
        "water_level":  water_level,
        "soil_moisture": soil_moisture
    }
