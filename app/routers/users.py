from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Request,
    UploadFile,
    Response,
)

from app.models.users import User
from app.schemas.users import (
    UserCreateRequest,
    UserLoginRequest,
    UserResponse,
    UserSearchParams,
    UserUpdateRequest,
)
from app.services.auth import AuthService
from app.services.jwt import JWTService
from app.utils.file import upload_file, validate_image_extension, delete_file

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("")
async def create_user(
    data: UserCreateRequest, auth_service: AuthService = Depends()
) -> int:
    request_data = data.model_dump()
    request_data["hashed_password"] = auth_service.hash_password(
        request_data.pop("password")
    )
    user = await User.create(**request_data)
    return user.id


@user_router.get("")
async def get_all_users() -> list[UserResponse]:
    result = await User.filter().all()
    if not result:
        raise HTTPException(status_code=404)
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            age=user.age,
            gender=user.gender,
            profile_image_url=user.profile_image_url,
        )
        for user in result
    ]


@user_router.post("/login", status_code=204)
async def login(
    data: UserLoginRequest, 
    response: Response,
    auth_service: AuthService = Depends()
) -> None:
    """사용자 로그인 API - JWT 토큰 생성 및 쿠키 설정"""
    user = await auth_service.login(data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # JWT 토큰 생성
    jwt_service = JWTService()
    access_token = jwt_service.create_access_token({"username": user.username})
    refresh_token = jwt_service.create_refresh_token({"username": user.username})
    
    # 쿠키에 토큰 설정
    jwt_service.attach_jwt_token_in_response_cookie(
        access_token, refresh_token, response
    )


@user_router.get("/search")
async def search_users(
    query_params: Annotated[UserSearchParams, Query()],
) -> list[UserResponse]:
    valid_query = {
        key: value
        for key, value in query_params.model_dump().items()
        if value is not None
    }
    filtered_users = await User.filter(**valid_query).all()
    if not filtered_users:
        raise HTTPException(status_code=404)
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            age=user.age,
            gender=user.gender,
            profile_image_url=user.profile_image_url,
        )
        for user in filtered_users
    ]


@user_router.get("/me")
async def get_user(request: Request) -> UserResponse:
    user = request.state.user
    return UserResponse(
        id=user.id,
        username=user.username,
        age=user.age,
        gender=user.gender,
        profile_image_url=user.profile_image_url,
    )


@user_router.patch("/me")
async def update_user(
    data: UserUpdateRequest, request: Request, auth_service: AuthService = Depends()
) -> UserResponse:
    user = request.state.user
    update_data = {
        key: value for key, value in data.model_dump().items() if value is not None
    }
    if "password" in update_data.keys():
        update_data["hashed_password"] = auth_service.hash_password(
            update_data.pop("password")
        )
    await user.update_from_dict(update_data)
    await user.save()
    return UserResponse(
        id=user.id,
        username=user.username,
        age=user.age,
        gender=user.gender,
        profile_image_url=user.profile_image_url,
    )


@user_router.delete("/me")
async def delete_user(request: Request) -> dict[str, str]:
    user = request.state.user
    await user.delete()

    return {"detail": "Successfully Deleted."}


@user_router.post("/me/profile_image", status_code=200)
async def register_profile_image(image: UploadFile, request: Request) -> UserResponse:
    """사용자 프로필 이미지 업로드 API"""
    validate_image_extension(image)
    user = request.state.user
    prev_image_url = user.profile_image_url

    try:
        image_url = await upload_file(image, "users/profile_images")
        user.profile_image_url = image_url
        await user.save()

        # 기존 이미지가 있다면 삭제
        if prev_image_url is not None:
            delete_file(prev_image_url)

        return UserResponse(
            id=user.id,
            username=user.username,
            age=user.age,
            gender=user.gender,
            profile_image_url=user.profile_image_url,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
