from fastapi import WebSocket, FastAPI, APIRouter, HTTPException
from fastapi.websockets import WebSocketDisconnect
from api.chatting import send_message, chatting
from models.chatting import Message
router = APIRouter()
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)

# manager = ConnectionManager()

# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
            
#             # Handle received message (e.g., process and respond)
#             await manager.broadcast(data)
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast("User disconnected")
websocket_clients = set()

# WebSocket endpoint
@router.websocket("/ws/{user_id}/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, user_id:str, chat_id:str):
    await websocket.accept()
    chatRoom = chatting[chat_id]
    if user_id != chatRoom.userID1 and user_id != chatRoom.userID2:
        raise HTTPException(status_code=404, detail="User is not a part of this chat room.")
    
    websocket_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            datas = data.split("/");
            await send_message(chat_id=datas[1], message=Message(
                senderID=datas[0],
                message=datas[2]
            ))
            for client in websocket_clients:
                await client.send_text(data)
    finally:
        websocket_clients.remove(websocket)