from enum import Enum
from typing import Any

from pydantic import BaseModel as PydanticBaseModel
from tortoise import fields

from app.models.base import BaseModel


class GenreEnum(str, Enum):
    SF = "SF"
    ROMANTIC = "Romantic"
    ADVENTURE = "Adventure"
    ACTION = "Action"
    COMEDY = "Comedy"
    HORROR = "Horror"
    FANTASY = "Fantasy"


class CastModel(PydanticBaseModel):
    name: str
    role: str


class Movie(BaseModel):
    title = fields.CharField(max_length=255)
    plot = fields.TextField()
    cast: Any = fields.JSONField()
    playtime = fields.IntField()
    genre = fields.CharEnumField(GenreEnum)
    poster_image_url = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "movies"

    def __str__(self) -> str:
        return self.title
