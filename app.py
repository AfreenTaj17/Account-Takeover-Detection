import streamlit as st
import requests
import sqlite3
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="ATO Detection System",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: linear-gradient(-45deg, #0f172a, #020617, #1e293b, #111827);
    background-size: 400% 400%;
    animation: gradientFlow 18s ease infinite;
    color: white;
}

@keyframes gradientFlow {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.stApp::before {
    content: "";
    position: fixed;
    width: 650px;
    height: 650px;
    background: radial-gradient(circle, rgba(59,130,246,0.16), transparent 60%);
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

.block-container {
    padding-top: 2rem;
    position: relative;
    z-index: 1;
}

.card {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 24px;
    border: 1px solid rgba(255,255,255,0.14);
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
    backdrop-filter: blur(10px);
    margin-bottom: 18px;
}

.title-text {
    font-size: 42px;
    font-weight: 800;
}

.sub-text {
    color: #cbd5e1;
    font-size: 16px;
}

.pulse-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 28px;
    margin-bottom: 20px;
}

.pulse {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: rgba(239, 68, 68, 0.25);
    position: relative;
}

.pulse::before, .pulse::after {
    content: "";
    position: absolute;
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: rgba(239, 68, 68, 0.45);
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
        transform: scale(2.5);
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
        Strict rule-based risk engine for login risk scoring, MFA decisioning, and account takeover prevention.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# INPUT + RESULT
# =========================
left, right = st.columns([1, 2])

with left:
    st.markdown("### 🧾 Login Event Input")

    with st.container(border=True):
        failed_attempts = st.slider(
            "Failed Attempts",
            min_value=0,
            max_value=5,
            value=1,
            step=1
        )

        geo_velocity_flag = 1 if st.toggle("Geo Velocity / New Location") else 0
        device_novelty_flag = 1 if st.toggle("New Device") else 0

        ip_risk = st.slider(
            "IP Risk",
            min_value=0,
            max_value=5,
            value=1,
            step=1
        )

        login_time_risk = st.slider(
            "Login Time Risk",
            min_value=0,
            max_value=5,
            value=1,
            step=1
        )

        account_age_risk = st.slider(
            "Account Age Risk",
            min_value=0,
            max_value=5,
            value=1,
            step=1
        )

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

            result = response.json()

            if "error" in result:
                st.error(f"Backend Error: {result['error']}")
                st.stop()

            risk_score = result["risk_score"]
            risk_percentage = result["risk_percentage"]
            decision = result["decision"]
            message = result["message"]

            c1, c2, c3 = st.columns(3)

            c1.metric("Risk Score", risk_score)
            c2.metric("Risk Percentage", f"{risk_percentage}%")
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
            st.error(f"Backend connection failed: {e}")

    else:
        st.info("Set login event values and click Evaluate Login Risk.")

# =========================
# DASHBOARD
# =========================
st.markdown("### 📊 Monitoring Dashboard")

try:
    db_path = Path("../api/ato_monitoring.db")
    conn = sqlite3.connect(db_path)

    dashboard_df = pd.read_sql_query(
        "SELECT * FROM login_predictions ORDER BY timestamp DESC",
        conn
    )

    conn.close()

    if not dashboard_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Decision Distribution")
            st.bar_chart(dashboard_df["decision"].value_counts())

        with col2:
            st.markdown("#### Risk Score Trend")
            dashboard_df["timestamp"] = pd.to_datetime(dashboard_df["timestamp"])
            st.line_chart(
                dashboard_df.sort_values("timestamp")
                .set_index("timestamp")["risk_percentage"]
            )

        st.markdown("#### Recent Predictions")
        st.dataframe(dashboard_df.head(10), use_container_width=True)

    else:
        st.info("No predictions logged yet.")

except Exception:
    st.info("Run backend and generate predictions first.")