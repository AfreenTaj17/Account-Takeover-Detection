import streamlit as st
import requests
import pandas as pd
from datetime import datetime


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ATO Detection System",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# API CONFIGURATION
# =========================================================

API_URL = "https://ato-detection-api.vercel.app"


# =========================================================
# SESSION STATE
# =========================================================

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .stApp {
        background:
            linear-gradient(
                -45deg,
                #0f172a,
                #020617,
                #1e293b,
                #111827
            );

        background-size: 400% 400%;
        animation: gradientFlow 18s ease infinite;

        color: white;
    }


    @keyframes gradientFlow {

        0% {
            background-position: 0% 50%;
        }

        50% {
            background-position: 100% 50%;
        }

        100% {
            background-position: 0% 50%;
        }

    }


    /* =====================================================
       BACKGROUND GLOW
       ===================================================== */

    .stApp::before {

        content: "";

        position: fixed;

        width: 650px;
        height: 650px;

        background:
            radial-gradient(
                circle,
                rgba(59,130,246,0.18),
                transparent 60%
            );

        top: -120px;
        left: -120px;

        animation: floatGlow 20s linear infinite;

        z-index: 0;
    }


    @keyframes floatGlow {

        0% {
            transform: translate(0,0);
        }

        50% {
            transform: translate(350px,220px);
        }

        100% {
            transform: translate(0,0);
        }

    }


    /* =====================================================
       MAIN CONTENT
       ===================================================== */

    .block-container {

        padding-top: 2rem;
        padding-bottom: 2rem;

        position: relative;
        z-index: 1;
    }


    /* =====================================================
       HERO CARD
       ===================================================== */

    .hero-card {

        background:
            rgba(255,255,255,0.06);

        border:
            1px solid rgba(255,255,255,0.16);

        border-radius: 22px;

        padding: 30px;

        margin-bottom: 20px;

        box-shadow:
            0 12px 35px rgba(0,0,0,0.45);

        backdrop-filter: blur(14px);

        -webkit-backdrop-filter: blur(14px);
    }


    .hero-title {

        font-size: 40px;

        font-weight: 800;

        line-height: 1.2;

        color: white;

        margin-bottom: 8px;
    }


    .hero-subtitle {

        font-size: 16px;

        color: #cbd5e1;

        line-height: 1.6;

        margin-top: 5px;
    }


    /* =====================================================
       GLASS CARD
       ===================================================== */

    .glass-card {

        background:
            rgba(255,255,255,0.055);

        border:
            1px solid rgba(255,255,255,0.15);

        border-radius: 20px;

        padding: 24px;

        box-shadow:
            0 10px 30px rgba(0,0,0,0.35);

        backdrop-filter: blur(14px);

        -webkit-backdrop-filter: blur(14px);

        margin-bottom: 20px;
    }


    .glass-card:hover {

        border-color:
            rgba(255,255,255,0.23);

        box-shadow:
            0 12px 35px rgba(0,0,0,0.42);
    }


    /* =====================================================
       SECTION HEADERS
       ===================================================== */

    .section-title {

        font-size: 20px;

        font-weight: 700;

        color: white;

        margin-bottom: 18px;
    }


    /* =====================================================
       API STATUS
       ===================================================== */

    .api-status {

        display: inline-flex;

        align-items: center;

        gap: 8px;

        padding: 8px 14px;

        margin-bottom: 20px;

        border-radius: 999px;

        background:
            rgba(34,197,94,0.10);

        border:
            1px solid rgba(34,197,94,0.30);

        color: #86efac;

        font-size: 14px;

        font-weight: 600;
    }


    .status-dot {

        width: 9px;

        height: 9px;

        border-radius: 50%;

        background: #22c55e;

        box-shadow:
            0 0 10px rgba(34,197,94,0.8);
    }


    /* =====================================================
       METRICS
       ===================================================== */

    [data-testid="stMetric"] {

        background:
            rgba(255,255,255,0.07);

        border:
            1px solid rgba(255,255,255,0.17);

        padding: 16px;

        border-radius: 16px;

        box-shadow:
            0 6px 20px rgba(0,0,0,0.30);

        backdrop-filter: blur(10px);
    }


    [data-testid="stMetricLabel"] {

        color: #cbd5e1 !important;
    }


    [data-testid="stMetricValue"] {

        color: white !important;
    }


    /* =====================================================
       INPUT CONTROLS
       ===================================================== */

    .stSlider > div {

        border:
            1px solid rgba(255,255,255,0.16);

        border-radius: 12px;

        padding: 7px;

        background:
            rgba(255,255,255,0.025);
    }


    /* =====================================================
       BUTTON
       ===================================================== */

    .stButton > button {

        border-radius: 12px;

        border:
            1px solid rgba(255,255,255,0.20);

        background:
            rgba(59,130,246,0.20);

        color: white;

        font-weight: 700;

        padding: 10px 18px;

        transition:
            all 0.2s ease;
    }


    .stButton > button:hover {

        border-color:
            rgba(96,165,250,0.60);

        background:
            rgba(59,130,246,0.32);

        transform:
            translateY(-1px);

        box-shadow:
            0 8px 20px rgba(0,0,0,0.30);
    }


    /* =====================================================
       DATAFRAME
       ===================================================== */

    [data-testid="stDataFrame"] {

        border:
            1px solid rgba(255,255,255,0.14);

        border-radius: 14px;

        overflow: hidden;

        box-shadow:
            0 6px 20px rgba(0,0,0,0.25);
    }


    /* =====================================================
       ALERT BOXES
       ===================================================== */

    [data-testid="stAlert"] {

        border-radius: 14px;
    }


    /* =====================================================
       BLOCK PULSE
       ===================================================== */

    .pulse-container {

        display: flex;

        justify-content: center;

        align-items: center;

        margin-top: 30px;

        margin-bottom: 20px;
    }


    .pulse {

        width: 120px;

        height: 120px;

        border-radius: 50%;

        background:
            rgba(239,68,68,0.25);

        position: relative;
    }


    .pulse::before,
    .pulse::after {

        content: "";

        position: absolute;

        width: 120px;

        height: 120px;

        border-radius: 50%;

        background:
            rgba(239,68,68,0.5);

        animation:
            pulseAnim 1.8s infinite;
    }


    .pulse::after {

        animation-delay:
            0.9s;
    }


    @keyframes pulseAnim {

        0% {

            transform:
                scale(0.6);

            opacity:
                0.7;
        }

        70% {

            transform:
                scale(2.6);

            opacity:
                0;
        }

        100% {

            opacity:
                0;
        }

    }


    /* =====================================================
       DASHBOARD CARD
       ===================================================== */

    .dashboard-card {

        background:
            rgba(255,255,255,0.045);

        border:
            1px solid rgba(255,255,255,0.14);

        border-radius: 20px;

        padding: 24px;

        margin-top: 10px;

        margin-bottom: 20px;

        box-shadow:
            0 10px 30px rgba(0,0,0,0.32);

        backdrop-filter: blur(12px);

        -webkit-backdrop-filter: blur(12px);
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .custom-footer {

        text-align: center;

        color: #64748b;

        font-size: 13px;

        padding: 20px 0 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HERO HEADER
# =========================================================
#
# IMPORTANT:
# Header text uses ONLY native Streamlit Markdown.
# No HTML tags are used here.
# =========================================================

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">
            🔐 Real-Time Account Takeover Detection
        </div>

        <div class="hero-subtitle">
            Production-grade risk engine with strict rules,
            anomaly detection, and decision intelligence.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LIVE API STATUS
# =========================================================

try:

    health_response = requests.get(
        API_URL,
        timeout=5
    )

    if health_response.status_code == 200:

        st.success(
            "🟢 Risk Engine Online — Connected to Live API"
        )

    else:

        st.warning(
            "🟡 Risk Engine responded with an unexpected status."
        )

except requests.exceptions.RequestException:

    st.error(
        "🔴 Risk Engine Offline — Unable to connect to the live API."
    )


# =========================================================
# MAIN LAYOUT
# =========================================================

left, right = st.columns(
    [1, 2],
    gap="large"
)


# =========================================================
# LOGIN EVENT INPUT
# =========================================================

with left:

    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">
                🧾 Login Event Input
            </div>
        """,
        unsafe_allow_html=True
    )

    failed_attempts = st.slider(
        "Failed Attempts",
        0,
        5,
        1
    )

    geo_velocity_flag = (
        1
        if st.toggle(
            "Geo Velocity / New Location"
        )
        else 0
    )

    device_novelty_flag = (
        1
        if st.toggle(
            "New Device"
        )
        else 0
    )

    ip_risk = st.slider(
        "IP Risk",
        0,
        5,
        1
    )

    login_time_risk = st.slider(
        "Login Time Risk",
        0,
        5,
        1
    )

    account_age_risk = st.slider(
        "Account Age Risk",
        0,
        5,
        1
    )

    evaluate = st.button(
        "🔍 Evaluate Login Risk",
        use_container_width=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# RISK RESULT
# =========================================================

with right:

    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">
                🔍 Risk Evaluation Result
            </div>
        """,
        unsafe_allow_html=True
    )

    if evaluate:

        payload = {

            "failed_attempts":
                failed_attempts,

            "geo_velocity_flag":
                geo_velocity_flag,

            "device_novelty_flag":
                device_novelty_flag,

            "ip_risk":
                ip_risk,

            "login_time_risk":
                login_time_risk,

            "account_age_risk":
                account_age_risk
        }

        try:

            response = requests.post(
                f"{API_URL}/score_login",
                json=payload,
                timeout=15
            )

            response.raise_for_status()

            result = response.json()

            risk_score = result.get(
                "risk_score",
                0
            )

            risk_percentage = result.get(
                "risk_percentage",
                0
            )

            decision = result.get(
                "decision",
                "UNKNOWN"
            )

            message = result.get(
                "message",
                "No explanation provided."
            )


            # -------------------------------------------------
            # STORE RESULT
            # -------------------------------------------------

            st.session_state.prediction_history.append({

                "timestamp":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                "failed_attempts":
                    failed_attempts,

                "geo_velocity_flag":
                    geo_velocity_flag,

                "device_novelty_flag":
                    device_novelty_flag,

                "ip_risk":
                    ip_risk,

                "login_time_risk":
                    login_time_risk,

                "account_age_risk":
                    account_age_risk,

                "risk_score":
                    risk_score,

                "risk_percentage":
                    risk_percentage,

                "decision":
                    decision
            })


            # -------------------------------------------------
            # RESULT METRICS
            # -------------------------------------------------

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Risk Score",
                f"{risk_score:.4f}"
            )

            c2.metric(
                "Risk %",
                f"{risk_percentage:.2f}%"
            )

            c3.metric(
                "Decision",
                decision
            )


            # -------------------------------------------------
            # DECISION
            # -------------------------------------------------

            if decision == "BLOCK":

                st.error(
                    f"🚫 {message}"
                )

                st.markdown(
                    """
                    <div class="pulse-container">
                        <div class="pulse"></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    "### 🚨 High Risk Detected"
                )


            elif decision == "MFA":

                st.warning(
                    f"⚠️ {message}"
                )

                st.markdown(
                    "### 🔐 MFA Required"
                )


            elif decision == "ALLOW":

                st.success(
                    f"✅ {message}"
                )

                st.markdown(
                    "### ✅ Login Allowed"
                )


            else:

                st.info(
                    message
                )


            # -------------------------------------------------
            # INPUT SUMMARY
            # -------------------------------------------------

            st.markdown(
                "### 📌 Input Summary"
            )

            st.dataframe(
                pd.DataFrame([payload]),
                use_container_width=True,
                hide_index=True
            )


        except requests.exceptions.Timeout:

            st.error(
                "⏱️ The risk engine took too long to respond."
            )


        except requests.exceptions.ConnectionError:

            st.error(
                "🔴 Could not connect to the live ATO risk engine."
            )


        except requests.exceptions.HTTPError as e:

            st.error(
                f"🔴 API returned an HTTP error: {e}"
            )


        except Exception as e:

            st.error(
                f"Unexpected error: {e}"
            )


    else:

        st.info(
            "Configure the login event parameters and click "
            "**Evaluate Login Risk** to analyze the login."
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# MONITORING DASHBOARD
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div class="dashboard-card">
        <div class="section-title">
            📊 Monitoring Dashboard
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


history = st.session_state.prediction_history


if history:

    df = pd.DataFrame(history)


    # -----------------------------------------------------
    # DASHBOARD METRICS
    # -----------------------------------------------------

    total_predictions = len(df)

    blocked_count = len(
        df[df["decision"] == "BLOCK"]
    )

    mfa_count = len(
        df[df["decision"] == "MFA"]
    )

    allowed_count = len(
        df[df["decision"] == "ALLOW"]
    )


    d1, d2, d3, d4 = st.columns(4)

    d1.metric(
        "Total Evaluations",
        total_predictions
    )

    d2.metric(
        "Blocked",
        blocked_count
    )

    d3.metric(
        "MFA",
        mfa_count
    )

    d4.metric(
        "Allowed",
        allowed_count
    )


    # -----------------------------------------------------
    # CHARTS
    # -----------------------------------------------------

    chart_left, chart_right = st.columns(2)


    with chart_left:

        st.markdown(
            "#### Decision Distribution"
        )

        decision_counts = (
            df["decision"]
            .value_counts()
        )

        st.bar_chart(
            decision_counts
        )


    with chart_right:

        st.markdown(
            "#### Risk Percentage Trend"
        )

        chart_df = df.copy()

        chart_df["timestamp"] = pd.to_datetime(
            chart_df["timestamp"]
        )

        chart_df = (
            chart_df
            .sort_values("timestamp")
            .set_index("timestamp")
        )

        st.line_chart(
            chart_df["risk_percentage"]
        )


    # -----------------------------------------------------
    # RECENT PREDICTIONS
    # -----------------------------------------------------

    st.markdown(
        "#### 🕐 Recent Predictions"
    )

    st.dataframe(
        df.sort_values(
            "timestamp",
            ascending=False
        ).head(10),

        use_container_width=True,

        hide_index=True
    )


else:

    st.info(
        "No predictions yet. Run a login risk evaluation "
        "to populate the monitoring dashboard."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div class="custom-footer">
        Account Takeover Detection •
        FastAPI Risk Engine + Streamlit Monitoring Interface
    </div>
    """,
    unsafe_allow_html=True
)
