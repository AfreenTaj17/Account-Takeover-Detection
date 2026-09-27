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
       HIDE STREAMLIT DEFAULT ELEMENTS
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


    /* =====================================================
       MAIN BACKGROUND
       ===================================================== */

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

        animation:
            gradientFlow 18s ease infinite;

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
       FLOATING BACKGROUND GLOW
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

        animation:
            floatGlow 20s linear infinite;

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

        padding: 32px;

        margin-bottom: 20px;

        box-shadow:
            0 12px 35px rgba(0,0,0,0.45);

        backdrop-filter:
            blur(14px);
    }


    .hero-title {

        font-size: 42px;

        font-weight: 800;

        line-height: 1.15;

        margin-bottom: 10px;

        color: white;
    }


    .hero-subtitle {

        font-size: 16px;

        color: #cbd5e1;

        line-height: 1.6;

        margin: 0;
    }


    /* =====================================================
       API STATUS
       ===================================================== */

    .api-status {

        display: inline-flex;

        align-items: center;

        gap: 8px;

        padding: 8px 14px;

        margin-bottom: 22px;

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
       SECTION CARD
       ===================================================== */

    .section-card {

        background:
            rgba(255,255,255,0.05);

        border:
            1px solid rgba(255,255,255,0.13);

        border-radius: 18px;

        padding: 22px;

        margin-bottom: 20px;

        box-shadow:
            0 8px 28px rgba(0,0,0,0.35);

        backdrop-filter:
            blur(10px);
    }


    /* =====================================================
       METRICS
       ===================================================== */

    [data-testid="stMetric"] {

        background:
            rgba(255,255,255,0.07);

        border:
            1px solid rgba(255,255,255,0.15);

        padding: 14px;

        border-radius: 15px;

        box-shadow:
            0 5px 18px rgba(0,0,0,0.30);
    }


    /* =====================================================
       INPUT CONTAINERS
       ===================================================== */

    [data-testid="stVerticalBlock"] > div {

        border-radius: 14px;
    }


    /* =====================================================
       SLIDERS
       ===================================================== */

    .stSlider > div {

        border:
            1px solid rgba(255,255,255,0.15);

        border-radius: 12px;

        padding: 6px;
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

        width: 110px;

        height: 110px;

        border-radius: 50%;

        background:
            rgba(239,68,68,0.25);

        position: relative;
    }


    .pulse::before,
    .pulse::after {

        content: "";

        position: absolute;

        width: 110px;

        height: 110px;

        border-radius: 50%;

        background:
            rgba(239,68,68,0.45);

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
                scale(2.5);

            opacity:
                0;
        }

        100% {

            opacity:
                0;
        }
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
# This is the ONLY place where the subtitle HTML exists.
# It is rendered using unsafe_allow_html=True.
# =========================================================

st.markdown(
    """
    <div class="hero-card">

        <div class="hero-title">
            🔐 Real-Time Account Takeover Detection
        </div>

        <p class="hero-subtitle">
            Production-grade risk engine with strict rules,
            anomaly detection, and decision intelligence.
        </p>

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

        st.markdown(
            """
            <div class="api-status">
                <span class="status-dot"></span>
                Risk Engine Online — Connected to Live API
            </div>
            """,
            unsafe_allow_html=True
        )

        api_online = True

    else:

        st.warning(
            "🟡 Risk Engine responded with an unexpected status."
        )

        api_online = False

except requests.exceptions.RequestException:

    st.error(
        "🔴 Risk Engine Offline — Unable to connect to the live API."
    )

    api_online = False


# =========================================================
# MAIN COLUMNS
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
        "### 🧾 Login Event Input"
    )

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )

    failed_attempts = st.slider(
        "Failed Attempts",
        min_value=0,
        max_value=5,
        value=1
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
        min_value=0,
        max_value=5,
        value=1
    )

    login_time_risk = st.slider(
        "Login Time Risk",
        min_value=0,
        max_value=5,
        value=1
    )

    account_age_risk = st.slider(
        "Account Age Risk",
        min_value=0,
        max_value=5,
        value=1
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
# RISK EVALUATION RESULT
# =========================================================

with right:

    st.markdown(
        "### 🔍 Risk Evaluation Result"
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


        # -------------------------------------------------
        # CALL LIVE BACKEND
        # -------------------------------------------------

        try:

            response = requests.post(
                f"{API_URL}/score_login",
                json=payload,
                timeout=15
            )

            response.raise_for_status()

            result = response.json()


            # -------------------------------------------------
            # EXTRACT RESULT
            # -------------------------------------------------

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
            # SAVE SESSION HISTORY
            # -------------------------------------------------

            history_record = {

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
            }


            st.session_state.prediction_history.append(
                history_record
            )


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
            # DECISION MESSAGE
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


# =========================================================
# MONITORING DASHBOARD
# =========================================================

st.markdown("---")

st.markdown(
    "### 📊 Monitoring Dashboard"
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

st.markdown(
    """
    <div class="custom-footer">
        Account Takeover Detection •
        FastAPI Risk Engine + Streamlit Monitoring Interface
    </div>
    """,
    unsafe_allow_html=True
)
