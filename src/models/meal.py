from ..app.database import db, ma
from sqlalchemy.orm import relationship
from marshmallow import fields, validates, ValidationError
from datetime import datetime

class Meal(db.Model):
    __tablename__ = 'meals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    allergy_risk = db.Column(db.Float, default=0.0)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='meals')
    
    allergies = relationship('Allergy', back_populates='meal', cascade='all, delete-orphan')
    
    def update_allergy_risk(self):
        """Update allergy risk based on number of allergies"""
        allergy_count = len(self.allergies)
        self.allergy_risk = min(allergy_count * 0.1, 0.3)  # Max 30% risk
        db.session.commit()

class MealSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Meal
        load_instance = True
    
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    allergies = fields.List(fields.Nested('AllergySchema', exclude=('meal',)), dump_only=True)
    allergy_risk = fields.Float(dump_only=True)
    
    @validates('name')
    def validate_name(self, value):
        if len(value) < 2:
            raise ValidationError('Meal name must be at least 2 characters long.')
