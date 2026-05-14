import streamlit as st
from Prediction_helper import predict

# ── Page Configuration ─────────────────────────────────────────────
st.set_page_config(
    page_title="HealthShield Premium Estimator",
    page_icon="🫀",
    layout="wide"
)

# ── Custom Styling ─────────────────────────────────────────────────
st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"]{
    background-color:#0d1117;
    color:white;
    font-family:Arial;
}

.hero{
    background:linear-gradient(135deg,#00d4aa22,#0088ff22);
    padding:30px;
    border-radius:20px;
    margin-bottom:25px;
    border:1px solid #00d4aa55;
}

.hero-title{
    font-size:42px;
    font-weight:bold;
    color:white;
}

.hero-sub{
    color:#cccccc;
    font-size:16px;
}

.card{
    background:#161b22;
    padding:20px;
    border-radius:15px;
    border:1px solid #2d333b;
    margin-bottom:20px;
}

.section-title{
    color:#00d4aa;
    font-size:14px;
    letter-spacing:2px;
    margin-bottom:15px;
    font-weight:bold;
}

.result-card{
    background:linear-gradient(135deg,#00d4aa22,#0088ff22);
    padding:35px;
    border-radius:20px;
    text-align:center;
    border:1px solid #00d4aa66;
}

.result-amount{
    font-size:48px;
    color:#00d4aa;
    font-weight:bold;
}

.low{
    color:#00d4aa;
}

.medium{
    color:#fbbf24;
}

.high{
    color:#ef4444;
}

div[data-testid="stButton"] button{
    width:100%;
    height:55px;
    border-radius:12px;
    background:linear-gradient(135deg,#00d4aa,#0099ff);
    color:black;
    font-size:18px;
    font-weight:bold;
    border:none;
}

</style>
""", unsafe_allow_html=True)

# ── Dropdown Options ───────────────────────────────────────────────
categorical_options = {
    "Gender": ["Male", "Female"],

    "Marital Status": ["Unmarried", "Married"],

    "BMI Category": [
        "Normal",
        "Obesity",
        "Overweight",
        "Underweight"
    ],

    "Smoking Status": [
        "No Smoking",
        "Regular",
        "Occasional"
    ],

    "Employment Status": [
        "Salaried",
        "Self-Employed",
        "Freelancer"
    ],

    "Region": [
        "Northwest",
        "Southeast",
        "Northeast",
        "Southwest"
    ],

    "Medical History": [
        "No Disease",
        "Diabetes",
        "High blood pressure",
        "Diabetes & High blood pressure",
        "Thyroid",
        "Heart disease",
        "High blood pressure & Heart disease",
        "Diabetes & Thyroid",
        "Diabetes & Heart disease"
    ],

    "Insurance Plan": [
        "Bronze",
        "Silver",
        "Gold"
    ]
}

# ── Risk Calculator ────────────────────────────────────────────────
def get_risk_level(user_age,
                   bmi_value,
                   smoking_value,
                   medical_value,
                   genetic_value):

    score = 0

    if user_age > 55:
        score += 2

    elif user_age > 40:
        score += 1

    if bmi_value == "Obesity":
        score += 2

    elif bmi_value == "Overweight":
        score += 1

    if smoking_value == "Regular":
        score += 3

    elif smoking_value == "Occasional":
        score += 1

    if "Heart disease" in medical_value:
        score += 3

    if "Diabetes" in medical_value:
        score += 2

    if "High blood pressure" in medical_value:
        score += 1

    score += genetic_value

    if score <= 3:
        return "🟢 Low Risk", "low"

    elif score <= 7:
        return "🟡 Moderate Risk", "medium"

    else:
        return "🔴 High Risk", "high"

# ── Hero Section ──────────────────────────────────────────────────
st.markdown("""
<div class="hero">

    <div class="hero-title">
        🫀 HealthShield Premium Calculator
    </div>

    <div class="hero-sub">
        AI-powered health insurance premium prediction system
    </div>

</div>
""", unsafe_allow_html=True)

# ── Input Form ────────────────────────────────────────────────────
with st.form("prediction_form"):

    # Personal Section
    st.markdown(
        '<div class="section-title">PERSONAL PROFILE</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=30,
            step=1
        )

    with col2:
        gender = st.selectbox(
            "Gender",
            categorical_options["Gender"]
        )

    with col3:
        marital_status = st.selectbox(
            "Marital Status",
            categorical_options["Marital Status"]
        )

    with col4:
        number_of_dependants = st.number_input(
            "Dependants",
            min_value=0,
            max_value=20,
            value=0,
            step=1
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Financial Section
    st.markdown(
        '<div class="section-title">FINANCIAL DETAILS</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col5, col6, col7 = st.columns(3)

    with col5:
        income_lakhs = st.number_input(
            "Income in Lakhs",
            min_value=0.0,
            max_value=200.0,
            value=5.0,
            step=1.0
        )

    with col6:
        employment_status = st.selectbox(
            "Employment Status",
            categorical_options["Employment Status"]
        )

    with col7:
        region = st.selectbox(
            "Region",
            categorical_options["Region"]
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Health Section
    st.markdown(
        '<div class="section-title">HEALTH PROFILE</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col8, col9, col10, col11 = st.columns(4)

    with col8:
        bmi_category = st.selectbox(
            "BMI Category",
            categorical_options["BMI Category"]
        )

    with col9:
        smoking_status = st.selectbox(
            "Smoking Status",
            categorical_options["Smoking Status"]
        )

    with col10:
        medical_history = st.selectbox(
            "Medical History",
            categorical_options["Medical History"]
        )

    with col11:
        genetical_risk = st.number_input(
            "Genetical Risk",
            min_value=0,
            max_value=5,
            value=0,
            step=1
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Plan Section
    st.markdown(
        '<div class="section-title">INSURANCE PLAN</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    insurance_plan = st.selectbox(
        "Insurance Plan",
        categorical_options["Insurance Plan"]
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Risk Indicator
    risk_text, risk_class = get_risk_level(
        int(age),
        bmi_category,
        smoking_status,
        medical_history,
        int(genetical_risk)
    )

    st.markdown(f"""
    <div class="card">

        <h3>Live Risk Analysis</h3>

        <h2 class="{risk_class}">
            {risk_text}
        </h2>

    </div>
    """, unsafe_allow_html=True)

    submitted = st.form_submit_button("🔍 Calculate Premium")

# ── Prediction Section ────────────────────────────────────────────
if submitted:

    input_dict = {
        "Age": int(age),
        "Number of Dependants": int(number_of_dependants),
        "Income in Lakhs": float(income_lakhs),
        "Genetical Risk": int(genetical_risk),
        "Insurance Plan": insurance_plan,
        "Employment Status": employment_status,
        "Gender": gender,
        "Marital Status": marital_status,
        "BMI Category": bmi_category,
        "Smoking Status": smoking_status,
        "Region": region,
        "Medical History": medical_history
    }

    with st.spinner("Predicting premium..."):

        prediction = predict(input_dict)

    prediction_value = float(prediction)

    formatted_prediction = f"{prediction_value:,.0f}"

    risk_text, risk_class = get_risk_level(
        int(age),
        bmi_category,
        smoking_status,
        medical_history,
        int(genetical_risk)
    )

    st.markdown(f"""
    <div class="result-card">

        <h3>Estimated Annual Premium</h3>

        <div class="result-amount">
            ₹ {formatted_prediction}
        </div>

        <h2 class="{risk_class}">
            {risk_text}
        </h2>

    </div>
    """, unsafe_allow_html=True)