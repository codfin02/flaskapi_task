from typing import TYPE_CHECKING
from tortoise import Model, fields

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.users import User


class Follow(BaseModel, Model):
    follower: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="followers"
    )
    following: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="followings"
    )
    is_following = fields.BooleanField(default=True)

    class Meta:
        table = "follows"
        unique_together = (("follower", "following"),)
