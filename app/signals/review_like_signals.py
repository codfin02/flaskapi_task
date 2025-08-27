from typing import Any
from tortoise.signals import post_save

from app.models.likes import ReviewLike
from app.utils.websocket import manager


@post_save(ReviewLike)
async def review_like_signals(
    sender: Any, 
    instance: ReviewLike, 
    created: bool, 
    using_db: Any, 
    update_fields: Any, 
    **kwargs: Any
) -> None:
    if created or instance.is_liked:
        await instance.fetch_related("review__user", "user")
        review_writer = instance.review.user
        user = instance.user

        await manager.send_notification(
            user_id=review_writer.id,
            message=f"{user.username}님이 내 리뷰에 좋아요를 눌렀습니다!"
        )
