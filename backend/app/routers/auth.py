from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import TokenResponse
from app.core.security import verify_password, create_access_token
from app.core.security import hash_password
from app.schemas.auth import RegisterRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Verifies username and password, and returns a JWT access token
    if correct. Uses the standard OAuth2 form format.
    """
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(user.username, user.role)
    return TokenResponse(access_token=token)
@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """
    Creates a new user account with the default 'analyst' role,
    and immediately returns a JWT token so the user is logged in.
    """
    existing_user = db.query(User).filter(User.username == payload.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = User(
        username=payload.username,
        hashed_password=hash_password(payload.password),
    )
    db.add(new_user)
    db.commit()

    token = create_access_token(new_user.username, new_user.role)
    return TokenResponse(access_token=token)