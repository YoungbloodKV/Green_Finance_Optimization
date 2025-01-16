from flask import Blueprint, request, jsonify
from utils.budget_allocator import allocate_budget

allocation_blueprint = Blueprint('allocation_routes', __name__)

@allocation_blueprint.route('/allocate', methods=['POST'])
def allocate():
    """Allocate budget to projects."""
    try:
        data = request.get_json()
        budget = data.get('budget')
        projects = data.get('projects')

        if not budget or not projects:
            return jsonify({"error": "Invalid data provided"}), 400

        allocation = allocate_budget(projects, budget)
        return jsonify({"allocation": allocation}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
