from flask_migrate import Migrate
from .main import create_app
from .database import db

app = create_app()
migrate = Migrate(app, db)

def init_migrations():
    """Initialize database migrations"""
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_migrations()
