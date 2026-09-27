import streamlit as st
import requests
import sqlite3
import pandas as pd
from pathlib import Path

# =========================
# PROJECT PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent
API_DIR = BASE_DIR.parent / "api"
DB_PATH = API_DIR / "ato_monitoring.db"

API_URL = "https://ato-detection-api.vercel.app"


st.set_page_config(
    page_title="ATO Detection System",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# 🔥 FULL CSS (DEPTH + ANIMATION)
# =========================
st.markdown("""
<style>

/* Remove default UI noise */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ===== Background Gradient ===== */
.stApp {
    background: linear-gradient(-45deg, #0f172a, #020617, #1e293b, #111827);
    background-size: 400% 400%;
    animation: gradientFlow 18s ease infinite;
    color: white;
}

/* Smooth gradient */
@keyframes gradientFlow {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Floating glow */
.stApp::before {
    content: "";
    position: fixed;
    width: 650px;
    height: 650px;
    background: radial-gradient(circle, rgba(59,130,246,0.18), transparent 60%);
    top: -120px;
    left: -120px;
    animation: floatGlow 20s linear infinite;
    z-index: 0;
}

@keyframes floatGlow {
    0% {transform: translate(0,0);}
    50% {transform: translate(350px, 220px);}
    100% {transform: translate(0,0);}
}

/* Container spacing */
.block-container {
    padding-top: 2rem;
    position: relative;
    z-index: 1;
}

/* ===== CARD (DEPTH EFFECT) ===== */
.card {
    background: rgba(255, 255, 255, 0.06);
    border-radius: 20px;
    padding: 24px;

    border: 2px solid rgba(255,255,255,0.18);

    box-shadow:
        0 8px 30px rgba(0,0,0,0.5),
        inset 0 0 0 1px rgba(255,255,255,0.05);

    backdrop-filter: blur(12px);
    margin-bottom: 20px;

    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow:
        0 14px 45px rgba(0,0,0,0.7),
        0 0 14px rgba(59,130,246,0.2);
}

/* Title */
.title-text {
    font-size: 42px;
    font-weight: 800;
}

.sub-text {
    color: #cbd5e1;
    font-size: 16px;
}

/* ===== INPUT CONTAINER DEPTH ===== */
[data-testid="stVerticalBlock"] > div {
    border: 2px solid rgba(255,255,255,0.14);
    border-radius: 16px;
    padding: 12px;
    box-shadow: 0 6px 25px rgba(0,0,0,0.4);
}

/* ===== METRICS DEPTH ===== */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    border: 2px solid rgba(255,255,255,0.18);
    padding: 14px;
    border-radius: 16px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.35);
}

/* ===== SLIDER ENHANCEMENT ===== */
.stSlider > div {
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 12px;
    padding: 6px;
}

/* ===== BLOCK PULSE ===== */
.pulse-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 30px;
}

.pulse {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: rgba(239, 68, 68, 0.25);
    position: relative;
}

.pulse::before, .pulse::after {
    content: "";
    position: absolute;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: rgba(239, 68, 68, 0.5);
    animation: pulseAnim 1.8s infinite;
}

.pulse::after {
    animation-delay: 0.9s;
}

@keyframes pulseAnim {
    0% {
        transform: scale(0.6);
        opacity: 0.7;
    }
    70% {
        transform: scale(2.6);
        opacity: 0;
    }
    100% {
        opacity: 0;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div class="card">
    <div class="title-text">🔐 Real-Time Account Takeover Detection</div>
    <div class="sub-text">
        Production-grade risk engine with strict rules, anomaly detection, and decision intelligence.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# INPUT + RESULT
# =========================
left, right = st.columns([1, 2])

with left:
    st.markdown("### 🧾 Login Event Input")

    with st.container():
        failed_attempts = st.slider("Failed Attempts", 0, 5, 1)
        geo_velocity_flag = 1 if st.toggle("Geo Velocity / New Location") else 0
        device_novelty_flag = 1 if st.toggle("New Device") else 0
        ip_risk = st.slider("IP Risk", 0, 5, 1)
        login_time_risk = st.slider("Login Time Risk", 0, 5, 1)
        account_age_risk = st.slider("Account Age Risk", 0, 5, 1)

        evaluate = st.button("Evaluate Login Risk", use_container_width=True)

with right:
    st.markdown("### 🔍 Risk Evaluation Result")

    if evaluate:
        payload = {
            "failed_attempts": failed_attempts,
            "geo_velocity_flag": geo_velocity_flag,
            "device_novelty_flag": device_novelty_flag,
            "ip_risk": ip_risk,
            "login_time_risk": login_time_risk,
            "account_age_risk": account_age_risk
        }

        try:
            response = requests.post(
                "http://127.0.0.1:8000/score_login",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            risk_score = result["risk_score"]
            risk_percentage = result["risk_percentage"]
            decision = result["decision"]
            message = result["message"]

            c1, c2, c3 = st.columns(3)
            c1.metric("Risk Score", risk_score)
            c2.metric("Risk %", f"{risk_percentage}%")
            c3.metric("Decision", decision)

            if decision == "BLOCK":
                st.error(f"🚫 {message}")

                st.markdown("""
                <div class="pulse-container">
                    <div class="pulse"></div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("### 🚨 High Risk Detected")

            elif decision == "MFA":
                st.warning(f"⚠️ {message}")
                st.markdown("### 🔐 MFA Required")

            else:
                st.success(f"✅ {message}")
                st.markdown("### ✅ Login Allowed")

            st.markdown("### 📌 Input Summary")
            st.dataframe(pd.DataFrame([payload]), use_container_width=True)

        except Exception as e:
            st.error(f"Backend error: {e}")

# =========================
# DASHBOARD
# =========================
st.markdown("### 📊 Monitoring Dashboard")

try:
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM login_predictions ORDER BY timestamp DESC",
        conn
    )

    conn.close()

    if not df.empty:
        col1, col2 = st.columns(2)

        col1.bar_chart(df["decision"].value_counts())

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        col2.line_chart(df.sort_values("timestamp").set_index("timestamp")["risk_percentage"])

        st.dataframe(df.head(10), use_container_width=True)

    else:
        st.info("No data yet.")

except:
    st.info("Run backend first.")
