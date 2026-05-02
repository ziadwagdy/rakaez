@echo off
echo 🛡  Room Guardian Setup
echo ──────────────────────

python --version >nul 2>&1
IF ERRORLEVEL 1 (echo Python not found. Install from https://python.org & pause & exit)

python -m venv venv
call venv\Scripts\activate

pip install -q -r requirements.txt

echo.
echo Setup complete! Starting Room Guardian in DEMO mode...
echo Open http://localhost:5000 in your browser
echo.
set DEMO_MODE=true
python app.py
