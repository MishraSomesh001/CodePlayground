from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud.user import create_user, get_or_create_google_user, get_user_by_email
from app.schemas.auth import (
    GoogleAccountRequest,
    LoginRequest,
    RegisterRequest,
    UserResponse,
)
from app.services.auth import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """Register a new user with email + password."""
    existing = await get_user_by_email(db, body.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    hashed = hash_password(body.password)
    user = await create_user(db, name=body.name, email=body.email, hashed_password=hashed)
    return user


@router.post("/login", response_model=UserResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Verify credentials and return the user object."""
    user = await get_user_by_email(db, body.email)

    if user is None or user.password is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    return user


@router.post("/google", response_model=UserResponse)
async def google_auth(body: GoogleAccountRequest, db: AsyncSession = Depends(get_db)):
    """Create or link a Google account and return the user."""
    user = await get_or_create_google_user(db, body)
    return user
