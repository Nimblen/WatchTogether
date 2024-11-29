from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from database.models import Permission, Role
from core.constants import Action
from services.core import CRUDBase


permission_crud = CRUDBase(Permission)


async def create_permission(
    name: str, description: str = None, session: AsyncSession = None
) -> Permission:
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
    return await permission_crud.create(session, {"name": name, ""})


async def add_permissions_for_role(
    role_id: int, permission_ids: list[int], session: AsyncSession
):
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

    permissions = await session.execute(
        select(Permission).filter(Permission.id.in_(permission_ids))
    )
    for permission in permissions.scalars():
        role.permissions.append(permission)

    await session.commit()


async def get_all_permissions_from_db(session: AsyncSession) -> List[Permission]:
    """Return all roles from db"""
    result = await session.execute(select(Permission))
    return result.scalars().all()


async def get_permission_from_db(
    permission_id: int, session: AsyncSession
) -> Permission:
    """Get permission by ID"""
    return await get_by_id_from_db(session, Permission, permission_id)


async def delete_permission_from_db(permission_id: int, session: AsyncSession):
    """Delete permission from db"""
    await delete_by_id_from_db(session, Permission, permission_id)

async def update_permission(
    permission_id: int,
    name: str = None,
    description: str = None,
    method: Action = None,
    session: AsyncSession = None,
) -> Permission:
    permission = await get_permission_from_db(permission_id, session)
    if not permission:
        raise HTTPException(
            status_code=404, detail=f"Permission with ID {permission_id} not found."
        )

    if name:
        permission.name = name
    if description:
        permission.description = description
    if method:
        permission.method = method

    await session.commit()
    await session.refresh(permission)
    return permission
