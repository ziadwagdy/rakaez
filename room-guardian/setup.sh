#!/bin/bash
# ============================================================
#  Room Guardian — One-command setup (Mac / Linux)
# ============================================================
echo "🛡  Room Guardian Setup"
echo "──────────────────────"

# 1. Python check
if ! command -v python3 &>/dev/null; then
  echo "❌ Python 3 not found. Install from https://python.org"; exit 1
fi

# 2. Virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Dependencies
pip install -q -r requirements.txt

# 4. Run
echo ""
echo "✅ Setup complete! Starting Room Guardian in DEMO mode…"
echo "   Open http://localhost:5000 in your browser"
echo ""
DEMO_MODE=true python app.py
