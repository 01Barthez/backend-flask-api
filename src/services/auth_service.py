from flask_jwt_extended import create_access_token
from ..models.user import User
from ..app.database import session
from datetime import timedelta

class AuthService:
    @staticmethod
    def register_user(username, email, password):
        # Check if user already exists
        if session.query(User).filter_by(username=username).first():
            raise ValueError("Username already exists")
        if session.query(User).filter_by(email=email).first():
            raise ValueError("Email already exists")
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        session.add(new_user)
        session.commit()
        
        return new_user
    
    @staticmethod
    def authenticate_user(username, password):
        user = session.query(User).filter_by(username=username).first()
        
        if user and user.check_password(password):
            # Create JWT token
            access_token = create_access_token(
                identity=user.id, 
                expires_delta=timedelta(hours=2)
            )
            return access_token
        
        raise ValueError("Invalid credentials")
    
    @staticmethod
    def get_user_by_id(user_id):
        return session.query(User).get(user_id)
