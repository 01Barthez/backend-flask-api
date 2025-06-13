from ..app.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validates, ValidationError
from datetime import datetime

class Meal(Base):
    __tablename__ = 'meals'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    ingredients = Column(Text)
    allergy_risk = Column(Float, default=0.0)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='meals')
    
    allergies = relationship('Allergy', back_populates='meal', cascade='all, delete-orphan')
    
    def update_allergy_risk(self):
        """Update allergy risk based on number of allergies"""
        allergy_count = len(self.allergies)
        self.allergy_risk = min(allergy_count * 0.1, 0.3)  # Max 30% risk

class MealSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Meal
        load_instance = True
        include_relationships = True
    
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    allergies = fields.List(fields.Nested('AllergySchema', exclude=('meal',)), dump_only=True)
    allergy_risk = fields.Float(dump_only=True)
    
    @validates('name')
    def validate_name(self, value):
        if len(value) < 2:
            raise ValidationError('Meal name must be at least 2 characters long.')
