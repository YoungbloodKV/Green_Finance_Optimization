from flask import Blueprint, request, jsonify  # Import jsonify
import pandas as pd
import json  # Import json for JSON operations

dataset_routes = Blueprint('dataset_routes', __name__)

@dataset_routes.route('/upload', methods=['POST'])
def upload_dataset():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Process the uploaded file
        df = pd.read_csv(file)
        result_summary = df.describe().to_dict()

        # Save processed results to a JSON object
        result_json = json.dumps(result_summary)

        return jsonify({"message": "Dataset processed successfully", "summary": result_json}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
