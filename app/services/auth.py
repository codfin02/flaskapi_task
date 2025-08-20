from fastapi import HTTPException, Request, Response, status

from app.models.users import UserModel
from app.services.jwt import JWTService


class AuthService:
    def __init__(self) -> None:
        self.jwt_service = JWTService()

    def login(self, username: str, password: str) -> Response:
        """
        입력받은 username, password를 검증하여 유저를 가져오고,
        가져온 유저에 대해서 액세스 토큰, 리프레쉬 토큰을 생성하고
        이를 응답으로 반환하는 함수입니다.
        """
        user = UserModel.authenticate(username, password)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

        access_token = self.jwt_service.create_access_token(data={"user_id": user.id})
        refresh_token = self.jwt_service.create_refresh_token(data={"user_id": user.id})

        response = self._get_login_response(access_token, refresh_token)

        return response

    def _get_login_response(self, access_token: str, refresh_token: str) -> Response:
        """
        입력받은 액세스 토큰과 리프레쉬 토큰을 쿠키에 저장하여 이를 응답 객체(Response)로 반환합니다.
        """
        response = Response(status_code=204)
        self.jwt_service.attach_jwt_token_in_response_cookie(access_token, refresh_token, response)
        return response

    def get_current_user(self, request: Request) -> Request:
        """
        요청 객체에 포함된 쿠키로 부터 엑세스 토큰을 가져와 이를 디코딩합니다.
        디코딩 된 토큰의 페이로드로 부터 유저 아이디를 가져옵니다.
        가져온 유저아이디를 통해 유저객체를 가져오고 요청객체의 state에 user 객체를 추가하고
        요청 객체를 리턴합니다.
        """
        access_token = request.cookies.get("access_token")
        if not access_token:
            raise HTTPException(status_code=401, detail="Unauthorized.")

        decoded = self.jwt_service._decode(access_token)

        user = UserModel.get(id=decoded["user_id"])
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized.")

        request.state.user = user

        return request 