#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from pulp import LpProblem, LpMaximize, LpVariable, lpSum
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from transformers import T5Tokenizer, T5ForConditionalGeneration
from utils.data_processor import load_and_preprocess_data
import warnings
warnings.filterwarnings('ignore')

# Adjust Pandas display settings
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Load the dataset
file_path = r"D:\ESG_REAL20_with_costs.csv"  # Update the relative path if necessary
data = pd.read_csv(file_path)

# Preprocessing: Melt the dataset to long format
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

# Prepare data for ESG score prediction
X = pivot_data_encoded[pivot_data_encoded['Year'] < 2020].drop(columns=['Value', 'Year'])
y = pivot_data_encoded[pivot_data_encoded['Year'] < 2020]['Value']
X_future = pivot_data_encoded[pivot_data_encoded['Year'] >= 2020].drop(columns=['Value', 'Year'])
future_years = pivot_data[pivot_data['Year'] >= 2020][['Country Name', 'Series Name', 'Year']]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train ESG Prediction Model
rf_model_esg = RandomForestRegressor(random_state=42)
rf_model_esg.fit(X_train, y_train)

# Predict ESG Scores for future years
predicted_scores = rf_model_esg.predict(X_future)

# Convert NumPy array to DataFrame
predicted_scores_df = pd.DataFrame(predicted_scores, columns=["Predicted ESG Score"])
future_years = pd.concat([future_years.reset_index(drop=True), predicted_scores_df], axis=1)

# Add hypothetical project costs
future_years['Project Cost'] = np.random.randint(50, 200, size=len(future_years))

# Train Risk Factor Prediction Model
pivot_data_encoded['Risk Factor'] = np.random.uniform(0.1, 0.5, size=len(pivot_data_encoded))
risk_X = pivot_data_encoded[pivot_data_encoded['Year'] < 2020].drop(columns=['Value', 'Year', 'Risk Factor'])
risk_y = pivot_data_encoded[pivot_data_encoded['Year'] < 2020]['Risk Factor']
risk_X_future = pivot_data_encoded[pivot_data_encoded['Year'] >= 2020].drop(columns=['Value', 'Year', 'Risk Factor'])

# Train-Test Split for Risk Factor
risk_X_train, risk_X_test, risk_y_train, risk_y_test = train_test_split(risk_X, risk_y, test_size=0.2, random_state=42)

# Train Risk Prediction Model
rf_model_risk = RandomForestRegressor(random_state=42)
rf_model_risk.fit(risk_X_train, risk_y_train)

# Predict Risk Factors for future years
predicted_risks = rf_model_risk.predict(risk_X_future)
future_years['Risk Factor'] = predicted_risks

# Function for MILP Allocation
def allocate_budget_milp(budget, project_series="All Projects"):
    if project_series != "All Projects":
        future_years_filtered = future_years[future_years['Series Name'] == project_series]
    else:
        future_years_filtered = future_years.copy()

    problem = LpProblem("ESG_Optimization", LpMaximize)

    projects = list(future_years_filtered.index)
    allocations = LpVariable.dicts("Allocation", projects, 0, 1, cat='Binary')

    problem += lpSum([
        future_years_filtered.loc[i, 'Predicted ESG Score'] * (1 - future_years_filtered.loc[i, 'Risk Factor']) * allocations[i]
        for i in projects
    ])
    problem += lpSum([
        future_years_filtered.loc[i, 'Project Cost'] * allocations[i]
        for i in projects
    ]) <= budget

    problem.solve()

    allocated_projects = []
    for i in projects:
        if allocations[i].varValue == 1:
            allocated_projects.append(i)

    allocated_allocation = future_years_filtered.loc[allocated_projects].copy()
    allocated_allocation['Allocated Cost'] = allocated_allocation['Project Cost']
    return allocated_allocation

# Load ESG-BERT Model
esg_bert_tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-esg")
esg_bert_model = TFAutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-esg", from_pt=True)

# Load T5 Model for Summarization
t5_tokenizer = T5Tokenizer.from_pretrained("t5-small")
t5_model = T5ForConditionalGeneration.from_pretrained("t5-small")

def analyze_with_esg_bert(text):
    inputs = esg_bert_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    outputs = esg_bert_model(**inputs)
    scores = outputs.logits.softmax(dim=-1).detach().numpy()[0]
    sentiment = ["Environmental", "Social", "Governance"][scores.argmax()]
    return sentiment, scores

def summarize_results_with_t5(text):
    input_ids = t5_tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = t5_model.generate(input_ids, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    return t5_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def summarize_and_analyze_esg_results():
    combined_results = []
    for _, row in future_years.iterrows():
        result_text = (
            f"Project: {row['Series Name']}, ESG Score: {row['Predicted ESG Score']:.2f}, "
            f"Risk Factor: {row['Risk Factor']:.2f}, Cost: {row['Project Cost']}"
        )
        combined_results.append(result_text)

    full_text = " ".join(combined_results)
    return summarize_results_with_t5(full_text)

# Main Pipeline
def main_pipeline(file_path, budget, project_series="All Projects"):
    """
    Execute the ESG prediction and budget allocation pipeline.

    Args:
        file_path (str): Path to the dataset.
        budget (float): Budget for allocation.
        project_series (str): Specific project series or "All Projects".

    Returns:
        pd.DataFrame: Allocated projects with relevant details.
    """
    pivot_data, pivot_data_encoded = load_and_preprocess_data(file_path)
    X = pivot_data_encoded[pivot_data_encoded['Year'] < 2020].drop(columns=['Value', 'Year'])
    y = pivot_data_encoded[pivot_data_encoded['Year'] < 2020]['Value']
    X_future = pivot_data_encoded[pivot_data_encoded['Year'] >= 2020].drop(columns=['Value', 'Year'])
    future_years = pivot_data[pivot_data['Year'] >= 2020][['Country Name', 'Series Name', 'Year']]

    rf_model_esg = RandomForestRegressor(random_state=42)
    rf_model_esg.fit(X_train, y_train)

    predicted_scores = rf_model_esg.predict(X_future)
    
    # Convert NumPy array to DataFrame
    predicted_scores_df = pd.DataFrame(predicted_scores, columns=["Predicted ESG Score"])
    future_years = pd.concat([future_years.reset_index(drop=True), predicted_scores_df], axis=1)

    future_years['Project Cost'] = np.random.randint(50, 200, size=len(future_years))

    allocated_projects = allocate_budget_milp(budget, project_series)
    return allocated_projects
