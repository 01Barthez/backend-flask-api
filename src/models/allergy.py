from ..app.database import db, ma
from sqlalchemy.orm import relationship
from marshmallow import fields, validates, ValidationError

class Allergy(db.Model):
    __tablename__ = 'allergies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(20), default='mild')
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='allergies')
    
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    meal = relationship('Meal', back_populates='allergies')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update meal's allergy risk when a new allergy is added
        if self.meal:
            self.meal.update_allergy_risk()

class AllergySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Allergy
        load_instance = True
    
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    meal_id = fields.Integer(required=True)
    
    @validates('name')
    def validate_name(self, value):
        if len(value) < 2:
            raise ValidationError('Allergy name must be at least 2 characters long.')
    
    @validates('severity')
    def validate_severity(self, value):
        valid_severities = ['mild', 'moderate', 'severe']
        if value.lower() not in valid_severities:
            raise ValidationError(f'Severity must be one of: {", ".join(valid_severities)}')
