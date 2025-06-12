from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

def register_error_handlers(app):
    """Register global error handlers for the Flask application"""
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handle Marshmallow validation errors"""
        return jsonify({
            "error": "Validation Error",
            "messages": error.messages
        }), 400
    
    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error):
        """Handle database-related errors"""
        return jsonify({
            "error": "Database Error",
            "message": str(error)
        }), 500
    
    @app.errorhandler(ValueError)
    def handle_value_error(error):
        """Handle value errors"""
        return jsonify({
            "error": "Invalid Input",
            "message": str(error)
        }), 400
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 Not Found errors"""
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource could not be found"
        }), 404
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        """Handle 401 Unauthorized errors"""
        return jsonify({
            "error": "Unauthorized",
            "message": "Authentication is required to access this resource"
        }), 401
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """Handle 403 Forbidden errors"""
        return jsonify({
            "error": "Forbidden",
            "message": "You do not have permission to access this resource"
        }), 403
