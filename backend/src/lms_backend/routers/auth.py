"""FastAPI router for user authentication."""

from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from lms_backend.auth import create_access_token, get_password_hash, verify_password
from lms_backend.database import engine
from lms_backend.models.user import Token, User, UserCreate, UserLogin, UserRead

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate):
    """Register a new user."""
    with Session(engine) as session:
        # Check if username exists
        existing_user = session.exec(select(User).where(User.username == user_data.username)).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Username already registered",
            )
        
        # Check if email exists
        existing_email = session.exec(select(User).where(User.email == user_data.email)).first()
        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already registered",
            )
        
        # Create new user
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        
        # Create access token
        access_token = create_access_token(data={"sub": user.id})
        
        return Token(
            access_token=access_token,
            user=UserRead(
                id=user.id,
                username=user.username,
                email=user.email,
                created_at=user.created_at,
            ),
        )


@router.post("/login", response_model=Token)
def login(user_data: UserLogin):
    """Login and get access token."""
    with Session(engine) as session:
        # Find user
        user = session.exec(select(User).where(User.username == user_data.username)).first()
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
            )
        
        # Verify password
        if not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
            )
        
        # Create access token
        access_token = create_access_token(data={"sub": user.id})
        
        return Token(
            access_token=access_token,
            user=UserRead(
                id=user.id,
                username=user.username,
                email=user.email,
                created_at=user.created_at,
            ),
        )
