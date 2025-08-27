from fastapi import FastAPI

from app.configs.database import initialize_tortoise
from app.middleware.auth import AuthMiddleware
from app.routers.movies import movie_router
from app.routers.users import user_router
from app.routers.reviews import review_router
from app.routers.likes import like_router
from app.routers.notifications import notification_router

# 시그널 임포트
import app.signals

app = FastAPI()

# include custom middleware
app.add_middleware(AuthMiddleware)

# include router in app
app.include_router(user_router)
app.include_router(movie_router)
app.include_router(review_router)
app.include_router(like_router)
app.include_router(notification_router)

# initialize_tortoise-orm
initialize_tortoise(app=app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
