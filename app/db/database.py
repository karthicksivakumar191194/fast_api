from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.settings import settings

# The URL to the database
SQLALCHEMY_DATABASE_URL = settings.database_url

# Create the SQLAlchemy engine that connects to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create the session factory for creating sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for your database models
Base = declarative_base()

# Dependency to get the current database session
def get_db():
    """
    Provides a database session, yielding it for use within a request context.
    After the request, the session is closed to free up resources.
    """
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Yield the session to be used in a route or service
    finally:
        db.close()  # Ensure that the session is closed after the request
