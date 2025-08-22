from typing import Any, Dict, Optional

from passlib.context import CryptContext  # type: ignore
from tortoise.exceptions import DoesNotExist

from app.models.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self) -> None:
        self.pwd_context = pwd_context

    def hash_password(self, password: str) -> str:
        return str(self.pwd_context.hash(password))

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bool(self.pwd_context.verify(plain_password, hashed_password))

    async def authenticate(self, username: str, password: str) -> Optional[User]:
        try:
            user = await User.get(username=username)
            if self.verify_password(password, user.hashed_password):
                return user
        except DoesNotExist:
            pass
        return None

    async def login(self, username: str, password: str) -> Optional[User]:
        return await self.authenticate(username, password)

    def _get_login_response(self, user: User) -> Dict[str, Any]:
        return {
            "id": user.id,
            "username": user.username,
            "age": user.age,
            "gender": user.gender,
        }

    async def get_current_user(self, username: Optional[str]) -> Optional[User]:
        if username is None:
            return None
        try:
            return await User.get(username=username)
        except DoesNotExist:
            return None
