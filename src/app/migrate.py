from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .main import create_app
from .database import Base

app = create_app()

def init_migrations():
    """Initialize database migrations"""
    with app.app_context():
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_migrations()
