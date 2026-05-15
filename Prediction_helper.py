import pandas as pd
import joblib

# =========================================================
# LOAD MODELS & SCALERS
# =========================================================

model_young = joblib.load("artifacts/model_young.joblib")
model_rest = joblib.load("artifacts/model_rest.joblib")

scaler_young = joblib.load("artifacts/scaler_young.joblib")
scaler_rest = joblib.load("artifacts/scaler_rest.joblib")


# =========================================================
# NORMALIZED RISK SCORE
# =========================================================

def calculate_normalized_risk(medical_history):

    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }

    diseases = medical_history.lower().split(" & ")

    total_risk_score = sum(
        risk_scores.get(disease, 0)
        for disease in diseases
    )

    max_score = 14
    min_score = 0

    normalized_risk_score = (
        (total_risk_score - min_score)
        / (max_score - min_score)
    )

    return normalized_risk_score


# =========================================================
# PREPROCESS INPUT
# =========================================================

def preprocess_input(input_dict):

    # IMPORTANT:
    # genetical_risk is intentionally misspelled
    # because trained scaler/model expects this column
    expected_columns = [
        'age',
        'number_of_dependants',
        'income_lakhs',
        'insurance_plan',
        'genetical_risk',
        'normalized_risk_score',
        'gender_Male',
        'region_Northwest',
        'region_Southeast',
        'region_Southwest',
        'marital_status_Unmarried',
        'bmi_category_Obesity',
        'bmi_category_Overweight',
        'bmi_category_Underweight',
        'smoking_status_Occasional',
        'smoking_status_Regular',
        'employment_status_Salaried',
        'employment_status_Self-Employed'
    ]

    insurance_plan_encoding = {
        'Bronze': 1,
        'Silver': 2,
        'Gold': 3
    }

    df = pd.DataFrame(
        0,
        columns=expected_columns,
        index=[0]
    )

    # =====================================================
    # MANUAL ENCODING
    # =====================================================

    for key, value in input_dict.items():

        # Gender
        if key == 'Gender':

            if value == 'Male':
                df['gender_Male'] = 1

        # Region
        elif key == 'Region':

            if value == 'Northwest':
                df['region_Northwest'] = 1

            elif value == 'Southeast':
                df['region_Southeast'] = 1

            elif value == 'Southwest':
                df['region_Southwest'] = 1

        # Marital Status
        elif key == 'Marital Status':

            if value == 'Unmarried':
                df['marital_status_Unmarried'] = 1

        # BMI
        elif key == 'BMI Category':

            if value == 'Obesity':
                df['bmi_category_Obesity'] = 1

            elif value == 'Overweight':
                df['bmi_category_Overweight'] = 1

            elif value == 'Underweight':
                df['bmi_category_Underweight'] = 1

        # Smoking
        elif key == 'Smoking Status':

            if value == 'Occasional':
                df['smoking_status_Occasional'] = 1

            elif value == 'Regular':
                df['smoking_status_Regular'] = 1

        # Employment
        elif key == 'Employment Status':

            if value == 'Salaried':
                df['employment_status_Salaried'] = 1

            elif value == 'Self-Employed':
                df['employment_status_Self-Employed'] = 1

        # Insurance Plan
        elif key == 'Insurance Plan':

            df['insurance_plan'] = insurance_plan_encoding.get(value, 1)

        # Numeric Features
        elif key == 'Age':

            df['age'] = int(value)

        elif key == 'Number of Dependants':

            df['number_of_dependants'] = int(value)

        elif key == 'Income in Lakhs':

            df['income_lakhs'] = float(value)

        # IMPORTANT TYPO COLUMN
        elif key == 'Genetical Risk':

            df['genetical_risk'] = int(value)

    # =====================================================
    # RISK SCORE
    # =====================================================

    df['normalized_risk_score'] = calculate_normalized_risk(
        input_dict['Medical History']
    )

    # =====================================================
    # SCALING
    # =====================================================

    df = handle_scaling(
        int(input_dict['Age']),
        df
    )

    return df


# =========================================================
# HANDLE SCALING
# =========================================================

def handle_scaling(age, df):

    if age <= 25:
        scaler_object = scaler_young

    else:
        scaler_object = scaler_rest

    # Some saved objects are dicts
    # Some are direct scalers

    if isinstance(scaler_object, dict):

        cols_to_scale = scaler_object['cols_to_scale']
        scaler = scaler_object['scaler']

    else:

        cols_to_scale = [
            'age',
            'number_of_dependants',
            'income_lakhs',
            'insurance_plan',
            'genetical_risk',
            'normalized_risk_score'
        ]

        scaler = scaler_object

    # Add dummy column if scaler expects it
    if 'income_level' in cols_to_scale:

        df['income_level'] = 0

    # Ensure all columns exist
    for col in cols_to_scale:

        if col not in df.columns:
            df[col] = 0

    # Apply scaling
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    # Remove dummy column
    if 'income_level' in df.columns:

        df.drop(
            'income_level',
            axis=1,
            inplace=True
        )

    return df


# =========================================================
# PREDICT FUNCTION
# =========================================================

def predict(input_dict):

    input_df = preprocess_input(input_dict)

    # =====================================================
    # FIX COLUMN ORDER ISSUE
    # =====================================================

    if int(input_dict['Age']) <= 25:

        model = model_young

    else:

        model = model_rest

    # Get expected columns from model
    expected_columns = model.feature_names_in_

    # Add missing columns
    for col in expected_columns:

        if col not in input_df.columns:
            input_df[col] = 0

    # Remove extra columns
    input_df = input_df[expected_columns]

    # Predict
    prediction = model.predict(input_df)

    return int(prediction[0])