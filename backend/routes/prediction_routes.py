import pandas as pd
from flask import Blueprint, request, jsonify
from models.esg_model import ESGModel

prediction_blueprint = Blueprint('prediction_routes', __name__)
esg_model = ESGModel()

@prediction_blueprint.route('/esg', methods=['POST'])
def predict_esg():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        df = pd.read_csv(file)

        # Call ESG model for predictions
        esg_model.train_models(df)
        future_predictions = esg_model.predict_esg(df)

        return jsonify({"predictions": future_predictions.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
