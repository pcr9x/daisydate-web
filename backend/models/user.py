from pydantic import BaseModel, EmailStr
from typing import Tuple, List


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class BaseUser(BaseModel):
    name: str
    email: EmailStr

class UserDetail(BaseModel):
    bio: str = None
    relationship_goals: str = None
    languages: str = None
    height: int = None
    interests: List[str] = None
    education: str = None # Bachelors, In College, High School, PhD, In Grad School, Masters, Trade School 
    pet: str = None
    drinking: str = None # Not for me, Sober, Sober serious, On special occasions, Socially on weekends, Most Nights
    smoking: str = None # Social smoker, Smoker when drinking, Non-smoker, Smoker, Trying to quit
    workout: str = None # Everyday, Often, Sometimes, Never
    job_title: str = None
    company: str = None
    living_in: str = None
    mbti: str = None # INTJ, INTP, ENTJ, ENTP, INFJ, INFP, ENFJ, ENFP, ISTJ, ISFJ, ESTJ, ESFJ, ISTP, ISFP, ESTP, ESFP

class UserPreferences(BaseModel):
    age: Tuple[int, int] = (18, 100)
    gender: str = None

class UserInfo(BaseUser):
    password: str
    date_of_birth: str
    age: int
    id: str = None
    detail: UserDetail = None
    preferences: UserPreferences = None
