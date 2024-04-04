from fastapi import HTTPException, APIRouter, status
from models.users import UserInfo, UserDetail
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from models.users import UserInfo, UserDetail
from api.auth import root, SECRET_KEY, ALGORITHM
import jwt, transaction

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@router.get("/account/{user_id}", response_model=UserInfo)
async def get_user(user_id: str):
    if user_id not in root:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user = root[user_id]
    return user


@router.get("/accounts/all", response_model=list[UserInfo])
async def get_all_users():
    return list(root.values())


@router.put("/account/detail/{user_id}")
async def update_user(user_id: str, detail: UserDetail):
    if user_id not in root:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    root[user_id].detail = detail
    transaction.commit()
    return {"message": "User's detail updated successfully"}


@router.delete("/account/delete/{user_id}")
async def delete_user(user_id: str):
    if user_id not in root:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    del root[user_id]
    transaction.commit()
    return {"message": "User deleted successfully"}


# Helper function to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Decode the token to get user information
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    # Check if user exists and is logged in
    user = await get_user(user_id)
    if user is None or not user.logged_in:
        raise credentials_exception

    return user


@router.post("/account/logout")
async def logout_user(current_user: UserInfo = Depends(get_current_user)):
    # Set the user's logged_in status to False
    current_user.logged_in = False
    root[current_user.id] = current_user
    transaction.commit()
    return {"message": "Logout successful"}
