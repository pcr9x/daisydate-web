from fastapi import APIRouter, HTTPException, status
from models.users import BaseUser, UserInfo, UserLogin, UserDetail, UserPreferences
from zodb_utils import get_zodb_storage
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt, transaction, uuid

router = APIRouter()

user_storage = "users.fs"
root = get_zodb_storage(user_storage)

SECRET_KEY = "$/daisydate/hello-world-from-mesan/14-11-2023$"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/signup")
async def signup_user(user: UserInfo):
    existing_email = next((u for u in root.values() if u.email == user.email), None)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        )

    date_of_birth = datetime.strptime(user.date_of_birth, "%Y-%m-%d")
    age = (datetime.now() - date_of_birth).days // 365

    if age < 18:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Users must be at least 18 years old to sign up",
        )

    user.age = age
    user.password = pwd_context.hash(user.password)
    user.id = str(uuid.uuid4())
    root[user.id] = user
    transaction.commit()
    return BaseUser(name=user.name, email=user.email)


@router.post("/login", response_model=dict)
async def login_user(login_user: UserLogin):
    user = next((u for u in root.values() if u.email == login_user.email), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )

    if not pwd_context.verify(login_user.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user/{user_id}", response_model=UserInfo)
async def get_user(user_id: str):
    if user_id not in root:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    
    user = root[user_id]
    return user


@router.get("/users/all", response_model=list[UserInfo])
async def get_all_users():
    return list(root.values())


@router.put("/user/detail/{user_id}")
async def update_user(user_id: str, detail: UserDetail):
    if user_id not in root:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    root[user_id].detail = detail
    transaction.commit()
    return {"message": "User's detail updated successfully"}


@router.put("/user/preferences/{user_id}")
async def update_user(user_id: str, preferences: UserPreferences):
    if user_id not in root:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    root[user_id].preferences = preferences
    transaction.commit()
    return {"message": "User's preferences updated successfully"}


@router.delete("/user/delete/{user_id}")
async def delete_user(user_id: str):
    if user_id not in root:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    del root[user_id]
    transaction.commit()
    return {"message": "User deleted successfully"}
