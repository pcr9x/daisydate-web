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
    bio: str = None # Max 100 characters
    relationship_goals: str = (
        None  # Long-term, Short-term, New friends, Casual, Just chatting, Open to all
    )
    school: str = None
    # languages: str = None # No choices

    # interests: List[str] = (
    #     None  # Online Games, Football, Car Racing, Drawing, Theater, Travel, Music, Table Tennis, Anime
    # )
    # education: str = (
    #     None  # Bachelors, In College, High School, PhD, In Grad School, Masters, Trade School
    # )
    # pet: str = (
    #     None  # Dog, Cat, Reptile, Amphibian, Bird, Fish, Don't have but love, Other, Turtle, Hamster, Rabbit, Pet-free, Want a pet, Allergic to pets
    # )
    # drinking: str = (
    #     None  # Not for me, Sober, Sober serious, On special occasions, Socially on weekends, Most Nights
    # )
    # smoking: str = (
    #     None  # Social smoker, Smoker when drinking, Non-smoker, Smoker, Trying to quit
    # )
    # workout: str = None  # Everyday, Often, Sometimes, Never
    # job_title: str = None # No choices
    # company: str = None # No choices
    # living_in: str = None # No choices
    # mbti: str = (
    #     None  # INTJ, INTP, ENTJ, ENTP, INFJ, INFP, ENFJ, ENFP, ISTJ, ISFJ, ESTJ, ESFJ, ISTP, ISFP, ESTP, ESFP
    # )


class UserPreferences(BaseModel):
    age: Tuple[int, int] = (18, 100)
    gender: str = "Everyone" # Everyone, Male, Female
    relationship_goals: str = None


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
    disliked: List[str] = []
    matches: List[str] = []
    daisies: int = 100
    logged_in: bool = False


class AgeRange(BaseModel):
    start_age: int
    end_age: int

class EditProfile(BaseModel):
  photo: str = None
  bio: str = None
  relationship_goals: str = None
  school: str = None