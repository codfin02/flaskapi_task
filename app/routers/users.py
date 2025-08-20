from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from fastapi.responses import Response

from app.models.users import UserModel
from app.schemas.users import (
    UserCreateRequest,
    UserLoginRequest,
    UserResponse,
    UserSearchParams,
    UserUpdateRequest,
)
from app.services.auth import AuthService

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/", response_model=int)
async def create_user(data: UserCreateRequest) -> int:
    user = UserModel.create(**data.model_dump())
    return user.id


@user_router.get("/", response_model=List[UserResponse])
async def get_all_users() -> List[UserModel]:
    result = UserModel.all()
    if not result:
        raise HTTPException(status_code=404)
    return result


@user_router.get("/search", response_model=List[UserResponse])
async def search_users(
    query_params: UserSearchParams = Depends(),
) -> List[UserModel]:
    valid_query = {
        key: value
        for key, value in query_params.model_dump().items()
        if value is not None
    }
    filtered_users = UserModel.filter(**valid_query)
    if not filtered_users:
        raise HTTPException(status_code=404)
    return filtered_users


@user_router.post("/login", status_code=204)
async def login(data: UserLoginRequest, auth_service: AuthService = Depends()) -> Response:
    return auth_service.login(data.username, data.password)


@user_router.get("/me", response_model=UserResponse)
async def get_user(request: Request) -> UserModel:
    assert isinstance(request.state.user, UserModel)
    return request.state.user


@user_router.patch("/me", response_model=UserResponse)
async def update_user(data: UserUpdateRequest, request: Request) -> UserModel:
    assert isinstance(request.state.user, UserModel)
    user = request.state.user
    user.update(**data.model_dump())
    return user


@user_router.delete("/me")
async def delete_user(request: Request) -> dict[str, str]:
    assert isinstance(request.state.user, UserModel)
    user = request.state.user
    user.delete()

    return {"detail": "Successfully Deleted."} 