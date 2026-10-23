"""
webapp.py
Streamlit Web Application for AI-Based Crop Recommendation.
Enhanced with modern UI cards, top contender probabilities,
regional presets, and tailored agronomic guidance.
"""

import json
import os
import pickle
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AgriVision AI - Crop Recommendation",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Clean, Minimalist & Professional)
st.markdown("""
<style>
    .stButton>button {
        background-color: #15803d;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.65rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        width: 100%;
        transition: background-color 0.15s ease;
    }
    .stButton>button:hover {
        background-color: #166534;
        color: #ffffff;
    }
    .winner-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #15803d;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)


# Load Model & Metadata
@st.cache_resource
def load_model_and_meta():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "crop_model.pkl")
    meta_path = os.path.join(base_dir, "model_metadata.json")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    metadata = {}
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

    return model, metadata


model, metadata = load_model_and_meta()

# Sidebar: Regional Presets & Information
st.sidebar.title("🌱 AgriVision AI")
st.sidebar.markdown("**Precision Crop Recommendation**")
st.sidebar.markdown("---")

st.sidebar.subheader("⚡ 1-Click Regional Presets")
preset_choice = st.sidebar.selectbox(
    "Select a climate & soil scenario:",
    [
        "Custom Input",
        "🌾 Indo-Gangetic Alluvial (Rice Paddy)",
        "☁️ Deccan Vertisol (Cotton Black Soil)",
        "🍎 Himalayan Valley (Apple Orchard)",
        "☕ Western Ghats (Coffee Estate)",
        "🌰 Semi-Arid Dryland (Chickpea / Gram)",
        "🥥 Coastal Sandy Loam (Coconut Palm)",
        "🍉 Riverine Sandy Bed (Watermelon)",
    ]
)

presets_map = {
    "🌾 Indo-Gangetic Alluvial (Rice Paddy)": {"N": 90, "P": 42, "K": 43, "temperature": 23.5, "humidity": 82.0, "ph": 6.8, "rainfall": 230.0},
    "☁️ Deccan Vertisol (Cotton Black Soil)": {"N": 115, "P": 45, "K": 20, "temperature": 24.0, "humidity": 80.0, "ph": 6.9, "rainfall": 80.0},
    "🍎 Himalayan Valley (Apple Orchard)": {"N": 20, "P": 135, "K": 200, "temperature": 22.0, "humidity": 92.0, "ph": 6.0, "rainfall": 110.0},
    "☕ Western Ghats (Coffee Estate)": {"N": 100, "P": 30, "K": 30, "temperature": 25.5, "humidity": 65.0, "ph": 6.7, "rainfall": 160.0},
    "🌰 Semi-Arid Dryland (Chickpea / Gram)": {"N": 40, "P": 68, "K": 80, "temperature": 18.5, "humidity": 17.0, "ph": 7.3, "rainfall": 75.0},
    "🥥 Coastal Sandy Loam (Coconut Palm)": {"N": 20, "P": 15, "K": 30, "temperature": 27.0, "humidity": 95.0, "ph": 6.0, "rainfall": 175.0},
    "🍉 Riverine Sandy Bed (Watermelon)": {"N": 100, "P": 18, "K": 50, "temperature": 26.0, "humidity": 85.0, "ph": 6.5, "rainfall": 50.0},
}

default_vals = presets_map.get(preset_choice, {
    "N": 90, "P": 42, "K": 43, "temperature": 23.5, "humidity": 82.0, "ph": 6.5, "rainfall": 200.0
})

st.sidebar.markdown("---")
st.sidebar.info("💡 **Model Accuracy:** 99.55%\n\n**Trained on:** 2,200 records across 22 multi-class agricultural crops.")

# Main Application Header
st.title("🌱 AI-Based Crop Recommendation System")
st.markdown("Precision agriculture decision support powered by Random Forest multi-class ensemble.")

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("Field Soil & Weather Parameters")

    c1, c2, c3 = st.columns(3)
    with c1:
        N = st.number_input("Nitrogen (N) kg/ha", 0, 200, int(default_vals["N"]))
    with c2:
        P = st.number_input("Phosphorus (P) kg/ha", 0, 200, int(default_vals["P"]))
    with c3:
        K = st.number_input("Potassium (K) kg/ha", 0, 200, int(default_vals["K"]))

    c4, c5 = st.columns(2)
    with c4:
        temperature = st.number_input("Temperature (°C)", 0.0, 60.0, float(default_vals["temperature"]), step=0.5)
    with c5:
        humidity = st.number_input("Relative Humidity (%)", 0.0, 100.0, float(default_vals["humidity"]), step=1.0)

    c6, c7 = st.columns(2)
    with c6:
        ph = st.number_input("Soil pH Level", 0.0, 14.0, float(default_vals["ph"]), step=0.1)
    with c7:
        rainfall = st.number_input("Rainfall (mm)", 0.0, 500.0, float(default_vals["rainfall"]), step=5.0)

    predict_btn = st.button("🌱 Recommend Optimal Crop")

with col_right:
    st.subheader("Agronomic Analysis & Recommendations")

    if predict_btn or preset_choice != "Custom Input":
        # Boundary validation
        if not (0 <= N <= 200 and 0 <= P <= 200 and 0 <= K <= 200):
            st.error("N, P, and K values must be between 0 and 200 kg/ha.")
        elif not (0 <= temperature <= 60):
            st.error("Temperature must be between 0 and 60 °C.")
        elif not (0 <= humidity <= 100):
            st.error("Humidity must be between 0 and 100 %.")
        elif not (0 <= ph <= 14):
            st.error("Soil pH must be between 0 and 14.")
        elif not (0 <= rainfall <= 500):
            st.error("Rainfall must be between 0 and 500 mm.")
        else:
            values = pd.DataFrame(
                [[N, P, K, temperature, humidity, ph, rainfall]],
                columns=["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
            )
            probs = model.predict_proba(values)[0]
            classes = model.classes_
            ranked = np.argsort(probs)[::-1]
            top_crop = classes[ranked[0]]
            top_conf = probs[ranked[0]] * 100

            st.markdown(f"""
            <div class="winner-box">
                <div style="font-size: 0.78rem; color: #15803d; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700;">
                    Recommended Crop
                </div>
                <div style="font-size: 2rem; font-weight: 700; color: #0f172a; margin: 0.2rem 0;">
                    {top_crop.title()}
                </div>
                <div style="font-size: 1rem; color: #15803d; font-weight: 600;">
                    Confidence: {top_conf:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Top 3 Contenders
            st.markdown("**Top Alternative Contenders:**")
            for idx in ranked[:3]:
                c_name = classes[idx].title()
                p_val = probs[idx]
                st.write(f"{c_name}: {p_val * 100:.1f}%")
                st.progress(float(p_val))

            # Soil pH Diagnostics
            st.markdown("---")
            if ph < 5.5:
                st.warning("⚠️ **Acidic Soil:** Consider applying agricultural lime (CaCO3) to enhance nutrient uptake.")
            elif ph <= 7.5:
                st.success("✅ **Optimal Soil pH:** Soil reaction is within ideal range for maximal nutrient availability.")
            else:
                st.warning("⚠️ **Alkaline Soil:** High pH detected. Adding gypsum or organic compost is recommended.")

    else:
        st.info("👈 Enter soil and climate measurements or pick a preset from the sidebar, then click **'Recommend Optimal Crop'**.")
