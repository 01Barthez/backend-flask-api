from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.allergy_service import AllergyService
from ..models.allergy import AllergySchema
from ..models.user import UserSchema

allergy_bp = Blueprint('allergies', __name__)
allergy_schema = AllergySchema()
allergies_schema = AllergySchema(many=True)
user_schema = UserSchema()

@allergy_bp.route('', methods=['POST'])
@jwt_required()
def create_allergy():
    """
    Create a new allergy for a meal
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
            meal_id:
              type: integer
            name:
              type: string
            severity:
              type: string
              enum: ['mild', 'moderate', 'severe']
    responses:
      201:
        description: Allergy created successfully
      400:
        description: Invalid input
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        allergy = AllergyService.create_allergy(
            user_id, 
            data['meal_id'], 
            data['name'], 
            data.get('severity', 'mild')
        )
        return jsonify(allergy_schema.dump(allergy)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@allergy_bp.route('', methods=['GET'])
@jwt_required()
def get_user_allergies():
    """
    Get all allergies for the current user
    ---
    security:
      - JWT: []
    responses:
      200:
        description: List of user's allergies
    """
    user_id = get_jwt_identity()
    allergies = AllergyService.get_user_allergies(user_id)
    return jsonify(allergies_schema.dump(allergies)), 200

@allergy_bp.route('/<int:allergy_id>', methods=['GET'])
@jwt_required()
def get_allergy(allergy_id):
    """
    Get a specific allergy
    ---
    security:
      - JWT: []
    parameters:
      - name: allergy_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Allergy details
      404:
        description: Allergy not found
    """
    user_id = get_jwt_identity()
    allergy = AllergyService.get_allergy_by_id(allergy_id, user_id)
    if not allergy:
        return jsonify({"error": "Allergy not found"}), 404
    return jsonify(allergy_schema.dump(allergy)), 200

@allergy_bp.route('/<int:allergy_id>', methods=['PUT'])
@jwt_required()
def update_allergy(allergy_id):
    """
    Update an allergy
    ---
    security:
      - JWT: []
    parameters:
      - name: allergy_id
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
            severity:
              type: string
              enum: ['mild', 'moderate', 'severe']
    responses:
      200:
        description: Allergy updated successfully
      404:
        description: Allergy not found
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    allergy = AllergyService.update_allergy(allergy_id, user_id, **data)
    if not allergy:
        return jsonify({"error": "Allergy not found"}), 404
    
    return jsonify(allergy_schema.dump(allergy)), 200

@allergy_bp.route('/<int:allergy_id>', methods=['DELETE'])
@jwt_required()
def delete_allergy(allergy_id):
    """
    Delete an allergy
    ---
    security:
      - JWT: []
    parameters:
      - name: allergy_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Allergy deleted successfully
      404:
        description: Allergy not found
    """
    user_id = get_jwt_identity()
    success = AllergyService.delete_allergy(allergy_id, user_id)
    
    if not success:
        return jsonify({"error": "Allergy not found"}), 404
    
    return '', 204

@allergy_bp.route('/users-with-allergies', methods=['GET'])
@jwt_required()
def get_users_with_allergies():
    """
    Get all users with allergies
    ---
    security:
      - JWT: []
    responses:
      200:
        description: Users with their allergy counts
    """
    users_with_allergies = AllergyService.get_users_with_allergies()
    result = [
        {
            "user": user_schema.dump(user), 
            "allergy_count": count
        } for user, count in users_with_allergies
    ]
    return jsonify(result), 200

@allergy_bp.route('/meals-causing-allergies', methods=['GET'])
@jwt_required()
def get_meals_causing_allergies():
    """
    Get meals that have caused allergies
    ---
    security:
      - JWT: []
    responses:
      200:
        description: Meals with their allergy counts
    """
    meals_with_allergies = AllergyService.get_meals_causing_allergies()
    result = [
        {
            "meal": meal_schema.dump(meal), 
            "allergy_count": count
        } for meal, count in meals_with_allergies
    ]
    return jsonify(result), 200
