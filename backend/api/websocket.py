from fastapi import WebSocket, FastAPI, APIRouter
from fastapi.websockets import WebSocketDisconnect

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
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.add(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            for client in websocket_clients:
                await client.send_text(data)
    finally:
        websocket_clients.remove(websocket)