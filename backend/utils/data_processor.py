import pandas as pd
import numpy as np


def preprocess_dataset(dataset):
    try:
        # Standardize column names
        dataset.columns = [
            col.strip().replace("[", "").replace("]", "").replace(" ", "") for col in dataset.columns
        ]

        # Fix year column naming: e.g., "2004[YR2004]" -> "YR2020"
        dataset.columns = [
            f"YR{col[-4:]}" if col[-4:].isdigit() and "YR" in col else col for col in dataset.columns
        ]

        # Detect year columns dynamically
        year_columns = [col for col in dataset.columns if "YR" in col]
        if not year_columns:
            raise ValueError("No valid year columns found (e.g., YR2020). Ensure dataset format is correct.")

        # Ensure required columns are present
        required_columns = ["CountryName", "SeriesName"] + year_columns
        missing_columns = [col for col in required_columns if col not in dataset.columns]
        if missing_columns:
            raise ValueError(f"Dataset is missing required columns: {missing_columns}")

        # Handle missing or invalid "Cost" column
        if "Cost" not in dataset.columns:
            dataset["Cost"] = np.random.randint(20, 81, size=len(dataset))
        else:
            dataset["Cost"] = dataset["Cost"].fillna(np.random.randint(20, 81, size=len(dataset)))

        # Handle missing or invalid "RiskFactor" column
        if "RiskFactor" not in dataset.columns:
            dataset["RiskFactor"] = np.random.uniform(0.1, 0.5, size=len(dataset))
        else:
            dataset["RiskFactor"] = dataset["RiskFactor"].fillna(np.random.uniform(0.1, 0.5, size=len(dataset)))

        # Drop rows with all year values as 0 or NaN
        dataset = dataset[required_columns + ["Cost", "RiskFactor"]]
        dataset = dataset.loc[~(dataset[year_columns].eq(0).all(axis=1) | dataset[year_columns].isna().all(axis=1))]

        # Fill missing values for year columns with column medians
        for col in year_columns:
            dataset[col].fillna(dataset[col].median(), inplace=True)

        return dataset, year_columns
    except Exception as e:
        print(f"Error in preprocessing dataset: {e}")
        raise


def create_pivot_data(dataset, year_column='YR2020'):
    """
    Create pivoted data structure for machine learning model training.

    Args:
        dataset (pd.DataFrame): Preprocessed dataset.
        year_column (str): The year column to use for pivoting.

    Returns:
        pd.DataFrame: Pivoted dataset ready for ML input.
    """
    try:
        # Ensure year_column is a string
        if not isinstance(year_column, str):
            raise ValueError(f"Invalid year_column value: {year_column}. Expected a single column name as a string.")

        # Validate the existence of the year column
        if year_column not in dataset.columns:
            raise ValueError(f"Year column '{year_column}' not found in dataset. Available columns: {dataset.columns.tolist()}")

        # Pivot data to wide format
        pivot_data = dataset.pivot_table(
            index=['CountryName', 'SeriesName'],
            values=year_column
        ).reset_index()

        # One-hot encode categorical features
        pivot_data_encoded = encode_categorical_features(pivot_data, ['CountryName', 'SeriesName'])
        print(f"Pivot data created:\n{pivot_data_encoded.head()}")

        if pivot_data_encoded.empty:
            raise ValueError("The pivoted dataset is empty. Check the input dataset or year column.")

        return pivot_data_encoded
    except Exception as e:
        print(f"Error in creating pivot data: {e}")
        raise

def encode_categorical_features(dataframe, categorical_columns):
    """
    Encode categorical features into one-hot representations.

    Args:
        dataframe (pd.DataFrame): Input data.
        categorical_columns (list): List of categorical columns to encode.

    Returns:
        pd.DataFrame: One-hot encoded DataFrame.
    """
    try:
        dataframe_encoded = pd.get_dummies(dataframe, columns=categorical_columns)
        print(f"Categorical features encoded: {categorical_columns}")
        return dataframe_encoded
    except Exception as e:
        print(f"Error in encoding categorical features: {e}")
        raise


def validate_dataset_columns(dataset, required_columns):
    """
    Validate if the dataset contains the required columns.

    Args:
        dataset (pd.DataFrame): Uploaded dataset.
        required_columns (list): List of required columns.

    Returns:
        bool: True if all columns are present, else raises an error.
    """
    try:
        missing_columns = [col for col in required_columns if col not in dataset.columns]
        if missing_columns:
            raise ValueError(f"Dataset is missing required columns: {missing_columns}")
        return True
    except Exception as e:
        print(f"Error in validating dataset columns: {e}")
        raise


def load_and_preprocess_data(file_path):
    """
    Load and preprocess the dataset for ESG prediction.

    Args:
        file_path (str): Path to the CSV dataset.

    Returns:
        pd.DataFrame: Preprocessed dataset ready for further processing.
        list: List of dynamically detected year columns.
    """
    try:
        # Load the dataset
        dataset = pd.read_csv(file_path, skipinitialspace=True)
        print(f"Dataset loaded with shape: {dataset.shape}")

        # Preprocess the dataset
        preprocessed_dataset, year_columns = preprocess_dataset(dataset)

        if preprocessed_dataset.empty:
            raise ValueError("The preprocessed dataset is empty. Check your input data and preprocessing logic.")

        print(f"Preprocessed dataset shape: {preprocessed_dataset.shape}")
        return preprocessed_dataset, year_columns
    except Exception as e:
        print(f"Error in load_and_preprocess_data: {e}")
        raise
