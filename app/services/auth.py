from sqlalchemy.orm import Session
from app.models.auth import User
from app.db.database import get_db
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from app.settings import settings

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Function to verify a plain-text password against a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Function to authenticate user
def authenticate_user(db: Session, username: str, password: str) -> User:
    # Query the user by username
    user = db.query(User).filter(User.username == username).first()

    if user is None:
        return None

    # Verify if the password is correct
    if not verify_password(password, user.hashed_password):
        return None

    return user


# Function to create a JWT token
def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    # Set expiration time
    expire = datetime.utcnow() + timedelta(seconds=settings.token_expire_seconds)
    to_encode.update({"exp": expire})

    # Create the JWT token
    encoded_jwt = jwt.encode(to_encode, settings.token_secret_key, algorithm=settings.token_algorithm)
    return encoded_jwt
