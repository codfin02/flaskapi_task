from typing import Dict, List, Annotated

from fastapi import FastAPI, HTTPException, Path, Query

from app.models.users import UserModel
from app.models.movies import MovieModel
from app.schemas.users import (
    UserCreateRequest,
    UserResponse,
    UserSearchParams,
    UserUpdateRequest,
)
from app.schemas.movies import (
    CreateMovieRequest,
    MovieResponse,
    MovieSearchParams,
    MovieUpdateRequest,
)

app = FastAPI()

# UserModel.create_dummy()  # API 테스트를 위한 더미를 생성하는 메서드 입니다.
MovieModel.create_dummy()  # API 테스트를 위한 더미를 생성하는 메서드 입니다.


@app.post("/users")
async def create_user(data: UserCreateRequest) -> int:
    user = UserModel.create(**data.model_dump())
    return user.id


@app.get("/users", response_model=List[UserResponse])
async def get_all_users() -> List[UserModel]:
    result = UserModel.all()
    if not result:
        raise HTTPException(status_code=404)
    return result


# Hint : path operations 순서를 고려하세요 !
@app.get("/users/search", response_model=List[UserResponse])
async def search_users(
    query_params: Annotated[UserSearchParams, Query()],
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


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int = Path(gt=0)) -> UserModel:
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)
    return user


@app.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(data: UserUpdateRequest, user_id: int = Path(gt=0)) -> UserModel:
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)
    user.update(**data.model_dump())
    return user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int = Path(gt=0)) -> Dict[str, str]:
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)
    user.delete()

    return {"detail": f"User: {user_id}, Successfully Deleted."}


# Movie API endpoints
@app.post("/movies", response_model=MovieResponse, status_code=201)
async def create_movie(data: CreateMovieRequest) -> MovieModel:
    movie = MovieModel.create(**data.model_dump())
    return movie


@app.get("/movies", response_model=List[MovieResponse], status_code=200)
async def get_movies(
    query_params: Annotated[MovieSearchParams, Query()],
) -> List[MovieModel]:
    valid_query = {
        key: value
        for key, value in query_params.model_dump().items()
        if value is not None
    }

    if valid_query:
        return MovieModel.filter(**valid_query)

    return MovieModel.all()


@app.get("/movies/{movie_id}", response_model=MovieResponse, status_code=200)
async def get_movie(movie_id: int = Path(gt=0)) -> MovieModel:
    movie = MovieModel.get(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404)
    return movie


@app.patch("/movies/{movie_id}", response_model=MovieResponse, status_code=200)
async def edit_movie(
    data: MovieUpdateRequest, movie_id: int = Path(gt=0)
) -> MovieModel:
    movie = MovieModel.get(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404)
    movie.update(**data.model_dump())
    return movie


@app.delete("/movies/{movie_id}", status_code=204)
async def delete_movie(movie_id: int = Path(gt=0)) -> None:
    movie = MovieModel.get(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404)
    movie.delete()
    return


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
