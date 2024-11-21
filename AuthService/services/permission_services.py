import re
from passlib.context import CryptContext
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database.models import User, Permission, Role, role_permissions
from services.token_services import decode_token



from sqlalchemy.ext.asyncio import AsyncSession
from database.models.permission import Permission
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


async def create_permission(name: str, description: str = None, session: AsyncSession = None):
    """
    Creates a new permission in the database.

    Args:
        name (str): The name of the permission. Must be unique.
        description (str, optional): A description of the permission.
        session (AsyncSession): The database session.

    Returns:
        Permission: The created permission object.

    Raises:
        HTTPException: If a permission with the same name already exists.
    """
    new_permission = Permission(name=name, description=description)
    session.add(new_permission)
    try:
        await session.commit()
        await session.refresh(new_permission)
        return new_permission
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Permission with name '{name}' already exists.")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create permission: {str(e)}")






async def add_permissions_for_role(role_id: int, permission_ids: list[int], session: AsyncSession):
    """
    Adds permissions to a role by ID.

    Args:
        role_id (int): ID of the role.
        permission_ids (list[int]): List of permission IDs to add.
        session (AsyncSession): Database session.

    Returns:
        None
    """
    role = await session.get(Role, role_id)
    if not role:
        raise ValueError(f"Role with ID {role_id} not found")

    permissions = await session.execute(select(Permission).filter(Permission.id.in_(permission_ids)))
    for permission in permissions.scalars():
        role.permissions.append(permission)

    await session.commit()


async def delete_role_permissions(role_id: int, permission_id: int, session: AsyncSession):
    """
    Removes a specific permission from a role by ID.

    Args:
        role_id (int): ID of the role.
        permission_id (int): ID of the permission to remove.
        session (AsyncSession): Database session.

    Returns:
        None
    """
    role = await session.get(Role, role_id)
    if not role:
        raise ValueError(f"Role with ID {role_id} not found")

    permission = next((perm for perm in role.permissions if perm.id == permission_id), None) # 
    if permission:
        role.permissions.remove(permission)

    await session.commit()

async def get_role_permissions_from_db(role_id: int, session: AsyncSession) -> list[str]:
    """
    Fetches all permissions for a user's role by role ID.

    Args:
        role_id (int): ID of the user's role.
        session (AsyncSession): Database session.

    Returns:
        list[str]: List of permission names.
    """
    permissions = await session.execute(
        select(Permission.name)
        .join(role_permissions, role_permissions.c.permission_id == Permission.id)
        .where(role_permissions.c.role_id == role_id)
    )
    return permissions.scalars().all()
