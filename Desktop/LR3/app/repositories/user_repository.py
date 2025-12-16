from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple, Optional
from orm_db import User
from app.models.user_model import UserCreate, UserUpdate
import uuid


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]: 
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_filter(self, count: int, page: int, **kwargs) -> Tuple[List[User], int]:
        # Общее количество
        total_count_query = select(func.count()).select_from(User)
        for key, value in kwargs.items():
            if hasattr(User, key) and value is not None:
                total_count_query = total_count_query.where(getattr(User, key) == value)
        
        total_result = await self.session.execute(total_count_query)
        total = total_result.scalar_one()

        # Данные с пагинацией
        offset_val = (page - 1) * count
        query = select(User).limit(count).offset(offset_val)
        
        for key, value in kwargs.items():
            if hasattr(User, key) and value is not None:
                query = query.where(getattr(User, key) == value)
        
        result = await self.session.execute(query)
        users = list(result.scalars().all())
        
        return users, total

    async def create(self, user_data: UserCreate) -> User:
        user = User(
            username=user_data.username,
            email=user_data.email,
            description=user_data.description
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: uuid.UUID, user_data: UserUpdate) -> Optional[User]: 
        user = await self.get_by_id(user_id)
        if not user:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(user, key, value)
        
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: uuid.UUID) -> bool: 
        user = await self.get_by_id(user_id)
        if not user:
            return False
        
        await self.session.delete(user)
        await self.session.commit()
        return True