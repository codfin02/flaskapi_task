from typing import Annotated

from fastapi import (
    APIRouter,
    Form,
    UploadFile,
    File,
    Depends,
    Path,
    HTTPException,
)

from app.models.reviews import Review
from app.models.users import User
from app.schemas.reviews import ReviewResponse
from app.utils.file import upload_file, delete_file

review_router = APIRouter(prefix="/reviews", tags=["reviews"])


@review_router.post("", status_code=201)
async def create_movie_review(
    user: Annotated[User, Depends()],
    movie_id: int = Form(),
    title: str = Form(),
    content: str = Form(),
    review_image: UploadFile | None = File(None),
) -> ReviewResponse:
    """영화 리뷰 생성 API"""
    review_data = {
        "user_id": user.id,
        "movie_id": movie_id,
        "title": title,
        "content": content,
    }

    if review_image:
        review_data["review_image_url"] = await upload_file(
            review_image, "reviews/images"
        )

    review = await Review.create(
        user_id=review_data["user_id"],
        movie_id=review_data["movie_id"],
        title=review_data["title"],
        content=review_data["content"],
        review_image_url=review_data.get("review_image_url"),
    )

    return ReviewResponse(
        id=review.id,
        user_id=user.id,
        movie_id=movie_id,
        title=review.title,
        content=review.content,
        review_image_url=review.review_image_url,
    )


@review_router.get("/{review_id}")
async def get_review(review_id: int = Path(gt=0)) -> ReviewResponse:
    """리뷰 조회 API"""
    review = await Review.get_or_none(id=review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review does not exist")
    return ReviewResponse(
        id=review.id,
        user_id=review.user.id,
        movie_id=review.movie.id,
        title=review.title,
        content=review.content,
        review_image_url=review.review_image_url,
    )


@review_router.patch("/{review_id}")
async def update_review(
    user: Annotated[User, Depends()],
    update_title: str | None = Form(None),
    update_content: str | None = Form(None),
    update_image: UploadFile | None = File(None),
    review_id: int = Path(gt=0),
) -> ReviewResponse:
    """리뷰 수정 API"""
    review = await Review.get_or_none(id=review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review does not exist")

    if review.user.id != user.id:
        raise HTTPException(
            status_code=403, detail="Only the review owner can update reviews"
        )

    review.title = update_title if update_title is not None else review.title
    review.content = update_content if update_content is not None else review.content
    if update_image:
        prev_image_url = review.review_image_url
        review.review_image_url = await upload_file(update_image, "reviews/images")

        if prev_image_url is not None:
            delete_file(prev_image_url)

    await review.save()

    return ReviewResponse(
        id=review.id,
        user_id=review.user.id,
        movie_id=review.movie.id,
        title=review.title,
        content=review.content,
        review_image_url=review.review_image_url,
    )


@review_router.delete("/{review_id}", status_code=204)
async def delete_review(
    user: Annotated[User, Depends()], review_id: int = Path(gt=0)
) -> None:
    """리뷰 삭제 API"""
    review = await Review.get_or_none(id=review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review does not exist")

    if review.user.id != user.id:
        raise HTTPException(
            status_code=403, detail="Only the review owner can delete review."
        )

    await review.delete()


@review_router.get("/{review_id}/like_count")
async def get_review_like_count(review_id: int = Path(gt=0)) -> dict[str, int]:
    """리뷰 좋아요 개수 조회 API"""
    from app.models.likes import ReviewLike

    like_count = await ReviewLike.filter(review_id=review_id, is_liked=True).count()
    return {"review_id": review_id, "like_count": like_count}


@review_router.get("/{review_id}/is_liked")
async def get_user_review_is_liked(
    user: Annotated[User, Depends()], review_id: int = Path(gt=0)
) -> dict[str, int | bool]:
    """사용자가 특정 리뷰에 좋아요를 눌렀는지 확인 API"""
    from app.models.likes import ReviewLike

    like = await ReviewLike.get_or_none(review_id=review_id, user_id=user.id)
    if like is None:
        return {"review_id": review_id, "user_id": user.id, "is_liked": False}

    return {
        "review_id": like.review.id,
        "user_id": like.user.id,
        "is_liked": like.is_liked,
    }
