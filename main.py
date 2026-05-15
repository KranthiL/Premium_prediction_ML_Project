from typing import cast
import streamlit as st
from Prediction_helper import predict

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HealthShield AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS (Enhanced & Fixed)
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Poppins', sans-serif;
        background-color: #f4f8fb;
    }

    [data-testid="stAppViewContainer"] {
        background-image: 
            linear-gradient(rgba(255,255,255,0.90), rgba(255,255,255,0.90)),
            url('https://images.unsplash.com/photo-1631815588090-d4bfec5b1ccb?q=80&w=1974&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    #MainMenu, footer, header {visibility: hidden;}

    /* Hero */
    .hero-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.97), rgba(240,248,255,0.95));
        border-radius: 28px;
        padding: 48px 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.7);
        backdrop-filter: blur(16px);
        margin-bottom: 32px;
        animation: fadeIn 1s ease;
    }

    .hero-title {
        font-size: 54px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 12px;
    }
    .hero-title span { color: #0ea5e9; }

    .hero-subtitle {
        font-size: 18.5px;
        color: #475569;
        line-height: 1.75;
        max-width: 720px;
    }

    /* Cards */
    .card {
        background: rgba(255,255,255,0.95);
        border-radius: 24px;
        padding: 32px;
        margin-bottom: 28px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.07);
        border: 1px solid rgba(226,232,240,0.9);
        transition: all 0.3s ease;
    }
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 35px rgba(14,165,233,0.12);
    }

    .section-title {
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: #0284c7;
        margin-bottom: 24px;
        text-transform: uppercase;
    }

    /* Input Styling */
    .stNumberInput input, 
    .stSelectbox div[data-baseweb="select"] > div {
        background: #f8fafc !important;
        border: 2px solid #dbeafe !important;
        border-radius: 16px !important;
        min-height: 54px !important;
        font-size: 16px !important;
        color: #0f172a !important;
    }

    .stNumberInput input:focus,
    .stSelectbox div[data-baseweb="select"] > div:focus-within {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 4px rgba(14,165,233,0.15) !important;
        background: white !important;
    }

    label p {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 14.5px !important;
    }

    /* Button */
    div[data-testid="stButton"] > button {
        width: 100%;
        height: 62px;
        border: none;
        border-radius: 20px;
        background: linear-gradient(135deg, #0ea5e9, #06b6d4);
        color: white;
        font-size: 20px;
        font-weight: 700;
        box-shadow: 0 10px 30px rgba(14,165,233,0.3);
        transition: all 0.3s ease;
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 18px 45px rgba(14,165,233,0.4);
        background: linear-gradient(135deg, #0284c7, #0891b2);
    }

    /* Result Card */
    .result-card {
        background: linear-gradient(135deg, #ecfeff, #f0fdf4);
        border-radius: 32px;
        padding: 48px 40px;
        text-align: center;
        border: 1px solid #bae6fd;
        box-shadow: 0 15px 40px rgba(14,165,233,0.15);
        animation: pulseCard 0.8s ease;
    }

    .result-title {
        font-size: 18px;
        font-weight: 600;
        color: #0369a1;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .result-value {
        font-size: 68px;
        font-weight: 700;
        color: #0f172a;
        margin: 16px 0;
    }

    /* Risk Pills */
    .risk-low { background: #dcfce7; color: #15803d; }
    .risk-medium { background: #fef9c3; color: #ca8a04; }
    .risk-high { background: #fee2e2; color: #dc2626; }

    .risk-pill {
        padding: 12px 24px;
        border-radius: 9999px;
        display: inline-block;
        font-weight: 700;
        font-size: 18px;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulseCard {
        0% { transform: scale(0.95); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# OPTIONS
# ─────────────────────────────────────────────────────────────
categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Overweight', 'Obesity', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Occasional', 'Regular'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer'],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High blood pressure',
        'Diabetes & High blood pressure', 'Thyroid',
        'Heart disease', 'High blood pressure & Heart disease',
        'Diabetes & Thyroid', 'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}


# ─────────────────────────────────────────────────────────────
# RISK LEVEL
# ─────────────────────────────────────────────────────────────
def get_risk_level(age, bmi, smoking, medical, genetical_risk):
    score = 0
    if age > 55:
        score += 2
    elif age > 40:
        score += 1

    if bmi == 'Obesity':
        score += 2
    elif bmi == 'Overweight':
        score += 1

    if smoking == 'Regular':
        score += 3
    elif smoking == 'Occasional':
        score += 1

    if 'Heart disease' in medical: score += 3
    if 'Diabetes' in medical: score += 2
    if 'High blood pressure' in medical: score += 1

    score += genetical_risk

    if score <= 3:
        return '🟢 Low Risk', 'risk-low'
    elif score <= 7:
        return '🟡 Moderate Risk', 'risk-medium'
    else:
        return '🔴 High Risk', 'risk-high'


# ─────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-title">HealthShield <span>AI</span></div>
    <div class="hero-subtitle">
        Get an accurate AI-powered estimate of your health insurance premium 
        using advanced machine learning and comprehensive health-risk analysis.
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FORM
# ─────────────────────────────────────────────────────────────
with st.form("prediction_form"):
    # Personal Information
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👤 Personal Information</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1)
    with col2:
        gender = st.selectbox("Gender", categorical_options['Gender'])
    with col3:
        marital_status = st.selectbox("Marital Status", categorical_options['Marital Status'])
    with col4:
        number_of_dependants = st.number_input("Number of Dependants", min_value=0, max_value=20, value=0, step=1)

    st.markdown('</div>', unsafe_allow_html=True)

    # Financial Information
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💼 Financial Information</div>', unsafe_allow_html=True)

    col5, col6, col7 = st.columns(3)
    with col5:
        income_lakhs = st.number_input("Income in Lakhs (₹)", min_value=0.0, max_value=200.0, value=5.0, step=0.5)
    with col6:
        employment_status = st.selectbox("Employment Status", categorical_options['Employment Status'])
    with col7:
        region = st.selectbox("Region", categorical_options['Region'])

    st.markdown('</div>', unsafe_allow_html=True)

    # Health Information
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🩺 Health Information</div>', unsafe_allow_html=True)

    col8, col9, col10, col11 = st.columns(4)
    with col8:
        bmi_category = st.selectbox("BMI Category", categorical_options['BMI Category'])
    with col9:
        smoking_status = st.selectbox("Smoking Status", categorical_options['Smoking Status'])
    with col10:
        medical_history = st.selectbox("Medical History", categorical_options['Medical History'])
    with col11:
        genetical_risk = st.number_input("Genetical Risk (0-5)", min_value=0, max_value=5, value=0, step=1)

    st.markdown('</div>', unsafe_allow_html=True)

    # Insurance Plan
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Insurance Plan</div>', unsafe_allow_html=True)
    insurance_plan = st.selectbox("Select Plan", categorical_options['Insurance Plan'])
    st.markdown('</div>', unsafe_allow_html=True)

    # Live Risk Indicator
    risk_text, risk_class = get_risk_level(age, bmi_category, smoking_status, medical_history, genetical_risk)
    st.markdown(f'''
    <div class="card" style="text-align:center; padding: 24px;">
        <h3 style="color:#334155; margin-bottom:12px;">Current Health Risk Assessment</h3>
        <div class="risk-pill {risk_class}">{risk_text}</div>
    </div>
    ''', unsafe_allow_html=True)

    # Submit Button
    submitted = st.form_submit_button("🔍 Predict My Premium")

# ─────────────────────────────────────────────────────────────
# PREDICTION
# ─────────────────────────────────────────────────────────────
if submitted:
    input_dict = {
        'Age': int(age),
        'Number of Dependants': int(number_of_dependants),
        'Income in Lakhs': float(income_lakhs),
        'Genetical Risk': int(genetical_risk),
        'Insurance Plan': insurance_plan,
        'Employment Status': employment_status,
        'Gender': gender,
        'Marital Status': marital_status,
        'BMI Category': bmi_category,
        'Smoking Status': smoking_status,
        'Region': region,
        'Medical History': medical_history
    }

    with st.spinner("Analyzing your profile with AI..."):
        prediction = predict(input_dict)

    prediction_value = float(prediction)
    formatted_prediction = f"{prediction_value:,.0f}"

    st.markdown(f'''
    <div class="result-card">
        <div class="result-title">Estimated Annual Premium</div>
        <div class="result-value">₹ {formatted_prediction}</div>
        <div class="result-note">
            This is an AI-generated estimate based on your profile. 
            Actual premium may vary.
        </div>
    </div>
    ''', unsafe_allow_html=True)