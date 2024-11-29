from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Role, user_roles, Permission, role_permissions


async def get_all_roles_from_db(session: AsyncSession) -> List[Role]:
    """Return all roles from db"""
    result = await session.execute(select(Role))  
    return result.scalars().all()

async def get_role_by_id(role_id: int, session: AsyncSession) -> Role:
    return await session.get(Role, role_id)

async def delete_role_from_db(role_id: int, session: AsyncSession):
    role = await get_role_by_id(role_id, session)
    if not role:
        raise ValueError(f"Role with ID {role} not found.")
    await session.delete(role)
    await session.commit()


async def get_role_permissions_from_db(
    role_id: int, session: AsyncSession
) -> list[str]:
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






async def delete_role_permissions(
    role_id: int, permission_id: int, session: AsyncSession
):
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

    permission = next(
        (perm for perm in role.permissions if perm.id == permission_id), None
    )
    if permission:
        role.permissions.remove(permission)
    await session.commit()