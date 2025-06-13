from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = None
session = None
Base = declarative_base()

def init_db(app):
    global engine, session
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    session = scoped_session(sessionmaker(bind=engine))
    Base.metadata.bind = engine
    return session
