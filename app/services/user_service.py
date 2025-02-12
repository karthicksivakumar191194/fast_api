from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from app.models import Tenant, User, UserStatusEnum

def create_owner_user(db: Session, tenant: Tenant, name: str, email: str) -> User:
    """
    Creates a new owner user with the provided details.
    """
    date_format = "MM-DD-YYYY"
    time_format = "HH:mm:ss"
    time_zone = "UTC"

    # Create the user object with all provided details
    user = User(
        tenant_id=tenant.id,
        name=name,
        email=email,
        date_format=date_format,
        time_format=time_format,
        time_zone=time_zone,
        is_account_owner=True,
        status=UserStatusEnum.ACTIVE
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_tenant_owner_user(db: Session, tenant: Tenant) -> User:
    """
    Get tenant owner user
    """
    user = db.query(User).filter(User.tenant_id == tenant.id, User.is_account_owner == True).first()

    return user


def is_tenant_owner_email_exists(db: Session, email: str) -> bool:
    """
    Validate if tenant owner email exists
    """
    user_exists = db.query(exists().where(User.email == email, User.is_account_owner == True)).scalar()

    # TODO: If tenant deleted allow user to use this email

    return user_exists