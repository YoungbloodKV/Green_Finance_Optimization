import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from pulp import LpProblem, LpMaximize, LpVariable, lpSum

# Function to load and preprocess the dataset
def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path)

    # Melt the dataset to long format
    year_columns = [col for col in data.columns if '[YR' in col]
    time_series_data = data.melt(
        id_vars=['Country Name', 'Country Code', 'Series Name', 'Series Code'],
        value_vars=year_columns,
        var_name='Year',
        value_name='Value'
    )
    time_series_data['Year'] = time_series_data['Year'].str.extract(r'\[YR(\d+)\]').astype(int)
    time_series_data.dropna(subset=['Value'], inplace=True)

    # Pivot data to wide format for machine learning
    pivot_data = time_series_data.pivot_table(
        index=['Country Name', 'Series Name', 'Year'],
        values='Value'
    ).reset_index()

    # One-hot encode categorical features
    pivot_data_encoded = pd.get_dummies(pivot_data, columns=['Country Name', 'Series Name'])

    return pivot_data, pivot_data_encoded

# Function to train ESG and risk factor models
def train_models(X_train, y_train, risk_X_train, risk_y_train):
    # Train ESG Prediction Model
    rf_model_esg = RandomForestRegressor(random_state=42)
    rf_model_esg.fit(X_train, y_train)

    # Train Risk Prediction Model
    rf_model_risk = RandomForestRegressor(random_state=42)
    rf_model_risk.fit(risk_X_train, risk_y_train)

    return rf_model_esg, rf_model_risk

# Function to predict ESG scores
def predict_esg(rf_model_esg, X_future):
    return rf_model_esg.predict(X_future)

# Function to predict ESG scores and risk factors
def predict_scores(models, X_future, risk_X_future):
    rf_model_esg, rf_model_risk = models

    predicted_esg_scores = predict_esg(rf_model_esg, X_future)
    predicted_risk_factors = rf_model_risk.predict(risk_X_future)

    return predicted_esg_scores, predicted_risk_factors

# Function to allocate budget using optimization
def allocate_budget(predicted_data, budget, project_series):
    # Filter for selected project series
    if project_series != "All Projects":
        predicted_data = predicted_data[predicted_data['Series Name'] == project_series]

    # Define MILP Problem
    problem = LpProblem("ESG_Optimization", LpMaximize)

    # Define decision variables
    projects = list(predicted_data.index)
    allocations = LpVariable.dicts("Allocation", projects, 0, 1, cat='Binary')

    # Objective: Maximize ESG Scores while considering risk factors
    problem += lpSum([
        predicted_data.loc[i, 'Predicted ESG Score'] * (1 - predicted_data.loc[i, 'Risk Factor']) * allocations[i]
        for i in projects
    ]), "Maximize ESG Impact Adjusted for Risk"

    # Constraint: Budget
    problem += lpSum([
        predicted_data.loc[i, 'Project Cost'] * allocations[i]
        for i in projects
    ]) <= budget, "Budget Constraint"

    # Solve the problem
    problem.solve()

    # Collect results
    allocated_projects = [i for i in projects if allocations[i].varValue == 1]

    allocated_data = predicted_data.loc[allocated_projects]
    used_budget = allocated_data['Project Cost'].sum()

    return allocated_data, used_budget

# Main pipeline for prediction and allocation
def main_pipeline(file_path, budget, project_series="All Projects"):
    # Load and preprocess data
    pivot_data, pivot_data_encoded = load_and_preprocess_data(file_path)

    # Prepare data for ESG score prediction
    X = pivot_data_encoded[pivot_data_encoded['Year'] < 2020].drop(columns=['Value', 'Year'])
    y = pivot_data_encoded[pivot_data_encoded['Year'] < 2020]['Value']
    X_future = pivot_data_encoded[pivot_data_encoded['Year'] >= 2020].drop(columns=['Value', 'Year'])
    future_years = pivot_data[pivot_data['Year'] >= 2020][['Country Name', 'Series Name', 'Year']]

    # Generate risk factor target variable for demonstration
    pivot_data_encoded['Risk Factor'] = np.random.uniform(0.1, 0.5, size=len(pivot_data_encoded))
    risk_X = X.copy()
    risk_y = pivot_data_encoded[pivot_data_encoded['Year'] < 2020]['Risk Factor']
    risk_X_future = X_future.copy()

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    risk_X_train, risk_X_test, risk_y_train, risk_y_test = train_test_split(risk_X, risk_y, test_size=0.2, random_state=42)

    # Train models
    rf_model_esg, rf_model_risk = train_models(X_train, y_train, risk_X_train, risk_y_train)

    # Predict ESG scores and risk factors
    predicted_esg_scores, predicted_risk_factors = predict_scores((rf_model_esg, rf_model_risk), X_future, risk_X_future)
    
    # Add predictions to future_years
    future_years['Predicted ESG Score'] = predicted_esg_scores
    future_years['Risk Factor'] = predicted_risk_factors
    future_years['Project Cost'] = np.random.randint(50, 200, size=len(future_years))

    # Allocate budget
    allocated_data, used_budget = allocate_budget(future_years, budget, project_series)

    return allocated_data, used_budget
