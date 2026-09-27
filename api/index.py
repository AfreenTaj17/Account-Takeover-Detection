```python
from fastapi import FastAPI
from pydantic import BaseModel, Field


# =====================================================
# INIT FASTAPI APP
# =====================================================

app = FastAPI(title="ATO Detection API - Rule Based")


# =====================================================
# INPUT SCHEMA
# =====================================================

class LoginEvent(BaseModel):
    failed_attempts: int = Field(..., ge=0, le=5)
    geo_velocity_flag: int = Field(..., ge=0, le=1)
    device_novelty_flag: int = Field(..., ge=0, le=1)
    ip_risk: int = Field(..., ge=0, le=5)
    login_time_risk: int = Field(..., ge=0, le=5)
    account_age_risk: int = Field(..., ge=0, le=5)


# =====================================================
# DECISION LOGIC
# =====================================================

def make_decision(features):

    failed = features["failed_attempts"]
    geo = features["geo_velocity_flag"]
    device = features["device_novelty_flag"]
    ip = features["ip_risk"]
    login_time = features["login_time_risk"]
    age = features["account_age_risk"]

    # High-impact features: 20% each
    # Medium-impact features: 10% each

    risk_score = 0

    risk_score += (failed / 5) * 0.20
    risk_score += geo * 0.20
    risk_score += device * 0.20
    risk_score += (ip / 5) * 0.10
    risk_score += (login_time / 5) * 0.10
    risk_score += (age / 5) * 0.10

    # Normalize from 0.90 max to 1.00
    risk_score = risk_score / 0.90

    # =================================================
    # STRICT FEATURE BRANCHING
    # =================================================

    if failed > 2:

        if geo == 1 and device == 1:
            return (
                risk_score,
                "BLOCK",
                ["Failed attempts above 2 with geo velocity and new device anomaly"]
            )

        if geo == 1:
            return (
                risk_score,
                "BLOCK",
                ["Failed attempts above 2 with geo velocity anomaly"]
            )

        if device == 1:
            return (
                risk_score,
                "BLOCK",
                ["Failed attempts above 2 with new device anomaly"]
            )

        if ip >= 4 or login_time >= 4:
            return (
                risk_score,
                "BLOCK",
                ["Failed attempts above 2 with high supporting risk"]
            )

        return (
            risk_score,
            "MFA",
            ["Failed attempts above 2"]
        )

    # =================================================
    # LOW FAILED ATTEMPT BRANCH
    # =================================================

    if failed <= 2:

        if geo == 1:

            if device == 1:
                return (
                    risk_score,
                    "BLOCK",
                    ["Geo velocity and new device anomaly"]
                )

            if ip >= 4:
                return (
                    risk_score,
                    "MFA",
                    ["Geo velocity anomaly with suspicious IP"]
                )

            if login_time >= 4:
                return (
                    risk_score,
                    "MFA",
                    ["Geo velocity anomaly with unusual login time"]
                )

            return (
                risk_score,
                "MFA",
                ["Geo velocity anomaly"]
            )

        if device == 1:

            if ip >= 4:
                return (
                    risk_score,
                    "MFA",
                    ["New device with suspicious IP"]
                )

            if login_time >= 4:
                return (
                    risk_score,
                    "MFA",
                    ["New device with unusual login time"]
                )

            if age >= 4:
                return (
                    risk_score,
                    "MFA",
                    ["New device with high account age risk"]
                )

            return (
                risk_score,
                "MFA",
                ["New device detected"]
            )

        medium_total = ip + login_time + age

        if medium_total <= 3:
            return (
                risk_score,
                "ALLOW",
                ["Low failed attempts and low supporting risk"]
            )

        if 4 <= medium_total <= 6:
            return (
                risk_score,
                "MFA",
                ["Medium supporting risk detected"]
            )

        return (
            risk_score,
            "BLOCK",
            ["High combined supporting risk"]
        )

    # =================================================
    # FALLBACK
    # =================================================

    if risk_score <= 0.40:
        return (
            risk_score,
            "ALLOW",
            ["Risk score within allow range"]
        )

    elif risk_score <= 0.60:
        return (
            risk_score,
            "MFA",
            ["Risk score within MFA range"]
        )

    return (
        risk_score,
        "BLOCK",
        ["Risk score within block range"]
    )


# =====================================================
# HOME ENDPOINT
# =====================================================

@app.get("/")
def home():

    return {
        "status": "ATO Detection API is running",
        "mode": "strict_rule_based",
        "database": "disabled_for_serverless_demo"
    }


# =====================================================
# SCORE LOGIN ENDPOINT
# =====================================================

@app.post("/score_login")
def score_login(event: LoginEvent):

    try:

        # Convert Pydantic model to dictionary
        try:
            input_dict = event.model_dump()
        except AttributeError:
            input_dict = event.dict()

        # Run ATO detection logic
        risk_score, decision, reasons = make_decision(input_dict)

        message = ", ".join(reasons)

        # =================================================
        # LIVE API RESPONSE
        # =================================================

        return {
            "risk_score": round(float(risk_score), 4),
            "risk_percentage": round(float(risk_score) * 100, 2),
            "decision": decision,
            "message": message
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# =====================================================
# PREDICTIONS ENDPOINT
# =====================================================

@app.get("/predictions")
def get_predictions():

    return {
        "message": "Prediction history is disabled for the serverless demo.",
        "predictions": []
    }
```

