from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, UploadFile

from app.models.movies import Movie
from app.schemas.movies import (
    CreateMovieRequest,
    MovieResponse,
    MovieSearchParams,
    MovieUpdateRequest,
)
from app.utils.file import delete_file, upload_file, validate_image_extension

movie_router = APIRouter(prefix="/movies", tags=["movies"])


@movie_router.post("", status_code=201)
async def create_movie(data: CreateMovieRequest) -> MovieResponse:
    movie = await Movie.create(**data.model_dump())
    return MovieResponse(
        id=movie.id,
        title=movie.title,
        plot=movie.plot,
        cast=movie.cast,
        playtime=movie.playtime,
        genre=movie.genre,
        poster_image_url=movie.poster_image_url,
    )


@movie_router.get("", status_code=200)
async def get_movies(
    query_params: Annotated[MovieSearchParams, Query()],
) -> list[MovieResponse]:
    valid_query = {
        key: value
        for key, value in query_params.model_dump().items()
        if value is not None
    }
    if valid_query:
        movies = await Movie.filter(**valid_query).all()
    else:
        movies = await Movie.filter().all()

    return [
        MovieResponse(
            id=movie.id,
            title=movie.title,
            plot=movie.plot,
            cast=movie.cast,
            playtime=movie.playtime,
            genre=movie.genre,
            poster_image_url=movie.poster_image_url,
        )
        for movie in movies
    ]


@movie_router.get("/{movie_id}", status_code=200)
async def get_movie(movie_id: int = Path(gt=0)) -> MovieResponse:
    movie = await Movie.get_or_none(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404)
    return MovieResponse(
        id=movie.id,
        title=movie.title,
        plot=movie.plot,
        cast=movie.cast,
        playtime=movie.playtime,
        genre=movie.genre,
        poster_image_url=movie.poster_image_url,
    )


@movie_router.patch("/{movie_id}", status_code=200)
async def update_movie(
    data: MovieUpdateRequest, movie_id: int = Path(gt=0)
) -> MovieResponse:
    movie = await Movie.get_or_none(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404)
    update_data = {
        key: value for key, value in data.model_dump().items() if value is not None
    }
    await movie.update_from_dict(update_data)
    await movie.save()
    return MovieResponse(
        id=movie.id,
        title=movie.title,
        plot=movie.plot,
        cast=movie.cast,
        playtime=movie.playtime,
        genre=movie.genre,
        poster_image_url=movie.poster_image_url,
    )


@movie_router.delete("/{movie_id}", status_code=204)
async def delete_movie(movie_id: int = Path(gt=0)) -> None:
    movie = await Movie.get_or_none(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404)
    await movie.delete()


@movie_router.post(
    "/{movie_id}/poster_image", response_model=MovieResponse, status_code=201
)
async def register_poster_image(
    image: UploadFile, movie_id: int = Path(gt=0)
) -> MovieResponse:
    """영화 포스터 이미지 업로드 API"""
    validate_image_extension(image)

    movie = await Movie.get_or_none(id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    prev_image_url = movie.poster_image_url
    try:
        image_url = await upload_file(image, "movies/poster_images")
        movie.poster_image_url = image_url
        await movie.save()

        # 기존 이미지가 있다면 삭제
        if prev_image_url is not None:
            delete_file(prev_image_url)

        return MovieResponse(
            id=movie.id,
            title=movie.title,
            plot=movie.plot,
            cast=movie.cast,
            playtime=movie.playtime,
            genre=movie.genre,
            poster_image_url=movie.poster_image_url,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
