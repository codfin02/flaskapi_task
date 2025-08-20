from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path

from app.models.movies import MovieModel
from app.schemas.movies import (
    CreateMovieRequest,
    MovieResponse,
    MovieSearchParams,
    MovieUpdateRequest,
)

movie_router = APIRouter(prefix="/movies", tags=["movies"])


@movie_router.post("/", response_model=MovieResponse, status_code=201)
async def create_movie(data: CreateMovieRequest) -> MovieModel:
    movie = MovieModel.create(**data.model_dump())
    return movie


@movie_router.get("/", response_model=List[MovieResponse], status_code=200)
async def get_movies(query_params: MovieSearchParams = Depends()) -> List[MovieModel]:
    valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}

    if valid_query:
        return MovieModel.filter(**valid_query)

    return MovieModel.all()


@movie_router.get("/{movie_id}", response_model=MovieResponse, status_code=200)
async def get_movie(movie_id: int = Path(gt=0)) -> MovieModel:
    movie = MovieModel.get(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404)
    return movie


@movie_router.patch("/{movie_id}", response_model=MovieResponse, status_code=200)
async def edit_movie(data: MovieUpdateRequest, movie_id: int = Path(gt=0)) -> MovieModel:
    movie = MovieModel.get(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404)
    movie.update(**data.model_dump())
    return movie


@movie_router.delete("/{movie_id}", status_code=204)
async def delete_movie(movie_id: int = Path(gt=0)) -> None:
    movie = MovieModel.get(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404)
    movie.delete()
    return 