# ============================================================
#  رصد (Rasd) — Alert Checker
#  Sensors: DHT11 (temp/humidity), Rain sensor, Soil moisture
# ============================================================
import config
import database as db

_last_alerts = set()


def check(temp, humidity, water_level, soil_moisture):
    triggered = []

    def _fire(kind, msg, val):
        if kind not in _last_alerts:
            _last_alerts.add(kind)
            db.insert_alert(kind, msg, val)
            triggered.append({"type": kind, "message": msg, "value": val})

    def _clear(kind):
        _last_alerts.discard(kind)

    # Temperature
    if temp > config.TEMP_MAX:
        _fire("TEMP_HIGH", f"🌡️ درجة الحرارة مرتفعة: {temp}°C", temp)
    else:
        _clear("TEMP_HIGH")

    if temp < config.TEMP_MIN:
        _fire("TEMP_LOW", f"🌡️ درجة الحرارة منخفضة: {temp}°C", temp)
    else:
        _clear("TEMP_LOW")

    # Humidity
    if humidity > config.HUMID_MAX:
        _fire("HUMID_HIGH", f"💧 رطوبة مرتفعة جداً: {humidity}%", humidity)
    else:
        _clear("HUMID_HIGH")

    if humidity < config.HUMID_MIN:
        _fire("HUMID_LOW", f"💧 رطوبة منخفضة جداً: {humidity}%", humidity)
    else:
        _clear("HUMID_LOW")

    # Rain / water leak sensor (LOW value = wet)
    if water_level < config.WATER_THRESHOLD:
        _fire("WATER_DETECTED", f"🌧️ تم كشف الماء! (قيمة: {water_level})", water_level)
    else:
        _clear("WATER_DETECTED")

    # Soil moisture sensor (LOW value = very wet)
    if soil_moisture < config.SOIL_WET_THRESHOLD:
        _fire("SOIL_WET", f"🪴 رطوبة التربة عالية جداً! (قيمة: {soil_moisture})", soil_moisture)
    else:
        _clear("SOIL_WET")

    return triggered
