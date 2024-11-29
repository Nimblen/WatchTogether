from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
import logging
from typing import Type, TypeVar, Optional, List

T = TypeVar("T")

logger = logging.getLogger(__name__)

class CRUDBase:

    def __init__(self, model: Type[T]):
        """
        Base class for CRUD operations.

        Args:
            model (Type[T]): SQLAlchemy model for the CRUD operations.
        """
        self.model = model

    async def get_by_id(self, session: AsyncSession, object_id: int) -> Optional[T]:
        """Get an object by its ID."""
        return await session.get(self.model, object_id)

    async def get_all(self, session: AsyncSession) -> List[T]:
        """Get all objects of the model."""
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def delete_by_id(self, session: AsyncSession, object_id: int):
        """Delete an object by its ID."""
        obj = await self.get_by_id(session, object_id)
        if not obj:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} with ID {object_id} not found."
            )
        await session.delete(obj)
        await session.commit()

    async def create(self, session: AsyncSession, **kwargs) -> T:
        """Create a new object."""
        obj = self.model(**kwargs)
        session.add(obj)
        try:
            await session.commit()
            await session.refresh(obj)
            return obj
        except IntegrityError as exc:
            await session.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(exc.orig)}")

    async def update(self, session: AsyncSession, object_id: int, **kwargs) -> Optional[T]:
        """Update an object."""
        obj = await self.get_by_id(session, object_id)
        if not obj:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} with ID {object_id} not found."
            )
        for key, value in kwargs.items():
            if not hasattr(obj, key):
                raise HTTPException(
                    status_code=422, detail=f"{key} is not a valid attribute of {self.model.__name__}."
                )
            setattr(obj, key, value)
        await session.commit()
        await session.refresh(obj)
        return obj
