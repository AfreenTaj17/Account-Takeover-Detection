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

st.markdown("""
<style>

/* Remove default UI noise */
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
   BACKGROUND
   ===================================================== */

.stApp {
    background: linear-gradient(
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
   FLOATING GLOW
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
   MAIN CONTAINER
   ===================================================== */

.block-container {

    padding-top: 2rem;

    position: relative;

    z-index: 1;
}


/* =====================================================
   CARD
   ===================================================== */

.card {

    background:
        rgba(255,255,255,0.06);

    border-radius: 20px;

    padding: 24px;

    border:
        2px solid rgba(255,255,255,0.18);

    box-shadow:

        0 8px 30px rgba(0,0,0,0.5),

        inset
        0 0 0 1px
        rgba(255,255,255,0.05);

    backdrop-filter: blur(12px);

    margin-bottom: 20px;

    transition:
        all 0.3s ease;
}

.card:hover {

    transform:
        translateY(-4px);

    box-shadow:

        0 14px 45px rgba(0,0,0,0.7),

        0 0 14px
        rgba(59,130,246,0.2);
}


/* =====================================================
   TITLE
   ===================================================== */

.title-text {

    font-size: 42px;

    font-weight: 800;
}

.sub-text {

    color: #cbd5e1;

    font-size: 16px;
}


/* =====================================================
   INPUT CONTAINER
   ===================================================== */

[data-testid="stVerticalBlock"] > div {

    border:
        2px solid
        rgba(255,255,255,0.14);

    border-radius: 16px;

    padding: 12px;

    box-shadow:
        0 6px 25px
        rgba(0,0,0,0.4);
}


/* =====================================================
   METRICS
   ===================================================== */

[data-testid="stMetric"] {

    background:
        rgba(255,255,255,0.08);

    border:
        2px solid
        rgba(255,255,255,0.18);

    padding: 14px;

    border-radius: 16px;

    box-shadow:
        0 5px 18px
        rgba(0,0,0,0.35);
}


/* =====================================================
   SLIDER
   ===================================================== */

.stSlider > div {

    border:
        1px solid
        rgba(255,255,255,0.2);

    border-radius: 12px;

    padding: 6px;
}


/* =====================================================
   STATUS CARD
   ===================================================== */

.status-card {

    padding: 12px 18px;

    border-radius: 12px;

    margin-bottom: 20px;

    background:
        rgba(255,255,255,0.06);

    border:
        1px solid
        rgba(255,255,255,0.15);
}


/* =====================================================
   BLOCK PULSE
   ===================================================== */

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
   SECTION HEADERS
   ===================================================== */

.section-title {

    font-size: 24px;

    font-weight: 700;

    margin-top: 20px;

    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================



st.markdown(
    """
    <div class="card">
        <div class="title-text">
            🔐 Real-Time Account Takeover Detection
        </div>

        <div class="sub-text">
            Production-grade risk engine with strict rules,
            anomaly detection, and decision intelligence.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# API STATUS
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
            "🟡 Risk Engine responded but returned an unexpected status."
        )

except Exception:

    st.error(
        "🔴 Risk Engine Offline — Unable to connect to the live API."
    )


# =========================================================
# LOGIN INPUT + RESULT
# =========================================================

left, right = st.columns([1, 2])


# =========================================================
# INPUT PANEL
# =========================================================

with left:

    st.markdown(
        "### 🧾 Login Event Input"
    )

    with st.container():

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


# =========================================================
# RESULT PANEL
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

        try:

            # -------------------------------------------------
            # LIVE API REQUEST
            # -------------------------------------------------

            response = requests.post(

                f"{API_URL}/score_login",

                json=payload,

                timeout=15
            )

            response.raise_for_status()

            result = response.json()


            # -------------------------------------------------
            # RESPONSE DATA
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
            # SAVE TO SESSION HISTORY
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
            # DECISION DISPLAY
            # -------------------------------------------------

            if decision == "BLOCK":

                st.error(
                    f"🚫 {message}"
                )

                st.markdown("""
                <div class="pulse-container">
                    <div class="pulse"></div>
                </div>
                """, unsafe_allow_html=True)

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


            else:

                st.success(
                    f"✅ {message}"
                )

                st.markdown(
                    "### ✅ Login Allowed"
                )


            # -------------------------------------------------
            # INPUT SUMMARY
            # -------------------------------------------------

            st.markdown(
                "### 📌 Input Summary"
            )

            st.dataframe(
                pd.DataFrame([payload]),
                use_container_width=True
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
                f"🔴 API returned an error: {e}"
            )

            try:

                st.json(
                    response.json()
                )

            except Exception:

                pass


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

        use_container_width=True
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

st.caption(
    "Account Takeover Detection • "
    "FastAPI Risk Engine + Streamlit Monitoring Interface"
)
