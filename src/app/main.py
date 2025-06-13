import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
from flask_talisman import Talisman
from dotenv import load_dotenv
from .database import init_db, session
from ..routes.auth import auth_bp
from ..routes.user import user_bp
from ..routes.meal import meal_bp
from ..routes.allergy import allergy_bp
from ..utils.error_handlers import register_error_handlers

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
    # Security Configurations
    Talisman(app, 
             content_security_policy={
                 'default-src': '\\self\\',
                 'script-src': '\\self\\',
                 'style-src': '\\self\\',
             },
             force_https=True,
             strict_transport_security=True,
             x_frame_options='SAMEORIGIN')
    
    # Initialize database
    init_db(app)
    
    # Extensions
    JWTManager(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Swagger Configuration
    Swagger(app, template_file='swagger.yaml')
    
    # Error Handlers
    register_error_handlers(app)
    
    # Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(meal_bp, url_prefix='/meals')
    app.register_blueprint(allergy_bp, url_prefix='/allergies')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
