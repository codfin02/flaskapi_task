from typing import Annotated

from fastapi import APIRouter, Depends, Path

from app.models.likes import ReviewLike, MovieReaction, ReactionTypeEnum
from app.models.users import User
from app.schemas.likes import (
    ReviewLikeResponse,
    MovieReactionResponse,
)

like_router = APIRouter(prefix="/likes", tags=["likes"])


@like_router.post("/reviews/{review_id}/like", status_code=200)
async def like_review(
    user: Annotated[User, Depends()], review_id: int = Path(gt=0)
) -> ReviewLikeResponse:
    """리뷰 좋아요 API"""
    review_like, _ = await ReviewLike.get_or_create(
        user_id=user.id, review_id=review_id
    )

    if not review_like.is_liked:
        review_like.is_liked = True
        await review_like.save()

    return ReviewLikeResponse(
        id=review_like.id,
        user_id=review_like.user.id,
        review_id=review_like.review.id,
        is_liked=review_like.is_liked,
    )


@like_router.post("/reviews/{review_id}/unlike", status_code=200)
async def unlike_review(
    user: Annotated[User, Depends()], review_id: int = Path(gt=0)
) -> ReviewLikeResponse:
    """리뷰 좋아요 취소 API"""
    review_like = await ReviewLike.get_or_none(user_id=user.id, review_id=review_id)

    if review_like is None:
        return ReviewLikeResponse(
            id=0, user_id=user.id, review_id=review_id, is_liked=False
        )

    if review_like.is_liked:
        review_like.is_liked = False
        await review_like.save()

    return ReviewLikeResponse(
        id=review_like.id,
        user_id=review_like.user.id,
        review_id=review_like.review.id,
        is_liked=review_like.is_liked,
    )


@like_router.post("/movies/{movie_id}/like", status_code=200)
async def like_movie(
    user: Annotated[User, Depends()], movie_id: int = Path(gt=0)
) -> MovieReactionResponse:
    """영화 좋아요 API"""
    reaction, _ = await MovieReaction.get_or_create(user_id=user.id, movie_id=movie_id)

    if reaction.type != ReactionTypeEnum.LIKE:
        reaction.type = ReactionTypeEnum.LIKE
        await reaction.save()

    return MovieReactionResponse(
        id=reaction.id,
        user_id=reaction.user.id,
        movie_id=reaction.movie.id,
        type=reaction.type,
    )


@like_router.post("/movies/{movie_id}/dislike", status_code=200)
async def dislike_movie(
    user: Annotated[User, Depends()], movie_id: int = Path(gt=0)
) -> MovieReactionResponse:
    """영화 싫어요 API"""
    reaction, _ = await MovieReaction.get_or_create(user_id=user.id, movie_id=movie_id)

    if reaction.type != ReactionTypeEnum.DISLIKE:
        reaction.type = ReactionTypeEnum.DISLIKE
        await reaction.save()

    return MovieReactionResponse(
        id=reaction.id,
        user_id=reaction.user.id,
        movie_id=reaction.movie.id,
        type=reaction.type,
    )
