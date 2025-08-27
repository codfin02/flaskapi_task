from enum import StrEnum
from typing import TYPE_CHECKING
from tortoise import Model, fields

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.reviews import Review
    from app.models.movies import Movie


class ReactionTypeEnum(StrEnum):
    LIKE = "like"
    DISLIKE = "dislike"


class ReviewLike(BaseModel, Model):
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="review_likes"
    )
    review: fields.ForeignKeyRelation["Review"] = fields.ForeignKeyField(
        "models.Review", related_name="likes"
    )
    is_liked = fields.BooleanField(default=True)

    class Meta:
        table = "review_likes"
        unique_together = (("user", "review"),)


class MovieReaction(BaseModel, Model):
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="movie_reactions"
    )
    movie: fields.ForeignKeyRelation["Movie"] = fields.ForeignKeyField(
        "models.Movie", related_name="reactions"
    )
    type = fields.CharEnumField(ReactionTypeEnum, default=ReactionTypeEnum.LIKE)

    class Meta:
        table = "movie_reactions"
        unique_together = (("user", "movie"),)
