# Account Takeover Detection System



Machine learning-based account takeover detection system using behavioral login features, risk scoring, FastAPI backend, and Streamlit frontend.

### 🚀 Try the Project

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://account-takeover-detection-app.streamlit.app/)

[![API Docs](https://img.shields.io/badge/API%20Docs-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://ato-detection-api.vercel.app/docs)

## Project Overview

Account Takeover (ATO) is a cybersecurity threat where an attacker gains unauthorized access to a user's account. This project identifies suspicious login behavior and assigns a risk score to each login attempt.

Based on the calculated risk score, the system classifies the login attempt into one of three actions:

- ALLOW
- MFA
- BLOCK

## Key Features

- Login risk prediction using machine learning
- Behavioral feature-based fraud detection
- Risk score generation
- Adaptive authentication decision logic
- FastAPI backend for real-time prediction
- Streamlit frontend for user-friendly interaction
- SQLite logging for storing prediction results

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Logistic Regression
- Random Forest
- FastAPI
- Streamlit
- SQLite
- Joblib

## Machine Learning Approach

The project uses behavioral and login-related features such as:

- Device novelty
- Location risk
- Failed login attempts
- Login time deviation
- IP reputation risk
- Account age risk

The model predicts the probability of risky login behavior and converts it into a risk score.

## Decision Logic

The risk score is mapped into authentication actions:

- Risk score below 0.30 → ALLOW
- Risk score between 0.30 and 0.70 → MFA
- Risk score above 0.70 → BLOCK

## Project Workflow

1. Data collection and preprocessing
2. Feature engineering
3. Model training
4. Model evaluation
5. Risk score calculation
6. FastAPI backend development
7. Streamlit frontend development
8. Prediction logging and monitoring

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Account-Takeover-Detection.git
cd Account-Takeover-Detection
