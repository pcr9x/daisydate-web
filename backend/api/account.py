from fastapi import HTTPException, APIRouter, status
from models.users import UserInfo, UserDetail, EditProfile
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from models.users import UserInfo, UserDetail, AgeRange
from api.auth import root, SECRET_KEY, ALGORITHM, save_uploaded_file
import jwt, transaction
from pydantic import BaseModel

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
async def update_user(user_id: str, detail: EditProfile):
    if user_id not in root:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
        
    photo_paths = []
    for photo in detail.photos:
        contents = await photo.read()
        file_path = save_uploaded_file(contents, photo.filename, user_id)
        photo_paths.append(file_path)
        
    user = root[user_id]
    user.detail.bio = detail.bio
    user.detail.relationship_goals = detail.relationship_goals
    user.detail.school = detail.school
    user.photos = photo_paths
    root[user_id] = user
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


@router.get("/account/preferences/{user_id}")
async def user_preferences(user_id: str):
    if user_id not in root:
        raise HTTPException(
            status_code=404, detail=f"User with ID: {user_id} not found"
        )
    return root[user_id].preferences


@router.post("/account/preferences/newGender/{user_id}/{gender}")
async def edit_user_preferences(user_id: str, gender: str):
    if user_id not in root:
        raise HTTPException(
            status_code=404, detail=f"User with ID: {user_id} not found"
        )

    user = root[user_id]
    user.preferences.gender = gender
    root[user_id] = user
    transaction.commit()
    return {"message": "edit gender successfully"}


@router.post("/account/preferences/newAgeRange/{user_id}")
async def edit_user_preferences(user_id: str, age_range: AgeRange):
    if user_id not in root:
        raise HTTPException(
            status_code=404, detail=f"User with ID: {user_id} not found"
        )

    user = root[user_id]
    user.preferences.age = (age_range.start_age, age_range.end_age)
    root[user_id] = user
    transaction.commit()
    return {"message": "edit age successfully"}


@router.post("/account/preferences/newRelationshipGoals/{user_id}/{relationship_goals}")
async def edit_user_preferences(user_id: str, relationship_goals):
    if user_id not in root:
        raise HTTPException(
            status_code=404, detail=f"User with ID: {user_id} not found"
        )

    user = root[user_id]
    user.preferences.relationship_goals = relationship_goals
    root[user_id] = user
    transaction.commit()
    return {"message": "edit relationship goals successfully"}

class UserDetailResponse(BaseModel):
    bio:str
    relationship_goals:str
    school:str
    photos: list[str]

@router.get("/account/userDetails/{user_id}", response_model=UserDetailResponse)
async def get_user_datail(user_id: str):
    if user_id not in root:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user = root[user_id]
    return UserDetailResponse(bio=user.detail.bio, relationship_goals=user.detail.relationship_goals, school=user.detail.school, photos=user.photos)