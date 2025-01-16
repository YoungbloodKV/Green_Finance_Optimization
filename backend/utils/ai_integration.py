import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model  # type: ignore
from pulp import LpProblem, LpMaximize, LpVariable, lpSum
from models.FinGreen_NLP import predicted_scores as nlp_predict_esg_scores
from models.FinGreen_NLP import allocate_budget_milp as nlp_allocate_budget
from models.FinGreen_NLP import summarize_and_analyze_esg_results as nlp_summarize_results
from utils.data_processor import preprocess_dataset, create_pivot_data
from transformers import T5Tokenizer, TFT5ForConditionalGeneration
import joblib

# Load T5 model for summarization
T5_MODEL_PATH = 't5-small'
t5_tokenizer = T5Tokenizer.from_pretrained(T5_MODEL_PATH)
t5_model = TFT5ForConditionalGeneration.from_pretrained(T5_MODEL_PATH)


def predict_esg_scores(input_data):
    """
    Predict ESG scores by delegating to FinGreen_NLP.

    Args:
        input_data (pd.DataFrame): Raw input data.

    Returns:
        pd.DataFrame: DataFrame with predicted ESG scores.
    """
    try:
        # Preprocess the dataset
        preprocessed_data, year_columns = preprocess_dataset(input_data)
        _, input_data_encoded = create_pivot_data(preprocessed_data, year_columns)

        # Call ESG prediction logic
        predictions = nlp_predict_esg_scores(input_data_encoded)

        # Combine predictions with input data
        input_data_encoded = input_data_encoded.reset_index(drop=True)
        predictions = pd.DataFrame(predictions, columns=["Predicted ESG Score"]).reset_index(drop=True)
        input_data_encoded["Predicted ESG Score"] = predictions["Predicted ESG Score"]

        print(f"Final predictions combined with input data:\n{input_data_encoded.head()}")
        return input_data_encoded
    except Exception as e:
        print(f"Error predicting ESG scores: {e}")
        raise


def summarize_and_analyze_esg_results(text_data, prompt="summarize: ", max_length=150, min_length=40):
    """
    Summarize ESG results using T5 model.

    Args:
        text_data (str): Combined project details and ESG scores in text format.
        prompt (str): Prompt to guide the T5 model summarization.
        max_length (int): Maximum length of the summary.
        min_length (int): Minimum length of the summary.

    Returns:
        str: Summarized ESG results.
    """
    try:
        # Tokenize and summarize using T5
        input_ids = t5_tokenizer.encode(prompt + text_data, return_tensors="pt", max_length=512, truncation=True)
        summary_ids = t5_model.generate(input_ids, max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = t5_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        print(f"Summary generated: {summary}")
        return summary
    except Exception as e:
        print(f"Error summarizing ESG results: {e}")
        raise


def allocate_budget_milp(data, budget, project_series="All Projects"):
    """
    Allocate budget using MILP by delegating to FinGreen_NLP.

    Args:
        data (pd.DataFrame): Raw project data with ESG scores.
        budget (float): Total budget for allocation.
        project_series (str): Optional filter for specific project series.

    Returns:
        pd.DataFrame: Allocated projects with cost and ESG scores.
    """
    try:
        # Preprocess and validate data
        preprocessed_data, year_columns = preprocess_dataset(data)
        pivot_data, _ = create_pivot_data(preprocessed_data, year_columns)

        # Call FinGreen_NLP's MILP allocation logic
        allocation_results = nlp_allocate_budget(pivot_data, budget, project_series)

        # Validate allocation results
        required_columns = ["Project Cost", "Predicted ESG Score", "Allocated Cost"]
        if not all(col in allocation_results.columns for col in required_columns):
            raise ValueError(f"Missing required columns in allocation results: {required_columns}")

        print(f"Budget allocation completed:\n{allocation_results.head()}")
        return allocation_results
    except Exception as e:
        print(f"Error in allocate_budget_milp: {e}")
        raise


def load_model(model_path, model_type="joblib"):
    """
    Load a pre-trained model from the specified path.

    Args:
        model_path (str): Path to the model file.
        model_type (str): Type of model to load ("joblib", "tensorflow", "pytorch").

    Returns:
        Trained model object.
    """
    try:
        if model_type == "joblib":
            return joblib.load(model_path)
        elif model_type == "tensorflow":
            from tensorflow.keras.models import load_model
            return load_model(model_path)
        elif model_type == "pytorch":
            import torch
            return torch.load(model_path)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    except Exception as e:
        print(f"Error loading model from {model_path}: {e}")
        raise
