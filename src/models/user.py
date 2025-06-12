from ..app.database import db, ma
from sqlalchemy.orm import relationship
from marshmallow import fields
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    meals = relationship('Meal', back_populates='user')
    allergies = relationship('Allergy', back_populates='user')
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password_hash',)
    
    id = fields.Integer(dump_only=True)
    meals = fields.List(fields.Nested('MealSchema', exclude=('user',)), dump_only=True)
    allergies = fields.List(fields.Nested('AllergySchema', exclude=('user',)), dump_only=True)
