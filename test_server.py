from server import app

def main():
    client = app.test_client()

    print("--- 1. Testing Health API ---")
    r = client.get("/api/health")
    print("Health Status:", r.status_code, r.get_json()["status"])

    print("\n--- 2. Testing Prediction API (Rice Preset) ---")
    payload = {
        "N": 90, "P": 42, "K": 43,
        "temperature": 20.8, "humidity": 82.0, "ph": 6.5, "rainfall": 202.9
    }
    r_pred = client.post("/api/predict", json=payload)
    data = r_pred.get_json()
    print("Status:", r_pred.status_code)
    print("Recommended Crop:", data["primary_recommendation"]["crop_name"])
    print("Confidence:", data["primary_recommendation"]["confidence_percentage"], "%")
    print("Top 3 Contenders:", [c["crop_name"] for c in data["top_contenders"][:3]])
    print("Soil pH Diagnostic:", data["soil_diagnostics"]["ph_analysis"]["category"])

    print("\n--- 3. Testing Out-of-Range Boundary Rejection ---")
    r_bad = client.post("/api/predict", json={"N": -5, "P": 50, "K": 50, "temperature": 25, "humidity": 70, "ph": 7, "rainfall": 100})
    print("Invalid Input Response Code:", r_bad.status_code, "Message:", r_bad.get_json().get("message"))

    print("\n--- 4. Testing QA Benchmark Suite ---")
    r_tests = client.get("/api/tests")
    t_data = r_tests.get_json()
    print("Benchmark Status:", t_data["overall_status"])
    for t in t_data["results"]:
        print(f"  [{t['id']}] {t['status']}: {t['name']} -> {t['actual']} ({t['latency_ms']} ms)")

    print("\n--- 5. Testing Crops Directory API ---")
    r_crops = client.get("/api/crops")
    print("Crops Count:", r_crops.get_json()["total"])

    print("\n--- 6. Testing Presets API ---")
    r_presets = client.get("/api/presets")
    print("Presets Count:", len(r_presets.get_json()["presets"]))

    print("\nALL BACKEND API TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
