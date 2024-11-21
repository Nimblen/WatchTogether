from pydantic import BaseModel
from core.constants import Action


class PermissionBase(BaseModel):
    name: str
    description: str
    method: Action

    class Config:
        from_attributes = True


class PermissionCreate(PermissionBase):
    pass


class PermissionRead(PermissionBase):
    id: int
    created_at: str
    updated_at: str

