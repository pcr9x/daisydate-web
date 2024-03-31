from pydantic import BaseModel, EmailStr
from typing import Tuple, List
from datetime import datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class BaseUser(BaseModel):
    name: str
    email: EmailStr


class UserDetail(BaseModel):
    bio: str = None
    relationship_goals: str = (
        None  # Long-term, Short-term, New friends, Still figuring it out
    )
    languages: str = None
    height: int = None  # [100, 250]
    interests: List[str] = (
        None  # Online Games, Football, Car Racing, Drawing, Theater, Travel, Music, Table Tennis, Anime
    )
    education: str = (
        None  # Bachelors, In College, High School, PhD, In Grad School, Masters, Trade School
    )
    pet: str = (
        None  # Dog, Cat, Reptile, Amphibian, Bird, Fish, Don't have but love, Other, Turtle, Hamster, Rabbit, Pet-free, Want a pet, Allergic to pets
    )
    drinking: str = (
        None  # Not for me, Sober, Sober serious, On special occasions, Socially on weekends, Most Nights
    )
    smoking: str = (
        None  # Social smoker, Smoker when drinking, Non-smoker, Smoker, Trying to quit
    )
    workout: str = None  # Everyday, Often, Sometimes, Never
    job_title: str = None
    company: str = None
    living_in: str = None
    mbti: str = (
        None  # INTJ, INTP, ENTJ, ENTP, INFJ, INFP, ENFJ, ENFP, ISTJ, ISFJ, ESTJ, ESFJ, ISTP, ISFP, ESTP, ESFP
    )


class UserPreferences(BaseModel):
    age: Tuple[int, int] = (18, 100)
    gender: str = "Everyone"
    relationship_goals: str = "Open to all"


class UserInfo(BaseUser):
    password: str
    date_of_birth: datetime
    age: int = None
    photos: List[str]
    gender: str
    id: str = None
    detail: UserDetail = UserDetail()
    preferences: UserPreferences = UserPreferences()
    liked: List[str] = []
    daisied: List[str] = []
    matches: List[str] = []
    daisies: int = 100


class UserLikeRequest(BaseModel):
    current_user_id: str
    other_user_id: str
