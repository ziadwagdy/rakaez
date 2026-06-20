# قاعدة البيانات — حفظ القراءات
import sqlite3

# إنشاء قاعدة البيانات (أو فتحها إن وُجدت)
conn = sqlite3.connect('rasd.db')

# إنشاء الجدول
conn.execute("""
    CREATE TABLE IF NOT EXISTS readings (
        id          INTEGER PRIMARY KEY,
        temperature REAL,
        humidity    REAL,
        timestamp   TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")

# حفظ قراءة
conn.execute(
    "INSERT INTO readings (temperature, humidity) VALUES (?, ?)",
    (28.5, 65)
)
conn.commit()

# قراءة البيانات
rows = conn.execute("SELECT * FROM readings").fetchall()
for row in rows:
    print(row)

conn.close()
