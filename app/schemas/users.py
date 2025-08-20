from enum import Enum
from typing import Optional, Annotated

from pydantic import BaseModel, conint


class GenderEnum(str, Enum):
    male = "male"
    female = "female"


class UserCreateRequest(BaseModel):
    username: str
    password: str
    age: int
    gender: GenderEnum


class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    age: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    username: str
    age: int
    gender: GenderEnum


class UserSearchParams(BaseModel):
    model_config = {"extra": "forbid"}

    username: Optional[str] = None
    age: Optional[Annotated[int, conint(gt=0)]] = None
    gender: Optional[GenderEnum] = None


class UserLoginRequest(BaseModel):
    username: str
    password: str
