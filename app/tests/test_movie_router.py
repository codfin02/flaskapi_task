import httpx
from fastapi import status

from main import app
from app.models.movies import MovieModel


async def test_api_create_movie() -> None:
    # given
    data = {"title": "test_movie", "playtime": 120, "genre": ["Action", "Adventure"]}

    # when
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)) as client:
        response = await client.post(url="/movies", json=data)

    # then
    assert response.status_code == status.HTTP_201_CREATED
    created_movie = response.json()
    assert created_movie["title"] == data["title"]
    assert created_movie["playtime"] == data["playtime"]
    assert created_movie["genre"] == data["genre"]


async def test_api_get_movies() -> None:
    # given
    MovieModel.create_dummy()

    # when
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)) as client:
        response = await client.get(url="/movies")

    # then
    assert response.status_code == status.HTTP_200_OK
    movies = response.json()
    assert len(movies) > 0
    assert "id" in movies[0]
    assert "title" in movies[0]
    assert "playtime" in movies[0]
    assert "genre" in movies[0]


async def test_api_get_movies_with_title_filter() -> None:
    # given
    MovieModel.create_dummy()

    # when
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)) as client:
        response = await client.get(url="/movies?title=dummy_movie")

    # then
    assert response.status_code == status.HTTP_200_OK
    movies = response.json()
    assert len(movies) > 0
    assert all("dummy_movie" in movie["title"] for movie in movies)


async def test_api_get_movies_with_genre_filter() -> None:
    # given
    MovieModel.create_dummy()

    # when
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)) as client:
        response = await client.get(url="/movies?genre=Action")

    # then
    assert response.status_code == status.HTTP_200_OK
    movies = response.json()
    assert len(movies) > 0
    assert all("Action" in movie["genre"] for movie in movies)


async def test_api_get_movie() -> None:
    # given
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)) as client:
        create_response = await client.post(
            url="/movies",
            json={"title": "test_movie", "playtime": 120, "genre": ["Action"]},
        )
        movie_id = create_response.json()["id"]

        # when
        response = await client.get(url=f"/movies/{movie_id}")

        # then
        assert response.status_code == status.HTTP_200_OK
        movie = response.json()
        assert movie["id"] == movie_id
        assert movie["title"] == "test_movie"
        assert movie["playtime"] == 120
        assert movie["genre"] == ["Action"]


async def test_api_get_movie_not_found() -> None:
    # when
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)) as client:
        response = await client.get(url="/movies/99999")

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_api_update_movie() -> None:
    # given
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)) as client:
        create_response = await client.post(
            url="/movies",
            json={"title": "test_movie", "playtime": 120, "genre": ["Action"]},
        )
        movie_id = create_response.json()["id"]

        # when
        response = await client.patch(
            url=f"/movies/{movie_id}", json={"title": "updated_movie", "playtime": 150}
        )

        # then
        assert response.status_code == status.HTTP_200_OK
        movie = response.json()
        assert movie["title"] == "updated_movie"
        assert movie["playtime"] == 150
        assert movie["genre"] == ["Action"]


async def test_api_update_movie_not_found() -> None:
    # when
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)) as client:
        response = await client.patch(
            url="/movies/99999", json={"title": "updated_movie"}
        )

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_api_delete_movie() -> None:
    # given
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)) as client:
        create_response = await client.post(
            url="/movies",
            json={"title": "test_movie", "playtime": 120, "genre": ["Action"]},
        )
        movie_id = create_response.json()["id"]

        # when
        response = await client.delete(url=f"/movies/{movie_id}")

        # then
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # verify movie is deleted
        get_response = await client.get(url=f"/movies/{movie_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


async def test_api_delete_movie_not_found() -> None:
    # when
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)) as client:
        response = await client.delete(url="/movies/99999")

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND
