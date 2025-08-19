import pytest

from app.models.users import UserModel
from app.models.movies import MovieModel

TEST_BASE_URL = "http://test"


@pytest.fixture(scope="function", autouse=True)
def user_model_clear() -> None:
    UserModel.clear()


@pytest.fixture(scope="function", autouse=True)
def movie_model_clear() -> None:
    MovieModel._data.clear()
    MovieModel._id_counter = 1
