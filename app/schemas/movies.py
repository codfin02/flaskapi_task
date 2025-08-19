from typing import List, Optional, Annotated
from pydantic import BaseModel, Field


class CreateMovieRequest(BaseModel):
    title: str
    playtime: int
    genre: List[str]


class MovieUpdateRequest(BaseModel):
    title: Optional[str] = None
    playtime: Optional[Annotated[int, Field(gt=0)]] = None
    genre: Optional[List[str]] = None


class MovieResponse(BaseModel):
    id: int
    title: str
    playtime: int
    genre: List[str]


class MovieSearchParams(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
