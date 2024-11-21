from pydantic import BaseModel
from typing import List
from schemas.permission import PermissionRead


class RoleBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class RoleCreate(RoleBase):
    permission_ids: List[int]  


class RoleRead(RoleBase):
    id: int
    permissions: List[PermissionRead]  
    start_date: str
    end_date: str
    created_at: str
    updated_at: str
