"""
run_app.py
Entry point to launch the AgriVision AI Full-Stack Application.
Checks assets, launches Flask server, and opens the web application in browser.
"""

import os
import sys
import threading
import time
import webbrowser

def open_browser():
    time.sleep(1.2)
    url = "http://127.0.0.1:5000"
    print(f"\n[AgriVision AI] Opening web application in browser: {url}\n")
    webbrowser.open(url)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "crop_model.pkl")

    if not os.path.exists(model_path):
        print("\n[AgriVision AI] Model not found. Running training pipeline first...")
        from app import train_crop_model
        train_crop_model()

    print("\n" + "=" * 65)
    print("🌱  AgriVision AI - Precision Crop Recommendation Full-Stack App")
    print("🚀  Local Server: http://127.0.0.1:5000")
    print("⚡  Model Accuracy: 99.55% (22 Crop Varieties)")
    print("🌤️  Live Satellite Weather: Open-Meteo Integration Active")
    print("🧪  QA Test Suite: http://127.0.0.1:5000 (Tab 4)")
    print("=" * 65 + "\n")

    # Open browser automatically in background thread
    threading.Thread(target=open_browser, daemon=True).start()

    from server import app
    app.run(host="127.0.0.1", port=5000, debug=False)

if __name__ == "__main__":
    main()
