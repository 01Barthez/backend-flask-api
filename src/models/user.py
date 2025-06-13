from ..app.database import Base
from sqlalchemy import Column, Integer, String, relationship
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    meals = relationship('Meal', back_populates='user')
    allergies = relationship('Allergy', back_populates='user')
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True
        exclude = ('password_hash',)
    
    id = fields.Integer(dump_only=True)
    meals = fields.List(fields.Nested('MealSchema', exclude=('user',)), dump_only=True)
    allergies = fields.List(fields.Nested('AllergySchema', exclude=('user',)), dump_only=True)
