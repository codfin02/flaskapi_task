from typing import TYPE_CHECKING
from tortoise import Model, fields

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.reviews import Review


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
