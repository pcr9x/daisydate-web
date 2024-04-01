from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api import users, websocket, matching, chatting
from api.users import get_user, SECRET_KEY, ALGORITHM
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
                username: str = payload.get("sub")
                user = get_user(username)
                if user is not None:
                    user.logged_in = False
    except Exception as e:
        pass  # Handle token extraction or decoding errors gracefully

    response = await call_next(request)
    return response


# Include your regular HTTP routes
app.include_router(users.router)
app.include_router(websocket.router)
app.include_router(matching.router)
app.include_router(chatting.router)
