from fastapi import WebSocket


class WebSocketConnectionManager:
    def __init__(self) -> None:
        # 활성화된 소켓 연결을 담을 딕셔너리. {user_id: WebSocket} 의 형태
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, ws: WebSocket) -> None:
        """
        웹 소켓 연결 수락 후 파라미터로 전달 받은 user_id를 키값으로 self.active_connections에 소켓 연결을 추가하는 코드를 작성해주세요.
        """
        await ws.accept()
        self.active_connections[user_id] = ws

    async def close(
        self, ws: WebSocket, code: int = 1000, reason: str | None = None
    ) -> None:
        """
        클라이언트에 웹 소켓 연결을 종료하는 메시지를 전송하고,
        self.disconnect 메서드를 호출하여 self.active_connections에서 해당 웹소켓 연결을 제거합니다.
        """
        await ws.send_json(
            {"type": "websocket.close", "code": code, "reason": reason or ""}
        )
        await self.disconnect(ws=ws)

    async def disconnect(self, ws: WebSocket) -> None:
        """
        파라미터로 전달받은 WebSocket 객체를 self.active_connections로 부터 제거합니다.
        """
        for user_id, conn in list(self.active_connections.items()):
            if conn == ws:
                del self.active_connections[user_id]
                break

    def get_user_connection(self, user_id: int) -> WebSocket | None:
        """
        파라미터로 전달받은 user_id를 통해 현재 유저의 웹소켓 커넥션을 self.active_connections 로 부터 가져옵니다.
        """
        if user_id not in self.active_connections:
            return None
        return self.active_connections[user_id]

    async def send_notification(self, user_id: int, message: str) -> None:
        """
        파라미터로 전달받은 user_id와 상기의 self.get_user_connection 메서드를 가져와서 현재 유저의 웹소켓 연결을 가져오고,
        웹소켓을 통해 파라미터로 전달받은 message를 전달합니다.
        이때, WebSocket 객체에 구현된 send_json() 메서드를 활용합니다.
        """
        ws = self.get_user_connection(user_id=user_id)
        if ws:
            await ws.send_json(data={"message": message})


# 웹소켓연결매니저 인스턴스화
manager = WebSocketConnectionManager()
