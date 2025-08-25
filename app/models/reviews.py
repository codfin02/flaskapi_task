from typing import TYPE_CHECKING
from tortoise import Model, fields

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.movies import Movie


class Review(BaseModel, Model):
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="reviews", on_delete=fields.CASCADE
    )
    movie: fields.ForeignKeyRelation["Movie"] = fields.ForeignKeyField(
        "models.Movie", related_name="reviews", on_delete=fields.CASCADE
    )
    title = fields.CharField(max_length=50)
    content = fields.CharField(max_length=255)
    review_image_url = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "reviews"
        unique_together = (("user", "movie"),)
