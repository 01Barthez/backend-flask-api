from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.auth_service import AuthService
from ..models.user import UserSchema

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            email:
              type: string
            password:
              type: string
    responses:
      201:
        description: User registered successfully
      400:
        description: Registration error
    """
    try:
        data = request.get_json()
        user = AuthService.register_user(
            data['username'], 
            data['email'], 
            data['password']
        )
        return jsonify(user_schema.dump(user)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    try:
        data = request.get_json()
        token = AuthService.authenticate_user(
            data['username'], 
            data['password']
        )
        return jsonify({"access_token": token}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get user profile
    ---
    security:
      - JWT: []
    responses:
      200:
        description: User profile retrieved
      401:
        description: Unauthorized
    """
    current_user_id = get_jwt_identity()
    user = AuthService.get_user_by_id(current_user_id)
    return jsonify(user_schema.dump(user)), 200
