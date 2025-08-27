from typing import Annotated

from pydantic import BaseModel, Field

from app.models.users import GenderEnum


class UserCreateRequest(BaseModel):
    username: str
    password: str
    age: int
    gender: GenderEnum


class UserUpdateRequest(BaseModel):
    username: str | None = None
    password: str | None = None
    age: int | None = None


class UserSearchParams(BaseModel):
    model_config = {"extra": "forbid"}

    username: str | None = None
    age: Annotated[int, Field(gt=0)] | None = None
    gender: GenderEnum | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    age: int
    gender: GenderEnum
    profile_image_url: str | None = None


class UserLoginRequest(BaseModel):
    username: str
    password: str


class FollowResponse(BaseModel):
    follower_id: int
    following_id: int
    is_following: bool


class FollowingUserResponse(BaseModel):
    following_id: int
    username: str
    profile_image_url: str | None = None


class FollowerUserResponse(BaseModel):
    follower_id: int
    username: str
    profile_image_url: str | None = None
