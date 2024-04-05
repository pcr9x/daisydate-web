from fastapi import HTTPException, APIRouter, File, UploadFile, Form, status
from models.users import UserInfo, UserLogin
from fastapi import APIRouter, HTTPException, status
from models.users import UserInfo, UserLogin
from zodb_utils import get_zodb_storage
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import List
import jwt, transaction, uuid, os

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


in_progress_registrations = {}

# CAPT- DONE
@router.post("/auth/signup/identifier", response_model=dict)
async def signup_identifier(user_data: dict):
    email = user_data.get("email")
    existing_email = next((u for u in root.values() if u.email == email), None)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        )

    password = user_data.get("password")
    hash_password = pwd_context.hash(password)
    registration_id = str(uuid.uuid4())
    in_progress_registrations[registration_id] = {
        "email": email,
        "password": hash_password,
    }
    return {
        "registration_id": registration_id,
        "message": "Email and password are valid",
    }

# CAPT- DONE
@router.post("/auth/signup/date-of-birth", response_model=dict)
async def signup_date_of_birth(user_data: dict):
    registration_id = user_data.get("registration_id")
    date_of_birth = user_data.get("date_of_birth")

    registration_data = in_progress_registrations.get(registration_id)
    if not registration_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid registration process.",
        )

    date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d")
    age = (datetime.now() - date_of_birth).days // 365
    if age < 18:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Users must be at least 18 years old to sign up",
        )

    registration_data["date_of_birth"] = date_of_birth
    registration_data["age"] = age
    in_progress_registrations[registration_id] = registration_data

    return {"message": "Date of birth is valid"}

# CAPT- DONE
@router.post("/auth/signup/details")
async def signup_details(user_data: dict):
    registration_id = user_data.get("registration_id")
    name = user_data.get("name")
    gender = user_data.get("gender")
    pref_gender = user_data.get("show_me")

    registration_data = in_progress_registrations.get(registration_id)
    if not registration_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid registration process.",
        )

    registration_data["name"] = name
    registration_data["gender"] = gender
    registration_data["show_me"] = pref_gender
    in_progress_registrations[registration_id] = registration_data

    return {"message": "User details are valid"}


UPLOAD_FOLDER = "assets/userImages"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_uploaded_file(contents, filename, user_id):
    user_directory = os.path.join(UPLOAD_FOLDER, user_id)
    os.makedirs(user_directory, exist_ok=True)
    file_path = os.path.join(user_directory, filename)
    with open(file_path, "wb") as new_file:
        new_file.write(contents)
    return file_path

# CAPT- DONE
@router.post("/auth/signup/photos")
async def signup_photos(
    registration_id: str = Form(...),
    photos: List[UploadFile] = File(...),
):
    registration_data = in_progress_registrations.get(registration_id)
    if not registration_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid registration process.",
        )

    email = registration_data.get("email")
    hash_password = registration_data.get("password")
    date_of_birth = registration_data.get("date_of_birth")
    age = registration_data.get("age")
    name = registration_data.get("name")
    gender = registration_data.get("gender")
    pref_gender = registration_data.get("show_me")
    user_id = str(uuid.uuid4())
    photo_paths = []
    for photo in photos:
        contents = await photo.read()
        file_path = save_uploaded_file(contents, photo.filename, user_id)
        photo_paths.append(file_path)

    user = UserInfo(
        name=name,
        email=email,
        password=hash_password,
        date_of_birth=date_of_birth,
        age=age,
        photos=photo_paths,
        gender=gender,
        id=user_id,
    )

    user.preferences.gender = pref_gender
    user.logged_in = True
    root[user.id] = user
    transaction.commit()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user.id),
    }


# CAPT- DONE
@router.post("/auth/login", response_model=dict)
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

    root[user.id].logged_in = True
    transaction.commit()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "user_id": str(user.id)}
