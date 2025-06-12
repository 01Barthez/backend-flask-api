from ..app.database import db
from ..models.allergy import Allergy
from ..models.user import User
from ..models.meal import Meal
from sqlalchemy import func

class AllergyService:
    @staticmethod
    def create_allergy(user_id, meal_id, name, severity='mild'):
        """Create a new allergy for a user's meal"""
        # Check if the meal belongs to the user
        meal = Meal.query.filter_by(id=meal_id, user_id=user_id).first()
        if not meal:
            raise ValueError("Meal not found or does not belong to the user")
        
        # Create allergy
        allergy = Allergy(
            name=name, 
            severity=severity, 
            user_id=user_id, 
            meal_id=meal_id
        )
        db.session.add(allergy)
        db.session.commit()
        
        # Update meal's allergy risk
        meal.update_allergy_risk()
        
        return allergy
    
    @staticmethod
    def get_user_allergies(user_id):
        """Get all allergies for a user"""
        return Allergy.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_allergy_by_id(allergy_id, user_id):
        """Get a specific allergy for a user"""
        return Allergy.query.filter_by(id=allergy_id, user_id=user_id).first()
    
    @staticmethod
    def update_allergy(allergy_id, user_id, **kwargs):
        """Update an allergy"""
        allergy = Allergy.query.filter_by(id=allergy_id, user_id=user_id).first()
        if not allergy:
            return None
        
        for key, value in kwargs.items():
            setattr(allergy, key, value)
        
        db.session.commit()
        
        # Update meal's allergy risk if severity changes
        if allergy.meal:
            allergy.meal.update_allergy_risk()
        
        return allergy
    
    @staticmethod
    def delete_allergy(allergy_id, user_id):
        """Delete an allergy"""
        allergy = Allergy.query.filter_by(id=allergy_id, user_id=user_id).first()
        if not allergy:
            return False
        
        # Store the meal to update its risk after deletion
        meal = allergy.meal
        
        db.session.delete(allergy)
        db.session.commit()
        
        # Update meal's allergy risk
        if meal:
            meal.update_allergy_risk()
        
        return True
    
    @staticmethod
    def get_users_with_allergies():
        """Get all users with their allergies"""
        return (
            db.session.query(User, func.count(Allergy.id).label('allergy_count'))
            .outerjoin(Allergy)
            .group_by(User)
            .filter(func.count(Allergy.id) > 0)
            .all()
        )
    
    @staticmethod
    def get_meals_causing_allergies():
        """Get meals that have caused allergies"""
        return (
            db.session.query(Meal, func.count(Allergy.id).label('allergy_count'))
            .join(Allergy)
            .group_by(Meal)
            .order_by(func.count(Allergy.id).desc())
            .all()
        )
