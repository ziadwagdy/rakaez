# ============================================================
#  رصد (Rasd) — Database Module (SQLite)
#  Sensors: DHT11 (temp/humidity), Rain sensor, Soil moisture
# ============================================================
import sqlite3
from datetime import datetime
from config import DB_PATH


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS readings (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp     TEXT    NOT NULL,
            temperature   REAL    NOT NULL,
            humidity      REAL    NOT NULL,
            water_level   INTEGER NOT NULL,
            soil_moisture INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT    NOT NULL,
            type        TEXT    NOT NULL,
            message     TEXT    NOT NULL,
            value       REAL    NOT NULL
        );
        """)
    print("✅ Database ready:", DB_PATH)


def insert_reading(temp, humidity, water_level, soil_moisture):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO readings (timestamp, temperature, humidity, water_level, soil_moisture) VALUES (?,?,?,?,?)",
            (ts, temp, humidity, water_level, soil_moisture)
        )
    return ts


def insert_alert(alert_type, message, value):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO alerts (timestamp, type, message, value) VALUES (?,?,?,?)",
            (ts, alert_type, message, value)
        )


def get_recent_readings(limit=50):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM readings ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in reversed(rows)]


def get_recent_alerts(limit=20):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM alerts ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_stats():
    with get_conn() as conn:
        row = conn.execute("""
            SELECT
                COUNT(*)                  AS total,
                ROUND(AVG(temperature),1) AS avg_temp,
                ROUND(MAX(temperature),1) AS max_temp,
                ROUND(MIN(temperature),1) AS min_temp,
                ROUND(AVG(humidity),1)    AS avg_humid
            FROM readings
        """).fetchone()
    return dict(row) if row else {}
