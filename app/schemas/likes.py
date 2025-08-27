from pydantic import BaseModel

from app.models.likes import ReactionTypeEnum


class ReviewLikeResponse(BaseModel):
    id: int
    user_id: int
    review_id: int
    is_liked: bool


class ReviewLikeCountResponse(BaseModel):
    review_id: int
    like_count: int


class ReviewIsLikedResponse(BaseModel):
    review_id: int
    user_id: int
    is_liked: bool


class MovieReactionResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    type: ReactionTypeEnum


class MovieReactionCountResponse(BaseModel):
    movie_id: int
    like_count: int
    dislike_count: int
