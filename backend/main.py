from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from api import user
from api import websocket
from PySide6.QtWebSockets import QWebSocket


app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your regular HTTP routes
app.include_router(user.router)
app.include_router(websocket.router)
