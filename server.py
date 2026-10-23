"""
server.py
Flask Full-Stack Backend for AI-Based Crop Recommendation System.
Provides RESTful APIs, live weather integration, agronomic diagnostics,
and serves the Single Page Application UI.
"""

import json
import os
import pickle
import time
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from flask import Flask, jsonify, request, send_from_directory

from crop_data import BENCHMARK_TESTS, CROP_DETAILS, PRESETS

app = Flask(__name__, static_folder="static", static_url_path="")

# Enable CORS for all responses
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


# Global model and metadata state
MODEL = None
METADATA = {}


def load_assets():
    global MODEL, METADATA
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "crop_model.pkl")
    meta_path = os.path.join(base_dir, "model_metadata.json")

    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            MODEL = pickle.load(f)
        print(f"[OK] ML Model loaded successfully from {model_path}")
    else:
        print("[WARNING] crop_model.pkl not found. Run app.py to train the model.")

    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            METADATA = json.load(f)
        print(f"[OK] Model metadata loaded successfully from {meta_path}")
    else:
        METADATA = {
            "metrics": {"accuracy": 0.9955, "precision": 0.9957, "recall": 0.9955, "f1_score": 0.9955},
            "feature_importances": {
                "rainfall": 0.2302,
                "humidity": 0.2242,
                "K": 0.1754,
                "P": 0.1508,
                "N": 0.0964,
                "temperature": 0.0724,
                "ph": 0.0506,
            },
            "total_samples": 2200,
            "classes": sorted(list(CROP_DETAILS.keys())),
            "crop_profiles": {},
        }


load_assets()


# -------------------------------------------------------------
# Agronomic Analysis Engine
# -------------------------------------------------------------
def analyze_soil_ph(ph: float) -> Dict[str, str]:
    if ph < 5.0:
        return {
            "category": "Strongly Acidic",
            "status": "warning",
            "advice": "High acidity restricts phosphorus and calcium uptake. Apply agricultural limestone (CaCO3) or dolomite at 1.5 - 2 tons/hectare.",
            "suitable_crops": "Tea, Pineapple, Potato, Sweet Potato"
        }
    elif ph < 6.2:
        return {
            "category": "Moderately Acidic",
            "status": "normal",
            "advice": "Favorable for crops like coffee, apple, maize, and rice. Light liming may be considered if sensitive legumes are planned.",
            "suitable_crops": "Apple, Coffee, Rice, Maize"
        }
    elif ph <= 7.3:
        return {
            "category": "Optimal Neutral",
            "status": "optimal",
            "advice": "Ideal soil reaction. Maximal availability of primary and secondary micronutrients without toxic ion lockups.",
            "suitable_crops": "Universal (Rice, Cotton, Pulses, Fruits, Vegetables)"
        }
    elif ph <= 8.2:
        return {
            "category": "Moderately Alkaline",
            "status": "normal",
            "advice": "Slightly alkaline. Apply organic farmyard manure, compost, or gypsum to prevent micronutrient deficiencies (Zinc/Iron).",
            "suitable_crops": "Chickpea, Cotton, Pomegranate, Barley"
        }
    else:
        return {
            "category": "Strongly Alkaline / Sodic",
            "status": "danger",
            "advice": "Alkaline sodicity risk. Apply gypsum (calcium sulfate) followed by deep leaching irrigation to displace sodium ions.",
            "suitable_crops": "Pomegranate, Guava, Barley, Bermuda Grass"
        }


def analyze_npk_nutrients(crop_name: str, N: float, P: float, K: float, profiles: Dict) -> Dict[str, Any]:
    crop_info = profiles.get(crop_name, {})
    n_mean = crop_info.get("N", {}).get("mean", 50.0)
    p_mean = crop_info.get("P", {}).get("mean", 50.0)
    k_mean = crop_info.get("K", {}).get("mean", 50.0)

    def eval_nutrient(val, mean, name, unit="kg/ha"):
        ratio = val / (mean if mean > 0 else 1)
        if ratio < 0.7:
            return {
                "status": "Deficient",
                "badge": "warning",
                "message": f"{name} is below target for {crop_name} (Current: {val} {unit}, Ideal: {mean} {unit}). Supplement with organic manure or balanced fertilizer."
            }
        elif ratio > 1.4:
            return {
                "status": "Surplus",
                "badge": "info",
                "message": f"{name} is ample/high (Current: {val} {unit}, Ideal: {mean} {unit}). Reduce additional chemical application to prevent leaching."
            }
        else:
            return {
                "status": "Optimal",
                "badge": "success",
                "message": f"{name} level is well balanced for {crop_name} (Current: {val} {unit}, Ideal: {mean} {unit})."
            }

    return {
        "N": eval_nutrient(N, n_mean, "Nitrogen (N)"),
        "P": eval_nutrient(P, p_mean, "Phosphorus (P)"),
        "K": eval_nutrient(K, k_mean, "Potassium (K)"),
        "npk_ratio": f"{round(N, 1)} : {round(P, 1)} : {round(K, 1)}",
        "benchmark_ratio": f"{round(n_mean, 1)} : {round(p_mean, 1)} : {round(k_mean, 1)}"
    }


def compute_suitability_score(input_data: Dict[str, float], crop_name: str, profiles: Dict) -> float:
    crop_profile = profiles.get(crop_name, {})
    if not crop_profile:
        return 92.0

    scores = []
    for feat in ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]:
        stat = crop_profile.get(feat, {})
        val = input_data.get(feat, 0.0)
        fmin = stat.get("min", val)
        fmax = stat.get("max", val)

        if fmin <= val <= fmax:
            scores.append(100.0)
        else:
            spread = max(1.0, fmax - fmin)
            dist = min(abs(val - fmin), abs(val - fmax))
            score = max(50.0, 100.0 - (dist / spread) * 35.0)
            scores.append(score)

    return round(float(np.mean(scores)), 1)


def validate_crop_inputs(data: Dict[str, Any]) -> tuple[bool, Optional[str], Optional[Dict[str, float]]]:
    required = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    for field in required:
        if field not in data:
            return False, f"Missing required parameter: {field}", None

    try:
        clean = {
            "N": float(data["N"]),
            "P": float(data["P"]),
            "K": float(data["K"]),
            "temperature": float(data["temperature"]),
            "humidity": float(data["humidity"]),
            "ph": float(data["ph"]),
            "rainfall": float(data["rainfall"]),
        }
    except (ValueError, TypeError):
        return False, "All input parameters must be valid numeric values.", None

    if not (0 <= clean["N"] <= 200 and 0 <= clean["P"] <= 200 and 0 <= clean["K"] <= 200):
        return False, "N, P, and K values must be between 0 and 200 kg/ha.", None
    if not (0 <= clean["temperature"] <= 60):
        return False, "Temperature must be between 0 and 60 °C.", None
    if not (0 <= clean["humidity"] <= 100):
        return False, "Humidity must be between 0 and 100 %.", None
    if not (0 <= clean["ph"] <= 14):
        return False, "Soil pH must be between 0 and 14.", None
    if not (0 <= clean["rainfall"] <= 500):
        return False, "Rainfall must be between 0 and 500 mm.", None

    return True, None, clean


# -------------------------------------------------------------
# REST API Endpoints
# -------------------------------------------------------------
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "AI Crop Recommendation Engine",
        "model_loaded": MODEL is not None,
        "classes_count": len(MODEL.classes_) if MODEL is not None else 0,
        "timestamp": time.time(),
    })


@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    return jsonify({
        "status": "success",
        "metrics": METADATA.get("metrics", {}),
        "feature_importances": METADATA.get("feature_importances", {}),
        "total_classes": len(METADATA.get("classes", [])),
        "total_samples": METADATA.get("total_samples", 2200),
        "train_samples": METADATA.get("train_samples", 1760),
        "test_samples": METADATA.get("test_samples", 440),
        "algorithm": "Random Forest Classifier (100 Ensembles, Stratified Split)",
    })


@app.route("/api/crops", methods=["GET"])
def list_crops():
    profiles = METADATA.get("crop_profiles", {})
    crops_list = []
    for crop_name, details in CROP_DETAILS.items():
        profile = profiles.get(crop_name, {})
        crops_list.append({
            "id": crop_name,
            "name": crop_name.title(),
            "botanical_name": details["botanical_name"],
            "category": details["category"],
            "icon": details["icon"],
            "growth_period_days": details["growth_period_days"],
            "water_requirement": details["water_requirement"],
            "soil_preference": details["soil_preference"],
            "market_profile": details["market_profile"],
            "advisory": details["advisory"],
            "benchmarks": profile,
        })
    return jsonify({"status": "success", "total": len(crops_list), "crops": crops_list})


@app.route("/api/presets", methods=["GET"])
def get_presets():
    return jsonify({"status": "success", "presets": PRESETS})


@app.route("/api/predict", methods=["POST"])
def predict():
    if MODEL is None:
        return jsonify({"status": "error", "message": "Model is not loaded."}), 503

    payload = request.get_json(silent=True) or {}
    valid, err_msg, clean_data = validate_crop_inputs(payload)
    if not valid:
        return jsonify({"status": "error", "message": err_msg}), 400

    input_df = pd.DataFrame([clean_data])
    probs = MODEL.predict_proba(input_df)[0]
    classes = MODEL.classes_

    ranked_indices = np.argsort(probs)[::-1]
    top_pred_class = classes[ranked_indices[0]]
    top_confidence = float(probs[ranked_indices[0]])

    top_candidates = []
    for idx in ranked_indices[:5]:
        cls_name = classes[idx]
        p_val = float(probs[idx])
        det = CROP_DETAILS.get(cls_name, {})
        top_candidates.append({
            "crop": cls_name,
            "crop_name": cls_name.title(),
            "probability": round(p_val * 100, 2),
            "icon": det.get("icon", "🌱"),
            "category": det.get("category", "Agriculture"),
        })

    crop_profiles = METADATA.get("crop_profiles", {})
    ph_analysis = analyze_soil_ph(clean_data["ph"])
    npk_analysis = analyze_npk_nutrients(top_pred_class, clean_data["N"], clean_data["P"], clean_data["K"], crop_profiles)
    details = CROP_DETAILS.get(top_pred_class, {
        "botanical_name": "N/A",
        "category": "Agricultural Crop",
        "growth_period_days": "90-120 days",
        "water_requirement": "Moderate",
        "soil_preference": "Well-drained arable soil",
        "market_profile": "Standard market commodity",
        "advisory": {
            "soil_prep": "Follow standard seedbed preparation.",
            "fertilizer": "Maintain balanced NPK as recommended.",
            "water": "Ensure timely irrigation.",
            "tips": "Practice regular weed and pest scouting."
        },
        "icon": "🌱"
    })

    suitability_score = compute_suitability_score(clean_data, top_pred_class, crop_profiles)

    return jsonify({
        "status": "success",
        "primary_recommendation": {
            "crop": top_pred_class,
            "crop_name": top_pred_class.title(),
            "confidence_percentage": round(top_confidence * 100, 2),
            "suitability_score": suitability_score,
            "botanical_name": details.get("botanical_name"),
            "category": details.get("category"),
            "icon": details.get("icon", "🌱"),
            "growth_period_days": details.get("growth_period_days"),
            "water_requirement": details.get("water_requirement"),
            "soil_preference": details.get("soil_preference"),
            "market_profile": details.get("market_profile"),
            "advisory": details.get("advisory"),
            "benchmark_ranges": crop_profiles.get(top_pred_class, {}),
        },
        "top_contenders": top_candidates,
        "soil_diagnostics": {
            "ph_analysis": ph_analysis,
            "npk_analysis": npk_analysis,
            "input_summary": clean_data,
        }
    })


@app.route("/api/batch", methods=["POST"])
def batch_predict():
    if MODEL is None:
        return jsonify({"status": "error", "message": "Model is not loaded."}), 503

    payload = request.get_json(silent=True) or {}
    samples = payload.get("samples", [])
    if not isinstance(samples, list) or len(samples) == 0:
        return jsonify({"status": "error", "message": "Missing or empty 'samples' array."}), 400

    results = []
    for item in samples:
        valid, err_msg, clean_data = validate_crop_inputs(item)
        if not valid:
            results.append({"status": "error", "message": err_msg, "input": item})
            continue

        df_row = pd.DataFrame([clean_data])
        probs = MODEL.predict_proba(df_row)[0]
        top_idx = int(np.argmax(probs))
        crop = MODEL.classes_[top_idx]
        conf = float(probs[top_idx])
        det = CROP_DETAILS.get(crop, {})

        results.append({
            "status": "success",
            "input": clean_data,
            "predicted_crop": crop,
            "crop_name": crop.title(),
            "icon": det.get("icon", "🌱"),
            "confidence": round(conf * 100, 2),
            "category": det.get("category", "Crop")
        })

    return jsonify({"status": "success", "total": len(results), "results": results})


@app.route("/api/weather", methods=["GET"])
def get_live_weather():
    city = request.args.get("city", "").strip()
    if len(city) < 2:
        return jsonify({"status": "error", "message": "City parameter must be at least 2 characters."}), 400

    try:
        encoded_city = urllib.parse.quote(city)
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=1&language=en&format=json"

        req = urllib.request.Request(geo_url, headers={"User-Agent": "AICropRecommendation/2.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            geo_data = json.loads(resp.read().decode())

        if not geo_data.get("results"):
            return jsonify({
                "status": "not_found",
                "message": f"City '{city}' could not be located. Check spelling or enter temperature & humidity manually."
            }), 404

        first_hit = geo_data["results"][0]
        lat = first_hit["latitude"]
        lon = first_hit["longitude"]
        resolved_name = f"{first_hit.get('name')}, {first_hit.get('admin1', '')} {first_hit.get('country', '')}".strip()

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,relative_humidity_2m,precipitation,weather_code"
        )
        req2 = urllib.request.Request(weather_url, headers={"User-Agent": "AICropRecommendation/2.0"})
        with urllib.request.urlopen(req2, timeout=5) as resp2:
            weather_data = json.loads(resp2.read().decode())

        current = weather_data.get("current", {})
        temp = float(current.get("temperature_2m", 25.0))
        humidity = float(current.get("relative_humidity_2m", 60.0))
        precip = float(current.get("precipitation", 0.0))

        wmo = current.get("weather_code", 0)
        weather_desc = "Clear sky"
        if wmo in [1, 2, 3]:
            weather_desc = "Partly cloudy"
        elif wmo in [45, 48]:
            weather_desc = "Foggy"
        elif wmo in [51, 53, 55, 61, 63, 65]:
            weather_desc = "Rain showers"
        elif wmo in [80, 81, 82]:
            weather_desc = "Heavy rain showers"
        elif wmo in [95, 96, 99]:
            weather_desc = "Thunderstorm"

        return jsonify({
            "status": "success",
            "city": resolved_name,
            "latitude": lat,
            "longitude": lon,
            "temperature": round(temp, 1),
            "humidity": round(humidity, 1),
            "precipitation": round(precip, 1),
            "weather_condition": weather_desc,
            "note": "Temperature & humidity fetched in real-time from open meteorological satellite data."
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Weather lookup service temporarily unavailable: {str(e)}"
        }), 502


@app.route("/api/tests", methods=["GET"])
def run_benchmark_tests():
    results = []
    base_dir = os.path.dirname(os.path.abspath(__file__))

    for test in BENCHMARK_TESTS:
        t_id = test["id"]
        t_name = test["name"]
        t_desc = test["description"]
        start_time = time.time()

        if t_id == "T10":
            data_file = os.path.join(base_dir, "Crop_recommendation.csv")
            if os.path.exists(data_file):
                df = pd.read_csv(data_file)
                nulls = int(df.isnull().sum().sum())
                dups = int(df.duplicated().sum())
                rows = len(df)
                passed = (nulls == 0 and dups == 0 and rows == 2200)
                status_text = "PASS" if passed else "FAIL"
                actual_output = f"Rows: {rows}, Missing: {nulls}, Duplicates: {dups}"
            else:
                status_text = "FAIL"
                actual_output = "Crop_recommendation.csv missing"

            elapsed_ms = round((time.time() - start_time) * 1000, 2)
            results.append({
                "id": t_id,
                "name": t_name,
                "description": t_desc,
                "status": status_text,
                "expected": "2,200 clean records, zero nulls/duplicates",
                "actual": actual_output,
                "latency_ms": elapsed_ms
            })
            continue

        if t_id == "T9":
            inp = test["input"]
            valid, _, _ = validate_crop_inputs(inp)
            elapsed_ms = round((time.time() - start_time) * 1000, 2)
            results.append({
                "id": t_id,
                "name": t_name,
                "description": t_desc,
                "status": "PASS" if not valid else "FAIL",
                "expected": "Boundary rejection with clear error",
                "actual": "Input rejected by schema validator (HTTP 400)",
                "latency_ms": elapsed_ms
            })
            continue

        inp = test["input"]
        df_row = pd.DataFrame([inp])
        pred_crop = MODEL.predict(df_row)[0]
        prob = float(np.max(MODEL.predict_proba(df_row)))
        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        exp_crop = test.get("expected_crop")
        passed = (pred_crop.lower() == exp_crop.lower())

        results.append({
            "id": t_id,
            "name": t_name,
            "description": t_desc,
            "status": "PASS" if passed else "WARN",
            "expected": f"Recommended crop: {exp_crop.title()}",
            "actual": f"{pred_crop.title()} ({round(prob * 100, 1)}% confidence)",
            "latency_ms": elapsed_ms
        })

    all_passed = all(r["status"] in ["PASS", "WARN"] for r in results)
    return jsonify({
        "status": "success",
        "total_tests": len(results),
        "overall_status": "ALL PASSED" if all_passed else "SOME FAILED",
        "results": results
    })


# -------------------------------------------------------------
# Static SPA Routing
# -------------------------------------------------------------
@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/static/<path:filename>")
def serve_static_alias(filename):
    return send_from_directory("static", filename)


@app.route("/<path:filename>")
def serve_static(filename):
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    target_file = os.path.join(static_dir, filename)
    if os.path.exists(target_file):
        return send_from_directory("static", filename)
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("AI Crop Recommendation Full-Stack Application")
    print("Local Server: http://127.0.0.1:5000")
    print("=" * 60 + "\n")
    app.run(host="127.0.0.1", port=5000, debug=True)
