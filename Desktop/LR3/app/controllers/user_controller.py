from typing import List, Dict, Any
from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from litestar.params import Parameter
from litestar.exceptions import NotFoundException
import uuid 

from app.services.user_service import UserService
from app.models.user_model import UserCreate, UserUpdate, UserResponse


class UserController(Controller):
    path = "/users"
    dependencies = {"user_service": Provide(UserService)}

    @get("/{user_id:uuid}") 
    async def get_user_by_id(
        self,
        user_service: UserService,
        user_id: uuid.UUID = Parameter(description="ID пользователя"), 
    ) -> UserResponse:
        """Получить пользователя по ID"""
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @get()
    async def get_all_users(
        self,
        user_service: UserService,
        count: int = Parameter(default=10, ge=1, le=100, description="Количество записей на странице"),
        page: int = Parameter(default=1, ge=1, description="Номер страницы"),
    ) -> Dict[str, Any]:
        """Получить всех пользователей с пагинацией"""
        users, total = await user_service.get_by_filter(count=count, page=page)
        
        return {
            "users": [UserResponse.model_validate(user) for user in users],
            "total": total,
            "page": page,
            "count": count,
            "pages": (total + count - 1) // count if total > 0 else 0
        }

    @post()
    async def create_user(
        self,
        user_service: UserService,
        user_data: UserCreate,
    ) -> UserResponse:
        """Создать нового пользователя"""
        user = await user_service.create(user_data)
        return UserResponse.model_validate(user)

    @delete("/{user_id:uuid}")
    async def delete_user(
    self,
    user_service: UserService,
    user_id: uuid.UUID = Parameter(description="ID пользователя"),) -> None:  # Измените тип возвращаемого значения
        """Удалить пользователя"""
        success = await user_service.delete(user_id)
        if not success:
            raise NotFoundException(detail=f"User with ID {user_id} not found")

    @put("/{user_id:uuid}")  
    async def update_user(
        self,
        user_service: UserService,
        user_id: uuid.UUID = Parameter(description="ID пользователя"),  
        user_data: UserUpdate = Parameter(description="Данные для обновления"),
    ) -> UserResponse:
        """Обновить пользователя"""
        user = await user_service.update(user_id, user_data)
        return UserResponse.model_validate(user)