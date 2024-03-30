from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import users
from api import websocket
from api import matching
from api import chatting


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
app.include_router(users.router)
app.include_router(websocket.router)
app.include_router(matching.router)
app.include_router(chatting.router)
