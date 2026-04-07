"""Pydantic models for users."""

from datetime import datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """A user in the TaskFlow application."""

    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=50)
    email: str = Field(unique=True, max_length=100)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.now)


class UserCreate(SQLModel):
    """Schema for user registration."""

    username: str
    email: str
    password: str


class UserLogin(SQLModel):
    """Schema for user login."""

    username: str
    password: str


class UserRead(SQLModel):
    """Schema for reading user info."""

    id: int
    username: str
    email: str
    created_at: datetime


class Token(SQLModel):
    """Schema for JWT token response."""

    access_token: str
    token_type: str = "bearer"
    user: UserRead
