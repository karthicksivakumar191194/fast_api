from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.auth import LoginRequest, Token
from app.services.auth import authenticate_user, create_access_token
from app.db.database import get_db

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
        login_request: LoginRequest, db: Session = Depends(get_db)
):
    # Validate user credentials
    user = authenticate_user(db, login_request.username, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Generate JWT token
    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}
