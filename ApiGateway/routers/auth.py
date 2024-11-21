from fastapi import APIRouter
from core.config import settings
from utils.http_client import make_request
from schemas.auth import LoginRequest, RegisterRequest
router = APIRouter()

@router.post("/login")
async def login(request: LoginRequest):
    """
    Authenticates a user via AuthService.
    """
    url = f"{settings.AUTH_SERVICE_URL}/auth/login"
    return await make_request("POST", url, json=request.dict())

@router.post("/register")
async def register(request: RegisterRequest):
    """
    Registers a new user via AuthService.
    """
    url = f"{settings.AUTH_SERVICE_URL}/auth/register"
    return await make_request("POST", url, json=request.dict())