from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api import websocket, chatting, suggested, discover, account, auth
from api.auth import SECRET_KEY, ALGORITHM
from api.account import get_user
from datetime import datetime
import jwt

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware to check token expiration and log out if expired
@app.middleware("http")
async def check_token_expiration(request: Request, call_next):
    try:
        # Extract token from request headers
        authorization_header = request.headers.get("Authorization")
        if authorization_header and authorization_header.startswith("Bearer "):
            token = authorization_header.split("Bearer ")[1]
            # Decode the token to get expiration time
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            expiration_time = datetime.utcfromtimestamp(payload.get("exp"))

            # If token has expired, log out the user
            if expiration_time <= datetime.utcnow():
                user_id: str = payload.get("sub")
                user = get_user(user_id)
                if user is not None:
                    user.logged_in = False
    except Exception as e:
        pass  # Handle token extraction or decoding errors gracefully

    response = await call_next(request)
    return response


# Include your regular HTTP routes
app.include_router(auth.router)
app.include_router(account.router)
app.include_router(websocket.router)
app.include_router(suggested.router)
app.include_router(chatting.router)
app.include_router(discover.router)
