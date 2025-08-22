from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.services.auth import AuthService
from app.services.jwt import JWTService


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            if request.url.path.startswith("/users"):
                if request.url.path not in ["/users/login", "/users", "/users/search"]:
                    # 쿠키에서 access_token 읽기
                    access_token = request.cookies.get("access_token")

                    if not access_token:
                        raise HTTPException(
                            status_code=401, detail="Access token required"
                        )

                    try:
                        # JWT 토큰 검증
                        jwt_service = JWTService()
                        payload = jwt_service.decode_token(access_token)
                        username = payload.get("username")

                        if not username:
                            raise HTTPException(status_code=401, detail="Invalid token")

                        # 사용자 정보 가져오기
                        user = await AuthService().get_current_user(username)
                        if not user:
                            raise HTTPException(
                                status_code=401, detail="User not found"
                            )

                        # request.state에 사용자 정보 설정
                        request.state.user = user

                    except Exception:
                        raise HTTPException(status_code=401, detail="Invalid token")

            response: Response = await call_next(request)
            return response

        except HTTPException as e:
            return JSONResponse({"detail": e.detail}, status_code=e.status_code)
        except Exception as e:
            return JSONResponse({"detail": str(e)}, status_code=500)
