from pydantic import BaseModel, EmailStr
from schemas.role import RoleRead
from typing import List

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role_ids: List[int]


class LoginRequest(BaseModel):
    username: str
    password: str



class UserRead(BaseModel):
    id: int
    username: str
    email: str
    roles: List[RoleRead]

    class Config:
        from_attributes = True
