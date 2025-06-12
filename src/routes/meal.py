from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.meal_service import MealService
from ..models.meal import MealSchema

meal_bp = Blueprint('meals', __name__)
meal_schema = MealSchema()
meals_schema = MealSchema(many=True)

@meal_bp.route('', methods=['POST'])
@jwt_required()
def create_meal():
    """
    Create a new meal
    ---
    security:
      - JWT: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
            ingredients:
              type: string
    responses:
      201:
        description: Meal created successfully
      400:
        description: Invalid input
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        meal = MealService.create_meal(
            user_id, 
            data['name'], 
            data.get('description', ''), 
            data.get('ingredients', '')
        )
        return jsonify(meal_schema.dump(meal)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@meal_bp.route('', methods=['GET'])
@jwt_required()
def get_user_meals():
    """
    Get all meals for the current user
    ---
    security:
      - JWT: []
    responses:
      200:
        description: List of user's meals
    """
    user_id = get_jwt_identity()
    meals = MealService.get_all_user_meals(user_id)
    return jsonify(meals_schema.dump(meals)), 200

@meal_bp.route('/<int:meal_id>', methods=['GET'])
@jwt_required()
def get_meal(meal_id):
    """
    Get a specific meal
    ---
    security:
      - JWT: []
    parameters:
      - name: meal_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Meal details
      404:
        description: Meal not found
    """
    user_id = get_jwt_identity()
    meal = MealService.get_meal_by_id(meal_id, user_id)
    if not meal:
        return jsonify({"error": "Meal not found"}), 404
    return jsonify(meal_schema.dump(meal)), 200

@meal_bp.route('/<int:meal_id>', methods=['PUT'])
@jwt_required()
def update_meal(meal_id):
    """
    Update a meal
    ---
    security:
      - JWT: []
    parameters:
      - name: meal_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
            ingredients:
              type: string
    responses:
      200:
        description: Meal updated successfully
      404:
        description: Meal not found
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    meal = MealService.update_meal(meal_id, user_id, **data)
    if not meal:
        return jsonify({"error": "Meal not found"}), 404
    
    return jsonify(meal_schema.dump(meal)), 200

@meal_bp.route('/<int:meal_id>', methods=['DELETE'])
@jwt_required()
def delete_meal(meal_id):
    """
    Delete a meal
    ---
    security:
      - JWT: []
    parameters:
      - name: meal_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Meal deleted successfully
      404:
        description: Meal not found
    """
    user_id = get_jwt_identity()
    success = MealService.delete_meal(meal_id, user_id)
    
    if not success:
        return jsonify({"error": "Meal not found"}), 404
    
    return '', 204

@meal_bp.route('/high-risk', methods=['GET'])
@jwt_required()
def get_high_risk_meals():
    """
    Get meals with high allergy risk
    ---
    security:
      - JWT: []
    parameters:
      - name: threshold
        in: query
        type: number
        default: 0.2
    responses:
      200:
        description: List of high-risk meals
    """
    threshold = float(request.args.get('threshold', 0.2))
    meals = MealService.get_meals_with_high_allergy_risk(threshold)
    return jsonify(meals_schema.dump(meals)), 200

@meal_bp.route('/most-allergies', methods=['GET'])
@jwt_required()
def get_meals_with_most_allergies():
    """
    Get meals sorted by number of allergies
    ---
    security:
      - JWT: []
    responses:
      200:
        description: Meals with most allergies
    """
    meals_with_counts = MealService.get_meals_with_most_allergies()
    result = [
        {
            "meal": meal_schema.dump(meal), 
            "allergy_count": count
        } for meal, count in meals_with_counts
    ]
    return jsonify(result), 200
