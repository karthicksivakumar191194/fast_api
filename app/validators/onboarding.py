from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import User
from typing import List

def validate_owner_email(db: Session, email: str, errors: List[str]):
    if db.query(User).filter(User.email == email).first():
        errors.append("Email already exists.")

def validate_company_name(company_name: str, errors: List[str]):
    if not company_name:
        errors.append("Company name cannot be empty.")

def validate_company_website(company_website: str, errors: List[str]):
    if company_website and not company_website.startswith("http"):
        errors.append("Invalid company website URL.")

def validate_onboard_request(request, db: Session):
    errors = []

    # Validate each field and add errors to the list if necessary
    validate_owner_email(db, request.owner_email, errors)
    validate_company_name(request.company_name, errors)
    validate_company_website(request.company_website, errors)

    # If there are errors, raise an HTTPException with all errors
    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": errors}
        )
