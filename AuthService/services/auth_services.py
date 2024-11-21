import re
from passlib.context import CryptContext
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from database.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_user(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()


async def create_user(db: AsyncSession, username: str, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def password_conditionals(
    password: str,
    length: int = 8,
    uppercase: bool = True,
    special_characters: bool = True,
):
    """
    Validates the password against the specified conditions:
    - Minimum length (default: 8 characters)
    - At least one uppercase letter (configurable)
    - At least one lowercase letter
    - At least one digit
    - At least one special character (configurable)
    """
    if len(password) < length:
        raise HTTPException(
            status_code=400,
            detail=f"Password must be at least {length} characters long",
        )

    if uppercase and not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one uppercase letter",
        )

    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one lowercase letter",
        )

    if not re.search(r"[0-9]", password):
        raise HTTPException(
            status_code=400, detail="Password must contain at least one digit"
        )

    if special_characters and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one special character",
        )

    return True







