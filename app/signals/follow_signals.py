from typing import Any
from tortoise.signals import post_save

from app.models.follows import Follow
from app.utils.websocket import manager


@post_save(Follow)
async def follow_signals(
    sender: Any, 
    instance: Follow, 
    created: bool, 
    using_db: Any, 
    update_fields: Any, 
    **kwargs: Any
) -> None:
    if created or instance.is_following:
        await instance.fetch_related("follower", "following")

        await manager.send_notification(
            user_id=instance.following.id,
            message=f"{instance.follower.username}님이 팔로우 하셨습니다."
        )
