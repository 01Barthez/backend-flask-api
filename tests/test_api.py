import pytest
import json
from src.app.main import create_app
from src.app.database import db

@pytest.fixture
def client():
    """Create a test client for the application"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_user_registration(client):
    """Test user registration endpoint"""
    response = client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'strongpassword'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['username'] == 'testuser'

def test_user_login(client):
    """Test user login endpoint"""
    # First register a user
    client.post('/auth/register', json={
        'username': 'loginuser',
        'email': 'login@example.com',
        'password': 'loginpassword'
    })
    
    # Then attempt to log in
    response = client.post('/auth/login', json={
        'username': 'loginuser',
        'password': 'loginpassword'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data

def test_create_meal(client):
    """Test creating a meal"""
    # First register and login a user
    client.post('/auth/register', json={
        'username': 'mealuser',
        'email': 'meal@example.com',
        'password': 'mealpassword'
    })
    login_response = client.post('/auth/login', json={
        'username': 'mealuser',
        'password': 'mealpassword'
    })
    token = json.loads(login_response.data)['access_token']
    
    # Create a meal
    response = client.post('/meals', json={
        'name': 'Test Meal',
        'description': 'A test meal',
        'ingredients': 'Test ingredients'
    }, headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Test Meal'
    assert data['allergy_risk'] == 0.0

def test_create_allergy(client):
    """Test creating an allergy for a meal"""
    # Register and login user
    client.post('/auth/register', json={
        'username': 'allergyuser',
        'email': 'allergy@example.com',
        'password': 'allergypassword'
    })
    login_response = client.post('/auth/login', json={
        'username': 'allergyuser',
        'password': 'allergypassword'
    })
    token = json.loads(login_response.data)['access_token']
    
    # Create a meal
    meal_response = client.post('/meals', json={
        'name': 'Allergy Test Meal',
        'description': 'A meal for allergy testing',
        'ingredients': 'Test ingredients'
    }, headers={'Authorization': f'Bearer {token}'})
    meal_data = json.loads(meal_response.data)
    
    # Create an allergy
    allergy_response = client.post('/allergies', json={
        'meal_id': meal_data['id'],
        'name': 'Peanut Allergy',
        'severity': 'moderate'
    }, headers={'Authorization': f'Bearer {token}'})
    
    assert allergy_response.status_code == 201
    allergy_data = json.loads(allergy_response.data)
    assert allergy_data['name'] == 'Peanut Allergy'
    
    # Check meal's allergy risk updated
    meal_check_response = client.get(f'/meals/{meal_data["id"]}', 
                                     headers={'Authorization': f'Bearer {token}'})
    meal_check_data = json.loads(meal_check_response.data)
    assert meal_check_data['allergy_risk'] == 0.1  # 10% for one allergy
