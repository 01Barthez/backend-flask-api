from ..app.database import db
from ..models.meal import Meal
from ..models.allergy import Allergy
from sqlalchemy import func

class MealService:
    @staticmethod
    def create_meal(user_id, name, description, ingredients):
        """Create a new meal for a user"""
        meal = Meal(
            name=name, 
            description=description, 
            ingredients=ingredients, 
            user_id=user_id
        )
        db.session.add(meal)
        db.session.commit()
        return meal
    
    @staticmethod
    def get_meal_by_id(meal_id, user_id):
        """Get a specific meal for a user"""
        return Meal.query.filter_by(id=meal_id, user_id=user_id).first()
    
    @staticmethod
    def get_all_user_meals(user_id):
        """Get all meals for a user"""
        return Meal.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def update_meal(meal_id, user_id, **kwargs):
        """Update a meal"""
        meal = Meal.query.filter_by(id=meal_id, user_id=user_id).first()
        if not meal:
            return None
        
        for key, value in kwargs.items():
            setattr(meal, key, value)
        
        db.session.commit()
        return meal
    
    @staticmethod
    def delete_meal(meal_id, user_id):
        """Delete a meal"""
        meal = Meal.query.filter_by(id=meal_id, user_id=user_id).first()
        if not meal:
            return False
        
        db.session.delete(meal)
        db.session.commit()
        return True
    
    @staticmethod
    def get_meals_with_high_allergy_risk(threshold=0.2):
        """Get meals with allergy risk above a certain threshold"""
        return Meal.query.filter(Meal.allergy_risk >= threshold).all()
    
    @staticmethod
    def get_meals_with_most_allergies():
        """Get meals sorted by number of allergies"""
        return (
            db.session.query(Meal, func.count(Allergy.id).label('allergy_count'))
            .outerjoin(Allergy)
            .group_by(Meal)
            .order_by(func.count(Allergy.id).desc())
            .all()
        )
