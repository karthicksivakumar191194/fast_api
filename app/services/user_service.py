from sqlalchemy.orm import Session
from app.models import User

def create_owner_account(db: Session, name: str, email: str, mobile_no: str) -> User:
    """
    Creates a new owner account (user) with the provided details.
    """
    owner = User(
        name=name,
        email=email,
        mobile_no=mobile_no,
        is_account_owner=True
    )
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return owner
