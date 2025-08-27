from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect, WebSocketState

from app.utils.websocket import manager

notification_router = APIRouter(prefix="/notifications", tags=["notifications"])


@notification_router.websocket("")
async def websocket_notifications(websocket: WebSocket) -> None:
    # JWT 토큰을 Authorization 헤더에서 가져옴
    token = websocket.headers.get("Authorization")
    
    if not token:
        await websocket.close(code=4001, reason="Authorization header required")
        return

    # 헤더로부터 가져온 토큰을 통해 유저를 가져옴
    try:
        from app.services.auth import AuthService
        from app.services.jwt import JWTService
        
        jwt_service = JWTService()
        payload = jwt_service.decode_token(token.split(" ")[1])
        username = payload.get("username")
        
        if not username:
            await websocket.close(code=4001, reason="Invalid token")
            return
            
        auth_service = AuthService()
        user = await auth_service.get_current_user(username)
        
        if not user:
            await websocket.close(code=4001, reason="User not found")
            return
            
    except Exception:
        await websocket.close(code=4001, reason="Invalid token")
        return

    await manager.connect(user_id=user.id, ws=websocket)

    try:
        while websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.receive()

    except WebSocketDisconnect:
        await manager.disconnect(ws=websocket)
