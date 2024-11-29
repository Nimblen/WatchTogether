from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserCreate, LoginRequest, Token, TokenRefreshRequest
from AuthService.services.user import (
    get_user,
    create_user,
    verify_password,
    password_conditionals,
)
from AuthService.services.token import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from database.sessions import get_session
from core.config import settings


router = APIRouter()


@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: AsyncSession = Depends(get_session)):
    db_user = await get_user(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    password_conditionals(
        password=user.password,
        length=settings.PASSWORD_MIN_LENGTH,
        uppercase=settings.PASSWORD_REQUIRE_UPPERCASE,
        special_characters=settings.PASSWORD_REQUIRE_SPECIAL_CHARACTERS,
    )
    new_user = await create_user(
        db=db, username=user.username, email=user.email, password=user.password
    )
    access_token = create_access_token(data={"sub": new_user.username})
    refresh_token = create_refresh_token(data={"sub": new_user.username})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": settings.TOKEN_TYPE,
    }


@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest, db: AsyncSession):
    user = await get_user(db, login_request.username)
    if not user or not verify_password(login_request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": settings.TOKEN_TYPE,
    }


@router.post("/token/refresh", response_model=Token)
async def refresh_token(request: TokenRefreshRequest):
    payload = decode_token(request.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    access_token = create_access_token(data={"sub": payload.get("sub")})
    refresh_token = create_refresh_token(data={"sub": payload.get("sub")})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": settings.TOKEN_TYPE,
    }
