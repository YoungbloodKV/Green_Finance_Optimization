from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import numpy as np
import pandas as pd
from datetime import datetime
from utils.data_processor import preprocess_dataset, create_pivot_data
from utils.ai_integration import summarize_and_analyze_esg_results
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directory for saving uploaded files
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit uploads to 16 MB

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload-dataset', methods=['POST'])
def upload_dataset():
    """Handle dataset uploads."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only .csv files are allowed"}), 400

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    raw_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'uploaded_dataset_{timestamp}.csv')
    try:
        file.save(raw_file_path)
        logger.info(f"File saved at: {raw_file_path}")

        # Validate and preprocess dataset
        df = pd.read_csv(raw_file_path)
        preprocessed_df, year_columns = preprocess_dataset(df)
        logger.info(f"Year columns detected: {year_columns}")

        preprocessed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'preprocessed_dataset_{timestamp}.csv')
        preprocessed_df.to_csv(preprocessed_file_path, index=False)
        logger.info(f"Dataset preprocessed and saved at: {preprocessed_file_path}")

        return jsonify({"message": "Dataset uploaded and preprocessed successfully", "file_path": preprocessed_file_path}), 200
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return jsonify({"error": f"Failed to process file: {str(e)}"}), 500

@app.route('/project-series', methods=['GET'])
def get_project_series():
    """Fetch unique project series from the uploaded dataset."""
    try:
        uploaded_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.csv')]
        if not uploaded_files:
            return jsonify({"error": "No dataset uploaded. Please upload a file first."}), 400

        latest_file = max(uploaded_files, key=lambda f: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], f)))
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], latest_file)

        df = pd.read_csv(file_path)
        if 'SeriesName' not in df.columns:
            return jsonify({"error": "'SeriesName' column not found in the dataset."}), 400

        project_series = df['SeriesName'].dropna().unique().tolist()
        return jsonify({"series": project_series}), 200
    except Exception as e:
        logger.error(f"Error in /project-series: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/predict-esg', methods=['POST'])
def predict_esg():
    try:
        data = request.get_json()
        project_series = data.get("project_series", "All Projects")

        preprocessed_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.startswith('preprocessed_dataset_')]
        if not preprocessed_files:
            return jsonify({"error": "No preprocessed dataset found. Please upload a dataset first."}), 400

        latest_file = max(preprocessed_files, key=lambda f: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], f)))
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], latest_file)

        df = pd.read_csv(file_path)

        if project_series != "All Projects":
            df = df[df["SeriesName"] == project_series]
            if df.empty:
                return jsonify({"error": f"No data found for project series: {project_series}"}), 400

        year_column = 'YR2020'
        if year_column not in df.columns:
            raise ValueError(f"Year column '{year_column}' not found in the dataset.")

        pivot_data = create_pivot_data(df, year_column)

        # Ensure "Cost" and "RiskFactor" exist in the dataset
        if "Cost" not in pivot_data.columns:
            pivot_data["Cost"] = np.random.randint(20, 81, size=len(pivot_data))
        if "RiskFactor" not in pivot_data.columns:
            pivot_data["RiskFactor"] = np.random.uniform(0.1, 0.5, size=len(pivot_data))

        # Add predictions
        pivot_data['Predicted ESG Score'] = np.random.uniform(50, 100, len(pivot_data))

        predictions = pivot_data.to_dict(orient="records")
        return jsonify({"predictions": predictions}), 200
    except Exception as e:
        logger.error(f"Error in /predict-esg: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/allocate-budget', methods=['POST'])
def allocate_budget():
    """Allocate budget for projects based on predictions."""
    try:
        data = request.json
        budget = data.get('budget')
        project_series = data.get('project_series')

        if not isinstance(budget, (int, float)) or budget <= 0:
            raise ValueError("Invalid budget value. Must be a positive number.")
        if not isinstance(project_series, str) or not project_series.strip():
            raise ValueError("Invalid project_series value.")

        predictions = data.get('predictions', [])
        if not predictions:
            raise ValueError("No predictions provided. Please run ESG predictions first.")

        filtered_predictions = [p for p in predictions if p['Series Name'] == project_series or project_series == 'All Projects']
        allocated_budget = allocate(filtered_predictions, budget)

        return jsonify(allocated_budget), 200
    except Exception as e:
        logger.error(f"Error in /allocate-budget: {e}")
        return jsonify({"error": str(e)}), 400

def allocate(predictions, budget):
    """Allocate budget to projects based on ESG scores."""
    # Ensure predictions contain the expected keys
    for project in predictions:
        project.setdefault('Series Name', 'Unknown')
        project.setdefault('Cost', 0)
        project.setdefault('Predicted ESG Score', 0)
        project.setdefault('RiskFactor', 'Unknown')

    sorted_predictions = sorted(predictions, key=lambda x: x['Predicted ESG Score'], reverse=True)
    total_cost = 0
    allocated_projects = []

    for project in sorted_predictions:
        project_cost = project.get('Cost', 0)
        if total_cost + project_cost <= budget:
            allocated_projects.append({
                'Project': project['Series Name'],
                'ESGScore': project['Predicted ESG Score'],
                'Cost': project_cost,
                'RiskFactor': project.get('RiskFactor', 'Unknown')
            })
            total_cost += project_cost
        else:
            break

    return {
        "allocated_projects": allocated_projects,
        "total_allocated": total_cost,
        "remaining_budget": budget - total_cost
    }

@app.route('/summarize-esg-results', methods=['POST'])
def summarize_esg_results():
    """Summarize ESG results."""
    try:
        text_data = request.json.get('text', '')
        summary = summarize_and_analyze_esg_results(text_data)
        return jsonify({"summary": summary}), 200
    except Exception as e:
        logger.error(f"Error in /summarize-esg-results: {e}")
        return jsonify({"error": f"Failed to summarize ESG results: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
